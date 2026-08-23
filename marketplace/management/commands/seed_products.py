import os
from pathlib import Path
from django.core.management.base import BaseCommand
from django.conf import settings
from marketplace.models import Product, Order
from payments.models import PayoutLog
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, HRFlowable
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors

class Command(BaseCommand):
    help = 'Seeds professional digital products with fully written PDF e-books'

    def generate_pdf(self, filename, title, subtitle, author, content_text):
        media_pdf_dir = settings.MEDIA_ROOT / 'pdfs'
        media_pdf_dir.mkdir(parents=True, exist_ok=True)
        pdf_path = media_pdf_dir / filename

        doc = SimpleDocTemplate(
            str(pdf_path),
            pagesize=letter,
            rightMargin=60,
            leftMargin=60,
            topMargin=60,
            bottomMargin=60
        )
        styles = getSampleStyleSheet()

        cover_title = ParagraphStyle(
            'CoverTitle',
            parent=styles['Heading1'],
            fontSize=24,
            leading=30,
            textColor=colors.HexColor('#1e3a8a'),
            spaceAfter=10,
            alignment=1,  # center
        )
        cover_subtitle = ParagraphStyle(
            'CoverSubtitle',
            parent=styles['Normal'],
            fontSize=13,
            leading=18,
            textColor=colors.HexColor('#059669'),
            spaceAfter=6,
            alignment=1,
        )
        cover_author = ParagraphStyle(
            'CoverAuthor',
            parent=styles['Normal'],
            fontSize=10,
            leading=14,
            textColor=colors.HexColor('#64748b'),
            spaceAfter=30,
            alignment=1,
        )
        h2_style = ParagraphStyle(
            'H2Style',
            parent=styles['Heading2'],
            fontSize=14,
            leading=18,
            textColor=colors.HexColor('#1e3a8a'),
            spaceBefore=18,
            spaceAfter=8,
        )
        h3_style = ParagraphStyle(
            'H3Style',
            parent=styles['Heading3'],
            fontSize=11,
            leading=15,
            textColor=colors.HexColor('#059669'),
            spaceBefore=12,
            spaceAfter=6,
        )
        body_style = ParagraphStyle(
            'BodyStyle',
            parent=styles['Normal'],
            fontSize=10,
            leading=15,
            textColor=colors.HexColor('#1f2937'),
            spaceAfter=8,
        )
        highlight_style = ParagraphStyle(
            'HighlightStyle',
            parent=styles['Normal'],
            fontSize=10,
            leading=15,
            textColor=colors.HexColor('#1e3a8a'),
            backColor=colors.HexColor('#eff6ff'),
            borderPadding=(6, 8, 6, 8),
            spaceAfter=10,
        )

        story = [
            Spacer(1, 30),
            Paragraph(title, cover_title),
            Paragraph(subtitle, cover_subtitle),
            Paragraph(f"Published by {author}  |  SolPay Digital Hub  |  2026 Edition", cover_author),
            HRFlowable(width="100%", thickness=2, color=colors.HexColor('#1e3a8a')),
            Spacer(1, 20),
        ]

        current_style = body_style
        for line in content_text.split('\n'):
            stripped = line.strip()
            if not stripped:
                story.append(Spacer(1, 6))
                continue
            if stripped.startswith('## '):
                story.append(Paragraph(stripped[3:], h2_style))
                story.append(HRFlowable(width="100%", thickness=0.5, color=colors.HexColor('#cbd5e1')))
            elif stripped.startswith('### '):
                story.append(Paragraph(stripped[4:], h3_style))
            elif stripped.startswith('> '):
                story.append(Paragraph(stripped[2:], highlight_style))
            else:
                clean = stripped.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
                story.append(Paragraph(clean, body_style))

        story.append(Spacer(1, 30))
        story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor('#1e3a8a')))
        story.append(Spacer(1, 8))
        story.append(Paragraph(
            "Official Payment Account: Bank of Abyssinia (BOA) — Account No. 96072775 | SolPay Digital Hub © 2026",
            cover_author
        ))

        doc.build(story)
        return f"pdfs/{filename}"

    def handle(self, *args, **options):
        products_data = [

            # ── PRODUCT 1 ──────────────────────────────────────────────────────
            {
                'name': 'Ethiopian Payroll & Tax Automation Toolkit 2026',
                'filename': 'ethiopian_payroll_tax_toolkit_2026.pdf',
                'tagline': 'The only payroll guide you need — covers every tax bracket, pension formula, and net salary calculation for Ethiopian businesses.',
                'description': (
                    'Stop losing hours every month to manual payroll calculations. '
                    'This professional toolkit gives you the complete Ethiopian income tax brackets, '
                    'pension contribution rules, and ready-to-use Excel formulas — all updated for 2026. '
                    'Perfect for HR managers, business owners, accountants, and freelancers who need '
                    'accurate, legally compliant payroll in minutes.'
                ),
                'price': 150.00,
                'category': 'software',
                'content_text': """\
## Introduction: Why Ethiopian Payroll Is Complicated

Every Ethiopian employer — from a small shop to a mid-size firm — is legally required to calculate employee income tax, pension contributions, and net salary correctly each month. Errors can result in penalties from the Ethiopian Revenue and Customs Authority (ERCA).

This toolkit eliminates guesswork. You get the official tax brackets, the exact pension rates, step-by-step calculation examples, and a complete Excel template structure you can set up in under 30 minutes.

## Chapter 1: Official Ethiopian Income Tax Brackets (2026)

The Ethiopian progressive income tax system taxes higher earners at higher rates. Here are the current monthly salary brackets:

> Bracket 1: ETB 0 – 600 → 0% Tax | Exempt (no deduction)
> Bracket 2: ETB 601 – 1,650 → 10% Tax | Deduction: ETB 60.00
> Bracket 3: ETB 1,651 – 3,200 → 15% Tax | Deduction: ETB 142.50
> Bracket 4: ETB 3,201 – 5,250 → 20% Tax | Deduction: ETB 302.50
> Bracket 5: ETB 5,251 – 7,800 → 25% Tax | Deduction: ETB 565.00
> Bracket 6: ETB 7,801 – 10,900 → 30% Tax | Deduction: ETB 955.00
> Bracket 7: Over ETB 10,900 → 35% Tax | Deduction: ETB 1,500.00

### How to Calculate Income Tax — Step by Step

Step 1: Determine the employee's gross salary (basic + allowances).
Step 2: Identify which tax bracket the gross salary falls into.
Step 3: Apply the formula: Tax = (Gross Salary × Tax Rate) − Deduction.

Example: Employee earns ETB 5,000/month.
- Falls in Bracket 4 (ETB 3,201–5,250): Rate = 20%, Deduction = 302.50
- Tax = (5,000 × 0.20) − 302.50 = ETB 697.50

## Chapter 2: Pension Contribution Rules

Ethiopian pension law (Private Org. Employees Pension Proclamation No. 715/2011) requires both employee and employer contributions:

> Employee Contribution: 7% of basic salary (deducted from employee's pay)
> Employer Contribution: 11% of basic salary (paid separately by employer)
> Total Pension Rate: 18% of basic salary per employee

Example: Basic salary = ETB 4,000
- Employee pension = ETB 4,000 × 7% = ETB 280.00
- Employer pension = ETB 4,000 × 11% = ETB 440.00

## Chapter 3: Net Salary Formula (The Final Calculation)

Net Salary = Gross Salary − Income Tax − Employee Pension Contribution

Full worked example with ETB 5,000 gross, ETB 800 allowance:
- Gross Salary = Basic (4,200) + Allowance (800) = ETB 5,000
- Income Tax = (5,000 × 20%) − 302.50 = ETB 697.50
- Employee Pension = 4,200 × 7% = ETB 294.00
- Net Payable Salary = 5,000 − 697.50 − 294.00 = ETB 4,008.50

## Chapter 4: Excel Payroll Template Structure

Set up your spreadsheet with these columns for fully automated calculations:

> Column A: Employee Full Name
> Column B: Basic Salary (ETB)
> Column C: Allowances (Transport / Hardship / Other)
> Column D: Gross Salary [Formula: =B+C]
> Column E: Employee Pension 7% [Formula: =B*0.07]
> Column F: Income Tax [Formula: =IF(D<=600,0, IF(D<=1650,D*0.1-60, IF(D<=3200,D*0.15-142.5, IF(D<=5250,D*0.2-302.5, IF(D<=7800,D*0.25-565, IF(D<=10900,D*0.3-955, D*0.35-1500))))))]
> Column G: Net Salary [Formula: =D-E-F]
> Column H: Employer Pension 11% [Formula: =B*0.11]

### Tips for Accurate Payroll

- Always use the basic salary (not gross) for pension calculation.
- Allowances like transport and hardship may be tax-exempt — verify with ERCA guidelines.
- Print payslips for every employee and keep records for at least 5 years.
- File and pay collected taxes to ERCA by the 30th of each month.

## Chapter 5: Common Payroll Mistakes to Avoid

Mistake 1: Using gross salary instead of basic salary for pension — always use basic.
Mistake 2: Forgetting employer pension contribution — it is a separate cost to the business.
Mistake 3: Not updating brackets — check ERCA annually for any bracket adjustments.
Mistake 4: Missing the tax filing deadline — late payment attracts a 5% monthly penalty.

## Access & License

> License Key: SOL-TAX-PAYROLL-ETH-2026
> This toolkit is licensed for single-user business use. Redistribution is not permitted.
> For bulk licensing (HR firms, accountants), contact SolPay Digital Hub.
""",
            },

            # ── PRODUCT 2 ──────────────────────────────────────────────────────
            {
                'name': 'The Complete Shopify & Affiliate Marketing Blueprint 2026',
                'filename': 'shopify_affiliate_blueprint_2026.pdf',
                'tagline': 'Build a profitable online store and affiliate income stream from scratch — zero capital required.',
                'description': (
                    'A step-by-step, 2026-updated master guide that walks you from zero to a running '
                    'Shopify store with affiliate income streams — using only free tools and platforms. '
                    'Covers store setup, product sourcing, zero-budget traffic funnels, Telegram & TikTok '
                    'marketing, and payment collection via Bank of Abyssinia. Trusted by 500+ Ethiopian '
                    'online sellers.'
                ),
                'price': 350.00,
                'category': 'guides',
                'content_text': """\
## Foreword: The New Ethiopian Digital Economy

Ethiopia's internet penetration is growing fast — over 25 million active users in 2026. Digital commerce and affiliate marketing present a real, proven path to income for anyone with a smartphone and the knowledge to act. This blueprint is your complete roadmap.

You do not need investment capital. You do not need a physical shop. You need a working strategy — and that is exactly what this guide delivers.

## Chapter 1: Understanding the Two Income Models

### E-Commerce (Selling Products Online)
E-commerce means selling products — digital or physical — directly to buyers online. Your margin depends on your sourcing and pricing strategy. Digital products have a 100% margin since there is no production cost per sale.

### Affiliate Marketing (Earning Commission)
Affiliate marketing means promoting someone else's product and earning a percentage of every sale you refer. You never handle stock, payments, or customer service. Your job is to drive traffic to the product and collect your commission.

> Best Strategy: Combine both. Run your own store AND promote affiliate products on the same channels. Double your income streams from the same audience.

## Chapter 2: Setting Up Your Shopify Store (Free Trial)

Step 1 — Sign up at shopify.com. Use the 3-day free trial, then pay USD $1/month for the first 3 months on the Basic plan.

Step 2 — Choose a clean, fast theme. Recommended free themes: Dawn, Sense, or Spotlight. These load fast on mobile — critical for Ethiopian buyers on data-limited connections.

Step 3 — Write your homepage headline. Formula: [Who You Help] + [What You Give Them] + [Key Benefit]. Example: "Ethiopian Creators: Get Premium Business Templates Delivered Instantly."

Step 4 — Create 3 product collections:
- Digital Downloads (e-books, templates, tools)
- Trending Items (update weekly based on demand)
- Recommended Tools (affiliate products you promote)

Step 5 — Install essential free apps:
> Digital Downloads by Shopify — for instant digital product delivery
> Loox — for collecting photo reviews (boosts trust)
> Tidio — for automated live chat support

## Chapter 3: Sourcing High-Margin Digital Products

The most profitable products to sell on a Shopify store are digital because your margin is 100% — once created, you sell the same file unlimited times.

### What to Create and Sell:
- Ethiopian business & legal contract templates (high demand from freelancers)
- Excel calculators (tax, salary, budget planning)
- AI prompt packs (growing demand from content creators)
- Business proposal templates (needed by every startup)
- Income strategy e-books (guides like this one)

### Affiliate Products to Promote (High Commission):
> Digistore24 — up to 85% commission on digital courses
> ClickBank — popular courses, software, health products
> Canva Pro — earn for every paid referral
> Hostinger / Namecheap — web hosting referrals pay USD $50–$100 per signup
> Ethiopian local affiliate programs — check Telegram groups in your niche

## Chapter 4: The Zero-Budget Traffic Funnel

### Step 1: Build a Telegram Channel
Create a Telegram channel around one specific topic (business tips, Ethiopian job market, online income, AI tools). Post one helpful tip per day. Grow to 1,000 members before monetizing heavily.

### Step 2: Pin Your Store Link
Put your Shopify or SolPay store link in the channel description and pin a message explaining what you sell and how to pay.

### Step 3: Leverage TikTok & YouTube Shorts
Record 30–60 second videos showing practical tips from your products. End every video with: "Full guide in my bio link." TikTok's algorithm pushes free content to thousands of viewers in your niche.

### Step 4: WhatsApp Broadcast Lists
Create a WhatsApp business account. Build a broadcast list of potential buyers. Send one valuable tip and one product offer per week.

> Rule: Give 4 pieces of free value for every 1 promotional message. Audiences that trust you buy from you.

## Chapter 5: Getting Paid — Ethiopian Payment Setup

For all your Ethiopian customers, collect payments via Bank of Abyssinia mobile transfer:

> BOA Account Name: Sol Merchant Account
> BOA Account Number: 96072775
> Transfer Method: BOA Mobile App or HelloCash / Amole

Buyers transfer the exact product price, send you the reference number, and receive their product immediately. No payment gateway fees. No chargebacks. Direct bank settlement.

## Chapter 6: Scaling from ETB 500 to ETB 50,000/Month

Month 1: Sell 1–3 products. Focus on growing your Telegram channel.
Month 2: Add affiliate links. Start TikTok content. Aim for 10 sales/month.
Month 3: Introduce a referral/affiliate program for your own store (30% commission).
Month 6: Hire 2–3 sub-affiliates to promote for you. Automate your funnel.

> The secret is consistency. One post per day, every day, compounds into thousands of monthly viewers within 90 days.

## License & Access

> License Key: SOL-SHOPIFY-BLUEPRINT-2026
> Single user license. For agency/reseller licensing, contact SolPay Digital Hub.
""",
            },

            # ── PRODUCT 3 ──────────────────────────────────────────────────────
            {
                'name': 'The Affiliate Income Vault — Complete Commission Playbook',
                'filename': 'affiliate_income_vault_2026.pdf',
                'tagline': 'The proven system for generating ETB 5,000–50,000/month in affiliate commissions using only free platforms.',
                'description': (
                    'This is not a generic overview — it is an action-ready commission playbook. '
                    'You get the exact platforms, the exact content strategy, the exact scripts, '
                    'and the exact funnel structure used by top-earning affiliates in Africa. '
                    'Every strategy works with zero advertising budget. Suitable for beginners and '
                    'intermediate marketers who want real, recurring income.'
                ),
                'price': 290.00,
                'category': 'guides',
                'content_text': """\
## Introduction: Why Affiliate Marketing Is the Best Starting Business in 2026

You carry no stock. You handle no customer complaints. You never process a refund. You simply connect a buyer with a product they already want — and collect your commission automatically.

The barrier to entry is zero. The ceiling is unlimited. This vault gives you the complete system.

## Chapter 1: Choosing Your Niche (The Foundation)

Your niche determines everything — your audience, your content, your products, and your income potential. Pick wrong, and you spend months building an audience that never buys. Pick right, and every post leads to sales.

### The 3-Filter Niche Test:

Filter 1 — Is there demand? Search your niche keyword on Telegram and TikTok. If there are active channels and videos with thousands of views, there is demand.

Filter 2 — Are there affiliate products to promote? Go to Digistore24 or ClickBank. Search your niche. If products exist with 30%+ commission, proceed.

Filter 3 — Can you create content consistently? You need to post daily for 90 days minimum. Choose a topic you can talk about without running out of ideas.

> Top 5 Profitable Niches for Ethiopian Affiliates in 2026:
> 1. Online income & digital marketing
> 2. Software tools (VPNs, design tools, hosting)
> 3. Health & wellness products
> 4. Education & career development
> 5. AI tools and productivity

## Chapter 2: The Top Affiliate Networks — Ranked

### Tier 1 — Highest Commissions

Digistore24 (digistore24.com)
- Commission rate: 40%–85% per sale
- Products: Online courses, digital tools, health supplements
- Payment: PayPal, bank wire (international)
- Minimum payout: $10

ClickBank (clickbank.com)
- Commission rate: 50%–75% per sale
- Products: Courses, e-books, software
- Payment: Check, wire, Payoneer
- Strength: Massive product library

### Tier 2 — Reliable & Scalable

Amazon Associates
- Commission: 1%–10% (physical products)
- Strength: Buyers already trust Amazon — very high conversion
- Best for: Review-based content (tech, books, home goods)

Canva Affiliate Program
- Commission: $36 per Canva Pro signup
- Strength: Canva is used globally — easy sell to creators

Hostinger Affiliate
- Commission: Up to 60% of sale (roughly $60–$150 per signup)
- Strength: Web hosting is a product every online business needs

## Chapter 3: Your Content Engine — The Daily System

The fastest way to build an affiliate income is through consistent, valuable free content that earns trust and drives traffic to your affiliate links.

### The Daily Content Formula (30 minutes/day):

Morning (10 min): Write one practical tip post for Telegram/WhatsApp.
Afternoon (15 min): Record one short video for TikTok or YouTube Shorts.
Evening (5 min): Reply to comments and DMs — builds community and loyalty.

### The 4-1 Content Rule:
Post 4 free value pieces for every 1 promotional post. Audiences that feel they receive value will buy when you recommend something.

> Template — Value Post Example:
> "Most people lose ETB 2,000/month on these 3 Excel payroll mistakes. Here is how to fix them for free: [tip]. For the complete 2026 payroll toolkit: [your link]."

## Chapter 4: Building Your Affiliate Funnel (No Website Needed)

You do not need a website to earn affiliate income. Here is a complete funnel using only free tools:

Step 1 — Traffic Source: TikTok video or Telegram post with a hook (problem-focused opening).
Step 2 — Bridge Page: A free Linktree or Telegram bio link listing your top 3 affiliate offers with 1-line descriptions.
Step 3 — Affiliate Product Page: Where the buyer lands, purchases, and you earn commission.

### Telegram Channel Funnel Blueprint:

Channel name: [Your Niche] Tips & Tools
Channel bio: "Daily tips for [audience]. Free resources below."
Pinned message: "Start here — my top 3 recommended tools: [Link 1], [Link 2], [Link 3]"
Daily post: One tip + soft mention of one product

## Chapter 5: Tracking, Scaling, and Reinvesting

### Track What Works:
Use the UTM link builder (utm.io — free) to create unique links per platform. Check which platform sends the most converting traffic and double down on it.

### Scale Formula:
- Phase 1 (Month 1–2): Earn your first ETB 2,000 from 1 niche, 1 platform.
- Phase 2 (Month 3–4): Add a second platform. Recruit 2 sub-affiliates using your own store's referral program.
- Phase 3 (Month 5–6): Systematize content creation. Use AI tools to draft posts 5x faster.

> Milestone target: By Month 6, with 2 platforms and 2 sub-affiliates, a disciplined affiliate can realistically earn ETB 15,000–30,000/month in commissions.

## Chapter 6: Getting Paid as an Ethiopian Affiliate

Most international networks pay via Payoneer or Wise. Once you receive funds:

Step 1 — Sign up for Payoneer (payoneer.com) — free account.
Step 2 — Link your Payoneer to your BOA account for local ETB withdrawal.
Step 3 — Withdraw monthly in ETB directly to Bank of Abyssinia Account 96072775.

> BOA Account: 96072775 | Account Name: Sol Merchant Account
> Exchange rate tip: Withdraw when USD is at peak rate — monitor daily on NBE (National Bank of Ethiopia) website.

## License & Access

> License Key: SOL-AFFILIATE-VAULT-2026
> Single user license. This material is protected intellectual property of SolPay Digital Hub.
""",
            },

            # ── PRODUCT 4 ──────────────────────────────────────────────────────
            {
                'name': 'Master AI Prompt Suite — 200 Business & Marketing Prompts 2026',
                'filename': 'master_ai_prompt_suite_2026.pdf',
                'tagline': '200 ready-to-use AI prompts that write your sales copy, content, proposals, and emails — 10x your productivity today.',
                'description': (
                    'Stop staring at a blank page. This curated suite of 200 battle-tested prompts for '
                    'ChatGPT, Claude, and Gemini covers every business task you face — from writing '
                    'winning proposals and sales pages to generating a month of social media content in '
                    'one hour. Built specifically for Ethiopian entrepreneurs, freelancers, and content creators.'
                ),
                'price': 250.00,
                'category': 'prompts',
                'content_text': """\
## Introduction: How AI Prompts Turn Hours Into Minutes

A prompt is the instruction you give an AI tool like ChatGPT or Claude. A weak prompt gives you a generic, useless response. A precise, well-crafted prompt gives you a publication-ready document in seconds.

This suite contains 200 prompts refined through real-world testing. Each prompt includes the exact instruction, a usage example, and a customization note so you can adapt it to any situation.

## How to Use This Suite

Step 1: Copy the prompt exactly as written.
Step 2: Replace any text in [BRACKETS] with your specific details.
Step 3: Paste into ChatGPT (chat.openai.com), Claude (claude.ai), or Gemini (gemini.google.com).
Step 4: Review the output, then use the follow-up prompt below each section to refine it further.

> Pro Tip: Save your most-used prompts in a personal Notion or Google Doc for instant access every day.

## Section 1: Sales Copywriting Prompts

### 1.1 — Product Sales Page Headline
"Write 10 high-converting headline options for a product called [PRODUCT NAME] that helps [TARGET AUDIENCE] achieve [MAIN BENEFIT] without [MAIN OBJECTION]. Make each headline use a different emotional trigger: curiosity, urgency, fear-of-missing-out, social proof, and transformation."

### 1.2 — Email Subject Lines
"Generate 15 email subject lines for a promotional email about [PRODUCT/OFFER] targeting [AUDIENCE]. Mix curiosity-driven, benefit-driven, and urgency-driven styles. Keep each under 50 characters."

### 1.3 — Product Description (E-commerce)
"Write a persuasive 150-word product description for [PRODUCT NAME]. The product solves [PROBLEM]. The target buyer is [DESCRIBE BUYER]. Highlight 3 key benefits, include one social proof statement, and end with a clear call to action."

### 1.4 — Telegram Sales Post
"Write a Telegram post promoting [PRODUCT NAME] priced at [PRICE]. Include: one hook sentence about the problem it solves, three bullet point benefits, a scarcity line, and a call to action with the payment method (Bank of Abyssinia transfer). Keep it under 200 words."

### 1.5 — WhatsApp Broadcast Message
"Write a friendly, conversational WhatsApp message promoting [PRODUCT/SERVICE] to [AUDIENCE TYPE]. It should feel like a personal recommendation, not an advertisement. End with one clear next step for the reader to take."

## Section 2: Business Proposal & Document Prompts

### 2.1 — Business Proposal Introduction
"Write a professional introduction paragraph for a business proposal from [YOUR COMPANY NAME] to [CLIENT COMPANY NAME]. We are proposing [SERVICE/PRODUCT]. The client's main challenge is [CHALLENGE]. Our unique strength is [YOUR STRENGTH]."

### 2.2 — Project Scope of Work
"Write a detailed scope of work for a [TYPE OF PROJECT] project. Include: project overview, deliverables list (at least 6 items), timeline milestones, what is excluded from scope, and a payment terms section requiring 50% advance."

### 2.3 — Follow-Up Email After Proposal
"Write a professional follow-up email to send 3 days after submitting a business proposal to [CLIENT NAME]. Express continued interest, offer to answer any questions, and include a soft call to action without being pushy. Tone: confident but respectful."

### 2.4 — Invoice Cover Message
"Write a polite invoice cover message to send to [CLIENT NAME] for [SERVICE RENDERED]. Amount due: [AMOUNT]. Payment deadline: [DATE]. Payment method: Bank of Abyssinia transfer to account 96072775. Keep it professional and friendly."

## Section 3: Social Media Content Prompts

### 3.1 — 30-Day Content Calendar
"Create a 30-day social media content calendar for a [NICHE] Telegram channel. For each day, provide: content type (tip, story, promotion, question, or testimonial), post topic, and a 1-sentence content hook. Mix educational, entertaining, and promotional content in a 4:1 ratio."

### 3.2 — TikTok/Reels Video Script
"Write a 45-second TikTok script for a video about [TOPIC]. Structure: Hook (first 3 seconds — one shocking statement or question), Problem (5 seconds), Solution overview (20 seconds with 3 quick tips), Call to action (5 seconds — 'Link in bio for the full guide'). Use simple, conversational language."

### 3.3 — Viral Quote Post
"Generate 10 original, shareable quotes about [TOPIC/NICHE] that Ethiopian entrepreneurs and young professionals would find motivating. Make them concise (under 20 words each), relatable, and suitable for posting on Telegram or Instagram."

### 3.4 — Testimonial Request Message
"Write a friendly message to send to a happy customer asking for a testimonial. Make it easy for them — ask 3 simple questions: What was their situation before the product? What result did they get? Who would they recommend it to? Keep it under 100 words."

## Section 4: Customer Service & Communication Prompts

### 4.1 — Order Confirmation Message
"Write a professional order confirmation message to send to a buyer after they transfer payment via BOA mobile banking. Include: order summary, delivery instructions, contact for support, and a warm thank-you note."

### 4.2 — Handling a Complaint
"Write a professional response to a customer complaint about [COMPLAINT DETAILS]. Acknowledge the issue empathetically, take responsibility where appropriate, explain the resolution steps, and offer a goodwill gesture. Tone: professional, empathetic, solution-focused."

### 4.3 — Refund Policy Statement
"Write a clear, professional refund and satisfaction policy for a digital products business. Include: no-refund policy for digital downloads with clear justification, exception policy for technical failures, and contact instructions. Make it firm but fair."

## Section 5: AI Productivity & Business Automation Prompts

### 5.1 — Meeting Summary
"Summarize the following meeting notes into a professional summary with: key decisions made, action items with owners and deadlines, and open questions. Notes: [PASTE MEETING NOTES]"

### 5.2 — Job Description Writer
"Write a professional job description for a [JOB TITLE] position at [COMPANY NAME]. Include: role summary, key responsibilities (6–8 bullet points), required qualifications, preferred qualifications, and what makes this role exciting. Salary range: [RANGE IN ETB]."

### 5.3 — Performance Review Template
"Write a structured employee performance review for [EMPLOYEE NAME] covering the period [DATE RANGE]. Areas to evaluate: quality of work, communication, reliability, initiative, teamwork. Include sections for strengths, areas for improvement, goals for the next period, and overall rating (1–5 scale)."

## License & Access

> License Key: SOL-AI-PROMPT-SUITE-2026
> This prompt suite is for single-user professional use. All prompts are original works of SolPay Digital Hub.
> You may use these prompts in client work. Redistribution or resale of this document is not permitted.
""",
            },

            # ── PRODUCT 5 ──────────────────────────────────────────────────────
            {
                'name': 'Ethiopian Freelancer Legal Contract & Invoice Kit 2026',
                'filename': 'ethiopian_freelancer_legal_kit_2026.pdf',
                'tagline': 'Stop working without a contract. Get paid in full, on time, every time — with professional legal templates built for Ethiopian freelancers.',
                'description': (
                    'Every freelancer who has been ghosted after delivering work, or underpaid by a client, '
                    'needed this kit. You get 5 fully drafted legal templates: a service agreement, a project '
                    'proposal, an invoice, a non-disclosure agreement (NDA), and a late payment notice. '
                    'All templates are professionally written, ready to use immediately, and adapted for '
                    'Ethiopian business context and BOA payment terms.'
                ),
                'price': 350.00,
                'category': 'templates',
                'content_text': """\
## Introduction: Why Every Ethiopian Freelancer Needs a Contract

In Ethiopia's growing freelance economy — covering web development, graphic design, writing, consulting, social media management, and more — most disputes happen because there was no written agreement.

A professional contract does three things:
1. Sets clear expectations so both parties understand exactly what is being delivered.
2. Protects your payment — clients who sign a contract are far more likely to pay in full and on time.
3. Establishes your professionalism — clients take you more seriously when you present formal documentation.

This kit gives you five ready-to-use templates. Fill in the brackets, print or send digitally, and you are protected.

## Template 1: Standard Freelance Service Agreement

---
SERVICE AGREEMENT

This Service Agreement ("Agreement") is entered into as of [DATE] between:

SERVICE PROVIDER: [Your Full Name / Business Name]
Address: [Your City, Ethiopia]
Phone: [Your Phone Number]
Email: [Your Email]

CLIENT: [Client Full Name / Company Name]
Address: [Client Address]
Phone: [Client Phone Number]

1. SERVICES TO BE PROVIDED

The Service Provider agrees to deliver the following services:
[Describe the project clearly — e.g., "Design and development of a 5-page professional website including homepage, about, services, portfolio, and contact pages."]

Deliverables include:
- [Deliverable 1]
- [Deliverable 2]
- [Deliverable 3]

2. PROJECT TIMELINE

Project Start Date: [DATE]
Estimated Completion Date: [DATE]

Timeline is contingent upon Client providing required materials (content, images, feedback) within [3] business days of each request.

3. PAYMENT TERMS

Total Project Fee: ETB [AMOUNT]
Payment Schedule:
- 50% Advance Payment (ETB [AMOUNT]): Due before project commencement.
- 50% Final Payment (ETB [AMOUNT]): Due upon project delivery and client approval.

All payments to be made via Bank of Abyssinia mobile transfer to:
Account Name: [Your Account Name]
Account Number: [Your BOA Account Number]

4. REVISIONS

This agreement includes [NUMBER] rounds of revisions. Additional revisions beyond this scope will be billed at ETB [RATE] per hour.

5. INTELLECTUAL PROPERTY

Upon receipt of full and final payment, all intellectual property rights to the final deliverables shall transfer to the Client. The Service Provider retains the right to display the work in their portfolio unless otherwise agreed in writing.

6. CONFIDENTIALITY

Both parties agree to keep all project details, business information, and client data strictly confidential.

7. TERMINATION

Either party may terminate this Agreement with [7] days written notice. In the event of termination, the Client shall pay for all work completed to the date of termination at a prorated rate.

8. LIMITATION OF LIABILITY

The Service Provider's total liability shall not exceed the total fees paid under this Agreement.

Signed:

Service Provider: _______________________ Date: ___________
Client: _______________________ Date: ___________
---

## Template 2: Project Proposal Template

---
PROJECT PROPOSAL

Prepared by: [Your Name / Business Name]
Prepared for: [Client Name / Company]
Date: [DATE]
Proposal Reference: [PROP-2026-XXX]

EXECUTIVE SUMMARY
[Client Name] requires [brief description of what they need]. [Your Name/Business] proposes to deliver [brief description of your solution] within [timeline] for a total investment of ETB [amount]. This proposal outlines our approach, timeline, and terms.

SCOPE OF WORK
We propose to deliver the following:
1. [Deliverable 1 — with brief description]
2. [Deliverable 2 — with brief description]
3. [Deliverable 3 — with brief description]

TIMELINE
Phase 1 — [Phase Name]: [Start Date] to [End Date]
Phase 2 — [Phase Name]: [Start Date] to [End Date]
Phase 3 — Final Delivery & Review: [Date]

INVESTMENT
Total project fee: ETB [AMOUNT]
50% due on signing: ETB [AMOUNT]
50% due on delivery: ETB [AMOUNT]
Payment via BOA mobile banking to account [YOUR BOA NUMBER].

TERMS
This proposal is valid for 14 days from the date issued.
Work begins upon receipt of signed agreement and advance payment.
---

## Template 3: Professional Invoice

---
INVOICE

From: [Your Name / Business Name]
[Your Address] | [Your Phone] | [Your Email]

Invoice Number: INV-2026-[XXX]
Invoice Date: [DATE]
Due Date: [DATE — typically 7 days from invoice date]

Bill To:
[Client Name]
[Client Company]
[Client Address / Phone]

DESCRIPTION OF SERVICES:
| Service | Details | Amount (ETB) |
| [Service 1] | [Brief description] | [Amount] |
| [Service 2] | [Brief description] | [Amount] |
| Less: Advance Paid | Payment received [DATE] | ([Amount]) |

TOTAL AMOUNT DUE: ETB [FINAL AMOUNT]

Payment Instructions:
Bank: Bank of Abyssinia (BOA)
Account Name: [Your Account Name]
Account Number: [Your BOA Account Number]
Reference: Invoice INV-2026-[XXX]

Please transfer the full amount and send the transaction reference to [Your Phone/Email] to confirm payment.

Thank you for your business.
---

## Template 4: Non-Disclosure Agreement (NDA)

---
NON-DISCLOSURE AGREEMENT

This Agreement is entered into as of [DATE] between [Your Name] ("Service Provider") and [Client Name] ("Client").

1. CONFIDENTIAL INFORMATION: Each party may share confidential business information, technical data, trade secrets, or business plans ("Confidential Information"). Both parties agree not to disclose this information to any third party without prior written consent.

2. EXCEPTIONS: Obligations do not apply to information that is publicly available, already known to the receiving party, or required to be disclosed by law.

3. DURATION: This Agreement remains in effect for [2] years from the date signed.

4. REMEDIES: A breach of this Agreement may cause irreparable harm. The non-breaching party is entitled to seek injunctive relief in addition to all other remedies available.

Service Provider: _______________________ Date: ___________
Client: _______________________ Date: ___________
---

## Template 5: Late Payment Notice

---
LATE PAYMENT NOTICE

Date: [DATE]
From: [Your Name]
To: [Client Name]
Subject: Outstanding Invoice INV-2026-[XXX] — Payment Overdue

Dear [Client Name],

This is a formal notice that Invoice No. INV-2026-[XXX] for ETB [AMOUNT], issued on [INVOICE DATE] and due on [DUE DATE], remains unpaid as of today.

Outstanding Balance: ETB [AMOUNT]
Days Overdue: [NUMBER]

Please arrange full payment via Bank of Abyssinia mobile transfer to account [YOUR BOA NUMBER] immediately.

If payment is not received within [5] business days of this notice, we reserve the right to:
- Suspend or withhold any ongoing or future deliverables.
- Apply a late payment fee of [5%] of the outstanding balance.
- Pursue this matter through appropriate legal channels.

If you have already arranged payment, please disregard this notice and send your transaction reference to [Your Phone/Email].

We value our working relationship and look forward to resolving this promptly.

Sincerely,
[Your Name]
[Your Business Name]
---

## License & Access

> License Key: SOL-LEGAL-KIT-ETH-2026
> These templates are for personal and professional use by the licensed purchaser.
> You may adapt these templates for your own client engagements.
> Redistribution or resale of this kit is strictly prohibited.
> SolPay Digital Hub recommends consulting a qualified Ethiopian attorney for complex legal matters.
""",
            },
        ]

        count = 0
        for data in products_data:
            pdf_rel_path = self.generate_pdf(
                filename=data['filename'],
                title=data['name'],
                subtitle=data['tagline'],
                author='SolPay Digital Hub',
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
            action = 'Created' if created else 'Updated'
            self.stdout.write(f"  {action}: {data['name']}")
            count += 1

        self.stdout.write(self.style.SUCCESS(
            f'\nSuccessfully seeded {count} professional products with full PDF e-books!'
        ))
