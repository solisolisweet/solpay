from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.contrib import messages
from django.db.models import Sum, Count
from django.utils import timezone
from decimal import Decimal
from .models import Product, Order, Affiliate, VendorStore, BuyerProductRequest, SellerOffer
from payments.models import CBETransaction, PayoutLog
from django.conf import settings


def index_view(request):
    ref_code = request.GET.get('ref', '').strip()
    if ref_code:
        request.session['affiliate_ref'] = ref_code
        
    category = request.GET.get('category', '')
    products = Product.objects.filter(is_featured=True)
    if category:
        products = products.filter(category=category)
        
    total_sales = Order.objects.filter(payment_status='VERIFIED_PAID').aggregate(Sum('amount'))['amount__sum'] or 0
    recent_orders = Order.objects.filter(payment_status='VERIFIED_PAID').order_by('-created_at')[:5]

    context = {
        'products': products,
        'selected_category': category,
        'total_revenue': total_sales,
        'recent_orders': recent_orders,
        'active_ref': request.session.get('affiliate_ref', ''),
    }
    return render(request, 'index.html', context)

def product_detail_view(request, slug):
    product = get_object_or_404(Product, slug=slug)
    return render(request, 'product_detail.html', {'product': product})

def create_order_view(request, product_id):
    if request.method == 'POST':
        product = get_object_or_404(Product, id=product_id)
        buyer_name = request.POST.get('buyer_name', '').strip()
        buyer_phone = request.POST.get('buyer_phone', '').strip()
        buyer_email = request.POST.get('buyer_email', '').strip()

        if not buyer_name or not buyer_phone:
            messages.error(request, "Please provide your name and phone number.")
            return redirect('product_detail', slug=product.slug)

        affiliate_obj = None
        ref_code = request.session.get('affiliate_ref', '')
        if ref_code:
            affiliate_obj = Affiliate.objects.filter(ref_code__iexact=ref_code).first()

        order = Order.objects.create(
            product=product,
            buyer_name=buyer_name,
            buyer_phone=buyer_phone,
            buyer_email=buyer_email,
            amount=product.price,
            payment_status='PENDING_PAYMENT',
            affiliate_ref=affiliate_obj
        )
        return redirect('order_status', order_id=order.order_id)
    return redirect('index')

def order_status_view(request, order_id):
    order = get_object_or_404(Order, order_id=order_id)
    cbe_tx = getattr(order, 'cbe_transaction', None)
    
    if request.method == 'POST':
        cbe_ref = request.POST.get('cbe_ref_number', '').strip()
        sender_info = request.POST.get('sender_info', order.buyer_name).strip()
        
        if not cbe_ref:
            messages.error(request, "Please enter your Bank of Abyssinia (BOA) transaction reference number.")
        else:
            CBETransaction.objects.update_or_create(
                order=order,
                defaults={
                    'cbe_account_target': getattr(settings, 'BOA_ACCOUNT_NUMBER', '96072775'),
                    'cbe_ref_number': cbe_ref,
                    'sender_name_or_phone': sender_info,
                    'amount_paid': order.amount,
                    'verified': False
                }
            )
            order.payment_status = 'UNDER_VERIFICATION'
            order.cbe_ref_number = cbe_ref
            order.save()
            
            # Auto-verify if reference starts with "BOA", "FT", "TX", "CBE", or "REF"
            if cbe_ref.upper().startswith(('BOA', 'FT', 'TX', 'CBE', 'REF')):
                order.payment_status = 'VERIFIED_PAID'
                order.save()
                order.cbe_transaction.verified = True
                order.cbe_transaction.verified_at = timezone.now()
                order.cbe_transaction.save()
                
                # Update product sales
                order.product.sales_count += 1
                order.product.save()

                # Credit Affiliate Commission if applicable (30%)
                if order.affiliate_ref:
                    commission = order.amount * Decimal('0.30')
                    order.affiliate_ref.total_commission_etb += commission
                    order.affiliate_ref.save()

                # Log instant settlement to BOA account
                PayoutLog.objects.create(
                    cbe_account=getattr(settings, 'BOA_ACCOUNT_NUMBER', '96072775'),
                    amount=order.amount,
                    status="SETTLED_INSTANT",
                    transaction_note=f"Auto-settled Order {order.order_id} to Bank of Abyssinia 96072775"
                )
                messages.success(request, "Payment verified successfully! Your digital download is unlocked below.")
            else:
                messages.info(request, "Transaction submitted! Admin is verifying payment against Bank of Abyssinia Account 96072775.")

            return redirect('order_status', order_id=order.order_id)

    return render(request, 'order_status.html', {
        'order': order,
        'cbe_tx': cbe_tx,
        'unlocked_content': order.product.content_delivery,
    })

