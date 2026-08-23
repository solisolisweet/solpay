import os
from pathlib import Path
from django.core.management.base import BaseCommand
from django.conf import settings
from marketplace.models import Product, Order
from payments.models import PayoutLog
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle

class Command(BaseCommand):
    help = 'Seeds complete digital products with generated downloadable PDF e-books and Ethiopian Tax Excel tool'

    def generate_pdf(self, filename, title, author, content_text):
        media_pdf_dir = settings.MEDIA_ROOT / 'pdfs'
        media_pdf_dir.mkdir(parents=True, exist_ok=True)
        pdf_path = media_pdf_dir / filename

        doc = SimpleDocTemplate(str(pdf_path), pagesize=letter)
        styles = getSampleStyleSheet()
        
        title_style = ParagraphStyle(
            'TitleStyle',
            parent=styles['Heading1'],
            fontSize=18,
            leading=22,
            textColor='#1e3a8a',
            spaceAfter=12
        )
        
        author_style = ParagraphStyle(
            'AuthorStyle',
            parent=styles['Italic'],
            fontSize=10,
            leading=14,
            textColor='#4b5563',
            spaceAfter=20
        )
        
        body_style = ParagraphStyle(
            'BodyStyle',
            parent=styles['Normal'],
            fontSize=10,
            leading=14,
            textColor='#1f2937',
            spaceAfter=10
        )

        story = [
            Paragraph(title, title_style),
            Paragraph(f"Author: {author} | Bank of Abyssinia Account 96072775 Settlement Verified", author_style),
            Spacer(1, 10),
        ]

        for paragraph in content_text.split('\n\n'):
            clean_p = paragraph.replace('\n', '<br/>')
            story.append(Paragraph(clean_p, body_style))
            story.append(Spacer(1, 8))

        doc.build(story)
        return f"pdfs/{filename}"

    def handle(self, *args, **options):
        products_data = [
            {
                'name': 'Ethiopian Tax, Pension & Net Salary Excel Automation Tool',
                'filename': 'ethiopian_tax_pension_excel_calculator.pdf',
                'tagline': 'Automated tax bracket formula & salary breakdown updated for Ethiopian income tax rules.',
                'description': 'Easily calculate monthly net pay, employee pension (7%), employer pension (11%), and income tax brackets for Ethiopian businesses, freelancers, and payroll management.',
                'price': 150.00,
                'category': 'software',
                'is_featured': True,
                'content_text': """ETHIOPIAN INCOME TAX & PAYROLL CALCULATOR FORMULA GUIDE

OFFICIAL ETHIOPIAN INCOME TAX BRACKETS (MONTHLY SALARY IN ETB):
1. 0 - 600 ETB: 0% Tax (Exempt)
2. 601 - 1,650 ETB: 10% Tax (Deduction: 60 ETB)
3. 1,651 - 3,200 ETB: 15% Tax (Deduction: 142.50 ETB)
4. 3,201 - 5,250 ETB: 20% Tax (Deduction: 302.50 ETB)
5. 5,251 - 7,800 ETB: 25% Tax (Deduction: 565.00 ETB)
6. 7,801 - 10,900 ETB: 30% Tax (Deduction: 955.00 ETB)
7. Over 10,900 ETB: 35% Tax (Deduction: 1,500.00 ETB)

PENSION CONTRIBUTION RATES:
- Employee Pension Contribution: 7% of basic salary
- Employer Pension Contribution: 11% of basic salary

EXCEL FORMULA FOR NET SALARY:
Net Salary = Basic Salary - (Gross Salary * Tax Rate - Deduction) - (Basic Salary * 7%)

EXCEL AUTOMATION TEMPLATE STRUCTURE:
Column A: Employee Name
Column B: Basic Salary
Column C: Allowance (Transport/Hardship)
Column D: Gross Salary = B + C
Column E: Employee Pension (7%) = B * 0.07
Column F: Income Tax = VLOOKUP/IF Bracket Formula
Column G: Net Payable Salary = D - E - F

FORMULA UNLOCK KEY: SOL-TAX-SPREADSHEET-2026
Direct Settlement: Bank of Abyssinia Account 96072775"""
            },
            {
                'name': 'The Complete Shopify E-Commerce & Affiliate Marketing Blueprint (2026 Edition)',
                'filename': 'shopify_affiliate_blueprint_2026.pdf',
                'tagline': 'Master Shopify store creation, dropshipping, affiliate funnels, and high-converting store setups.',
                'description': 'A comprehensive master e-book covering everything you need to know about setting up a profitable Shopify store, integrating affiliate marketing links, sourcing high-converting products, running zero-budget traffic campaigns, and automating sales.',
                'price': 350.00,
                'category': 'guides',
                'is_featured': True,
                'content_text': """CHAPTER 1: INTRODUCTION TO E-COMMERCE & AFFILIATE MARKETING
E-Commerce and Affiliate Marketing are two of the most scalable online business models.
- E-Commerce: Selling digital products, services, or physical items directly to buyers.
- Affiliate Marketing: Promoting third-party products and earning a commission (10% to 75%) on every purchase made through your custom referral link.

CHAPTER 2: SETTING UP YOUR SHOPIFY STORE
Step 1: Sign up for a Shopify trial account.
Step 2: Choose a modern theme (Sense, Dawn, or Spotlight).
Step 3: Customize your homepage layout with clear headlines, high-resolution product mockups, and bold Buy Now buttons.
Step 4: Create collections (Digital Downloads, Trending Products, Recommended Tools).
Step 5: Install essential free apps (Digital Downloads app, PageFly builder, Telegram share widget).

CHAPTER 3: FINDING HIGH-MARGIN PRODUCTS
1. Digital Products (100% Profit Margin): E-books, templates, prompt packs, courses, spreadsheets.
2. Affiliate Offers: Amazon Associates, ClickBank, Digistore24, CJ Affiliate, local Ethiopian affiliate offers.

CHAPTER 4: ZERO-BUDGET TRAFFIC FUNNEL
- Telegram Channels: Build a niche Telegram channel, share valuable free tips daily, and attach store/affiliate links.
- WhatsApp Groups: Share short direct solutions and link to your store.
- Bank of Abyssinia Settlement: Configure target account 96072775 for direct mobile transfers."""
            },
            {
                'name': 'The Ultimate Affiliate Marketing Vault & Secret Funnel Secrets',
                'filename': 'ultimate_affiliate_marketing_vault.pdf',
                'tagline': 'Complete step-by-step guide to generating recurring affiliate income with $0 ad budget.',
                'description': 'Discover secret affiliate strategies used by top online marketers. Learn how to promote software, digital tools, e-books, and global affiliate offers using free social traffic.',
                'price': 290.00,
                'category': 'guides',
                'is_featured': True,
                'content_text': """CORE STRATEGY OVERVIEW:
Affiliate marketing pays you commissions for sending buyers to products.

HIGH-PAYING AFFILIATE NETWORKS:
1. Digistore24 (Pays up to 85% commission per sale)
2. ClickBank (Digital courses & tools)
3. Amazon Associates (Physical products)

HOW TO BUILD A 100% FREE VIRAL TRAFFIC ENGINE:
Step 1: Pick a specific niche (Business, AI, Health, Coding, Finance).
Step 2: Create a Telegram channel or TikTok account focused on that niche.
Step 3: Post 1 piece of helpful content daily.
Step 4: Place your custom affiliate link or store page in the channel description."""
            },
            {
                'name': 'Master AI & ChatGPT Business Prompt Suite 2026',
                'filename': 'master_ai_chatgpt_prompt_suite_2026.pdf',
                'tagline': '1,500+ battle-tested AI prompts for copywriting, automated marketing, and coding.',
                'description': 'Unlock maximum productivity with curated prompts designed for ChatGPT, Claude, and Gemini. Includes business proposal generators, social media content calendars, and automated customer support templates.',
                'price': 250.00,
                'category': 'prompts',
                'is_featured': True,
                'content_text': """SECTION 1: COPYWRITING & SALES PROMPTS
Prompt 1: Write a high-converting sales page headline and 5 bullet points for a product named [PRODUCT_NAME] that solves [PROBLEM].
Prompt 2: Draft an engaging 3-part email welcome sequence for subscribers interested in [TOPIC].

SECTION 2: SOCIAL MEDIA VIRAL POST PROMPTS
Prompt 3: Give me 10 viral video script hooks for TikTok under 30 seconds about [TOPIC].
Prompt 4: Create a 7-day Telegram content calendar with call-to-actions for [STORE_LINK]."""
            },
            {
                'name': 'Ethiopian Freelance & Business Contract Kit',
                'filename': 'ethiopian_freelance_legal_contract_kit.pdf',
                'tagline': 'Legally sound proposal, contract, and invoice templates for Ethiopian creators.',
                'description': 'Ready-to-use legal agreement templates tailored for freelance work, web design, consulting, and software development. Protect your work and get paid faster.',
                'price': 350.00,
                'category': 'templates',
                'is_featured': True,
                'content_text': """STANDARD FREELANCE SERVICE AGREEMENT TEMPLATE:

This Service Agreement (Agreement) is made between:
Provider: [YOUR NAME / BUSINESS NAME]
Client: [CLIENT NAME]

1. SERVICES: The Provider agrees to perform work on [PROJECT TITLE].
2. PAYMENT TERMS: 50% advance payment prior to project start, remaining 50% due upon project delivery to Bank of Abyssinia Account 96072775.
3. INTELLECTUAL PROPERTY: All final deliverables belong to Client upon full settlement."""
            }
        ]

        count = 0
        for data in products_data:
            pdf_rel_path = self.generate_pdf(
                filename=data['filename'],
                title=data['name'],
                author='SolPay Digital Publishing',
                content_text=data['content_text']
            )

            product, created = Product.objects.update_or_create(
                name=data['name'],
                defaults={
                    'tagline': data['tagline'],
                    'description': data['description'],
                    'price': data['price'],
                    'category': data['category'],
                    'is_featured': True,
                    'content_delivery': data['content_text'],
                    'pdf_file': pdf_rel_path
                }
            )
            count += 1

        self.stdout.write(self.style.SUCCESS(f'Successfully seeded {count} products with downloadable PDF files!'))
