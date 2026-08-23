from django.db import models
import uuid

class Product(models.Model):
    CATEGORY_CHOICES = [
        ('prompts', 'AI & Business Prompts'),
        ('templates', 'Ethiopian Business & CV Templates'),
        ('guides', 'Zero-Capital Earning Guides'),
        ('software', 'Developer & Freelance Tools'),
    ]

    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)
    tagline = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2, help_text="Price in Ethiopian Birr (ETB)")
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, default='templates')
    content_delivery = models.TextField(help_text="Digital content, download link, or license key delivered upon verification")
    pdf_file = models.FileField(upload_to='pdfs/', blank=True, null=True, help_text="Direct downloadable PDF document file")
    sales_count = models.IntegerField(default=0)
    is_featured = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)


    def save(self, *args, **kwargs):
        if not self.slug:
            from django.utils.text import slugify
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name} - {self.price} ETB"

class Affiliate(models.Model):
    name = models.CharField(max_length=100)
    ref_code = models.CharField(max_length=50, unique=True)
    phone_or_bank = models.CharField(max_length=100, help_text="Bank of Abyssinia Account or Phone")
    total_commission_etb = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Affiliate {self.name} ({self.ref_code}) - {self.total_commission_etb} ETB Earned"

class Order(models.Model):
    STATUS_CHOICES = [
        ('PENDING_PAYMENT', 'Pending Payment'),
        ('UNDER_VERIFICATION', 'Verification Pending'),
        ('VERIFIED_PAID', 'Verified & Delivered'),
        ('CANCELLED', 'Cancelled'),
    ]

    order_id = models.CharField(max_length=50, unique=True, editable=False)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='orders')
    buyer_name = models.CharField(max_length=150)
    buyer_phone = models.CharField(max_length=20)
    buyer_email = models.EmailField(blank=True, null=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_status = models.CharField(max_length=30, choices=STATUS_CHOICES, default='PENDING_PAYMENT')
    cbe_ref_number = models.CharField(max_length=100, blank=True, null=True, help_text="Bank of Abyssinia Transaction Reference")
    affiliate_ref = models.ForeignKey(Affiliate, on_delete=models.SET_NULL, null=True, blank=True, related_name='orders')
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.order_id:
            self.order_id = f"SOL-{uuid.uuid4().hex[:8].upper()}"
        super().save(*args, **kwargs)

class VendorStore(models.Model):
    store_name = models.CharField(max_length=150)
    owner_name = models.CharField(max_length=100)
    owner_phone = models.CharField(max_length=20)
    rental_status = models.CharField(max_length=30, choices=[
        ('PENDING_PAYMENT', 'Pending BOA Payment'),
        ('ACTIVE', 'Active Store Rental'),
        ('EXPIRED', 'Expired'),
    ], default='PENDING_PAYMENT')
    rental_fee_etb = models.DecimalField(max_digits=10, decimal_places=2, default=500.00, help_text="Store Rental Fee per month")
    boa_ref_number = models.CharField(max_length=100, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Store: {self.store_name} ({self.owner_phone}) - {self.rental_status}"

class BuyerProductRequest(models.Model):
    STATUS_CHOICES = [
        ('OPEN', 'Open for Seller Offers'),
        ('ACCEPTED', 'Seller Offer Accepted'),
        ('COMPLETED', 'Fulfilled via Phone/BOA'),
    ]

    buyer_name = models.CharField(max_length=150)
    buyer_phone = models.CharField(max_length=20)
    product_title = models.CharField(max_length=200)
    description = models.TextField(help_text="Details of what the buyer wants to purchase or get delivered")
    budget_etb = models.DecimalField(max_digits=10, decimal_places=2, help_text="Max budget in ETB")
    delivery_phone = models.CharField(max_length=20, help_text="Phone number for direct phone delivery")
    status = models.CharField(max_length=30, choices=STATUS_CHOICES, default='OPEN')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Request: {self.product_title} by {self.buyer_name} ({self.budget_etb} ETB)"

class SellerOffer(models.Model):
    request = models.ForeignKey(BuyerProductRequest, on_delete=models.CASCADE, related_name='seller_offers')
    seller_name = models.CharField(max_length=150)
    seller_phone = models.CharField(max_length=20)
    offer_price_etb = models.DecimalField(max_digits=10, decimal_places=2)
    delivery_notes = models.TextField(help_text="Phone delivery instructions or download link")
    accepted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Offer by {self.seller_name} for {self.request.product_title} ({self.offer_price_etb} ETB)"