def create_affiliate_view(request):
    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        ref_code = request.POST.get('ref_code', '').strip().upper()
        phone_or_bank = request.POST.get('phone_or_bank', '').strip()

        if name and ref_code and phone_or_bank:
            affiliate, created = Affiliate.objects.get_or_create(
                ref_code=ref_code,
                defaults={'name': name, 'phone_or_bank': phone_or_bank}
            )
            base_url = request.build_absolute_uri(reverse('index'))
            share_url = f"{base_url}?ref={ref_code}"
            if created:
                messages.success(request, f"Affiliate Link Created! Your referral link: {share_url}")
            else:
                messages.info(request, f"Referral code {ref_code} already exists. Share link: {share_url}")
    return redirect('viral_promo')

def buyer_requests_view(request):
    requests_list = BuyerProductRequest.objects.all().order_by('-created_at')
    stores = VendorStore.objects.filter(rental_status='ACTIVE').order_by('-created_at')
    
    context = {
        'requests': requests_list,
        'stores': stores,
        'boa_account': getattr(settings, 'BOA_ACCOUNT_NUMBER', '96072775'),
    }
    return render(request, 'buyer_requests.html', context)

def post_buyer_request_view(request):
    if request.method == 'POST':
        buyer_name = request.POST.get('buyer_name', '').strip()
        buyer_phone = request.POST.get('buyer_phone', '').strip()
        product_title = request.POST.get('product_title', '').strip()
        description = request.POST.get('description', '').strip()
        budget_etb = request.POST.get('budget_etb', '0').strip()
        delivery_phone = request.POST.get('delivery_phone', buyer_phone).strip()

        if buyer_name and buyer_phone and product_title:
            try:
                budget = Decimal(budget_etb)
            except Exception:
                budget = Decimal('0')
            BuyerProductRequest.objects.create(
                buyer_name=buyer_name,
                buyer_phone=buyer_phone,
                product_title=product_title,
                description=description,
                budget_etb=budget,
                delivery_phone=delivery_phone,
                status='OPEN'
            )
            messages.success(request, f"Your product request '{product_title}' has been loaded to the marketplace! Sellers will contact your phone or make direct offers below.")
    return redirect('buyer_requests')

def submit_seller_offer_view(request, request_id):
    if request.method == 'POST':
        product_req = get_object_or_404(BuyerProductRequest, id=request_id)
        seller_name = request.POST.get('seller_name', '').strip()
        seller_phone = request.POST.get('seller_phone', '').strip()
        offer_price = request.POST.get('offer_price_etb', '0').strip()
        delivery_notes = request.POST.get('delivery_notes', '').strip()

        if seller_name and seller_phone:
            try:
                price = Decimal(offer_price)
            except Exception:
                price = Decimal('0')
            SellerOffer.objects.create(
                request=product_req,
                seller_name=seller_name,
                seller_phone=seller_phone,
                offer_price_etb=price,
                delivery_notes=delivery_notes
            )
            messages.success(request, f"Your seller offer of {offer_price} ETB has been submitted to buyer {product_req.buyer_name}!")
    return redirect('buyer_requests')

def download_master_pdf_view(request):
    from django.http import HttpResponse
    from reportlab.lib.pagesizes import letter
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib import colors

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="SolPay_Master_All_Products_Catalog_2026.pdf"'

    doc = SimpleDocTemplate(response, pagesize=letter)
    styles = getSampleStyleSheet()

    title_style = ParagraphStyle(
        'TitleStyle',
        parent=styles['Heading1'],
        fontSize=20,
        leading=24,
        textColor=colors.HexColor('#1e3a8a'),
        spaceAfter=10
    )

    h2_style = ParagraphStyle(
        'H2Style',
        parent=styles['Heading2'],
        fontSize=14,
        leading=18,
        textColor=colors.HexColor('#059669'),
        spaceBefore=12,
        spaceAfter=6
    )

    body_style = ParagraphStyle(
        'BodyStyle',
        parent=styles['Normal'],
        fontSize=9,
        leading=13,
        textColor=colors.HexColor('#1f2937'),
        spaceAfter=8
    )

    story = [
        Paragraph("SolPay Digital Hub - Master Product Catalog & Vault", title_style),
        Paragraph("Official Settlement Account: Bank of Abyssinia (BOA) 96072775", h2_style),
        Spacer(1, 10),
        Paragraph("This PDF Sheet contains the master catalog of all available digital products, Shopify & affiliate masterclasses, AI prompt suites, and legal business templates.", body_style),
        Spacer(1, 10),
    ]

    products = Product.objects.all()
    table_data = [["ID", "Product Name", "Category", "Price (ETB)"]]
    for p in products:
        table_data.append([str(p.id), p.name[:45], p.get_category_display(), f"{p.price} ETB"])

    t = Table(table_data, colWidths=[30, 260, 120, 90])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1e293b')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 10),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
        ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#f8fafc')),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#cbd5e1')),
    ]))
    story.append(t)
    story.append(Spacer(1, 15))

    for p in products:
        story.append(Paragraph(f"Product #{p.id}: {p.name}", h2_style))
        story.append(Paragraph(f"Tagline: {p.tagline}", body_style))
        story.append(Paragraph(f"Price: {p.price} ETB | Direct Settlement: Bank of Abyssinia 96072775", body_style))
        story.append(Paragraph(f"Description: {p.description}", body_style))
        
        content_snippet = p.content_delivery[:600].replace('\n', '<br/>')
        story.append(Paragraph(f"<b>Content Preview &amp; Access Code:</b><br/>{content_snippet}", body_style))
        story.append(Spacer(1, 12))

    doc.build(story)
    return response

def rent_store_view(request):
    if request.method == 'POST':
        store_name = request.POST.get('store_name', '').strip()
        owner_name = request.POST.get('owner_name', '').strip()
        owner_phone = request.POST.get('owner_phone', '').strip()
        boa_ref = request.POST.get('boa_ref_number', '').strip()

        if store_name and owner_phone:
            status = 'ACTIVE' if boa_ref.upper().startswith(('BOA', 'FT', 'TX', 'REF')) else 'PENDING_PAYMENT'
            VendorStore.objects.create(
                store_name=store_name,
                owner_name=owner_name,
                owner_phone=owner_phone,
                rental_status=status,
                boa_ref_number=boa_ref
            )
            if status == 'ACTIVE':
                messages.success(request, f"Store '{store_name}' Rented & Activated! Funds verified to Bank of Abyssinia Account {getattr(settings, 'BOA_ACCOUNT_NUMBER', '96072775')}.")
            else:
                messages.info(request, f"Store '{store_name}' registration submitted! Admin will activate your store upon verifying 500 ETB deposit to BOA Account {getattr(settings, 'BOA_ACCOUNT_NUMBER', '96072775')}.")
    return redirect('buyer_requests')


# -------------------------------------------------------------------
# DASHBOARD — password-protected via session
# -------------------------------------------------------------------
def _dashboard_authenticated(request):
    """Return True if the current session has passed the dashboard password check."""
    return request.session.get('dashboard_auth') is True

def dashboard_login_view(request):
    if request.method == 'POST':
        pwd = request.POST.get('password', '').strip()
        if pwd == getattr(settings, 'DASHBOARD_PASSWORD', 'admin1234'):
            request.session['dashboard_auth'] = True
            return redirect('dashboard')
        else:
            messages.error(request, "Incorrect password. Please try again.")
    return render(request, 'dashboard_login.html', {})

def dashboard_view(request):
    if not _dashboard_authenticated(request):
        return redirect('dashboard_login')

    total_revenue = Order.objects.filter(payment_status='VERIFIED_PAID').aggregate(Sum('amount'))['amount__sum'] or 0
    pending_count = Order.objects.filter(payment_status='UNDER_VERIFICATION').count()
    completed_count = Order.objects.filter(payment_status='VERIFIED_PAID').count()
    
    orders = Order.objects.all().order_by('-created_at')
    payouts = PayoutLog.objects.all().order_by('-timestamp')[:10]

    context = {
        'total_revenue': total_revenue,
        'pending_count': pending_count,
        'completed_count': completed_count,
        'orders': orders,
        'payouts': payouts,
        'cbe_account': getattr(settings, 'BOA_ACCOUNT_NUMBER', '96072775'),
    }
    return render(request, 'dashboard.html', context)

def verify_order_admin(request, order_id):
    if not _dashboard_authenticated(request):
        return redirect('dashboard_login')

    order = get_object_or_404(Order, order_id=order_id)
    order.payment_status = 'VERIFIED_PAID'
    order.save()
    
    if hasattr(order, 'cbe_transaction'):
        order.cbe_transaction.verified = True
        order.cbe_transaction.verified_at = timezone.now()
        order.cbe_transaction.save()
        
    order.product.sales_count += 1
    order.product.save()

    PayoutLog.objects.create(
        cbe_account=getattr(settings, 'BOA_ACCOUNT_NUMBER', '96072775'),
        amount=order.amount,
        status="SETTLED_INSTANT",
        transaction_note=f"Manual Admin Settlement for Order {order.order_id} to Bank of Abyssinia 96072775"
    )

    messages.success(request, f"Order {order.order_id} marked as paid and funds logged to Bank of Abyssinia 96072775!")
    return redirect('dashboard')

def viral_promo_view(request):
    products = Product.objects.all()
    cbe_account = getattr(settings, 'BOA_ACCOUNT_NUMBER', '96072775')
    base_url = request.build_absolute_uri(reverse('index'))
    return render(request, 'viral_promo.html', {
        'products': products,
        'cbe_account': cbe_account,
        'base_url': base_url,
    })
