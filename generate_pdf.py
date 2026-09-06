from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, HRFlowable
import os

doc = SimpleDocTemplate(
    'Custom_Tender_Rules.pdf',
    pagesize=A4,
    rightMargin=2*cm, leftMargin=2*cm,
    topMargin=2*cm, bottomMargin=2*cm
)

styles = getSampleStyleSheet()
story = []

title_style = ParagraphStyle('title', parent=styles['Title'], fontSize=16, spaceAfter=12, textColor=colors.darkblue)
subtitle_style = ParagraphStyle('subtitle', parent=styles['Normal'], fontSize=10, spaceAfter=16, textColor=colors.black, alignment=1) # 1 is TA_CENTER
heading_style = ParagraphStyle('heading', parent=styles['Heading2'], fontSize=11, spaceAfter=6, textColor=colors.darkred, fontName='Helvetica-Bold')
body_style = ParagraphStyle('body', parent=styles['Normal'], fontSize=9.5, spaceAfter=14, leading=14, alignment=4) # 4 is TA_JUSTIFY

story.append(Paragraph('MINISTRY OF COMMERCE AND INDUSTRY', title_style))
story.append(Paragraph('DEPARTMENT FOR PROMOTION OF INDUSTRY AND INTERNAL TRADE (DPIIT)<br/>STANDARD BIDDING DOCUMENT (SBD) & COMPLIANCE CRITERIA', subtitle_style))
story.append(HRFlowable(width='100%', thickness=2, color=colors.darkblue))
story.append(Spacer(1, 0.5*cm))

rules = [
    ('1. Statutory Code of Integrity and Ethical Conduct', 
     'Pursuant to Rule 175 of the General Financial Rules (GFR) 2017, the Procuring Entity strictly enforces a zero-tolerance policy against corrupt, fraudulent, coercive, or collusive practices. Any omission, concealment, or misrepresentation of material facts intended to mislead the Procuring Entity for financial arbitrage shall invoke immediate disqualification and referral to the Central Vigilance Commission (CVC).'),

    ('2. Financial Capacity and Enterprise Classification (MSME Mandate)', 
     "In alignment with the Public Procurement Policy for Micro and Small Enterprises (MSEs) Order, 2012, this procurement tranche is strictly reserved for entities classified under the Micro category. To qualify, the bidder must present a verifiable Udyam Registration. Furthermore, the bidder's audited financial statements must reflect an annual turnover limit <= Rs. 10 Cr for the preceding three financial years. Exceeding this statutory threshold renders the bid fundamentally non-responsive."),

    ('3. Earnest Money Deposit (EMD) and Bid Security Declarations', 
     'Standard bidders are mandated to furnish an Earnest Money Deposit (EMD) equivalent to 2% of the estimated contract value via an irrevocable Bank Guarantee. However, registered Startups (as recognized by DPIIT) and bona fide Micro/Small Enterprises are granted EMD exemption. Such entities must upload a valid exemption certificate and a duly executed Bid Security Declaration on non-judicial stamp paper.'),

    ('4. Public Procurement (Preference to Make in India) Order, 2017', 
     'In consonance with the self-reliant India (Aatmanirbhar Bharat) initiative, strict preference shall be accorded to Class-I Local Suppliers. The bidder must submit a geographically verifiable self-certification demonstrating that the local content in the offered goods/services constitutes no less than 50% of the total value.'),

    ('5. Consortia, Joint Ventures, and Sub-contracting Limitations', 
     'Bids submitted by a Consortium or Joint Venture (JV) shall not be entertained under this specific tender ID. The prime bidder shall bear singular and indivisible legal responsibility for the execution of the contract. Sub-contracting is permissible only up to 20% of the aggregate contract value and mandates prior written authorization from the Competent Authority.'),

    ('6. Stringent Prohibitions on Debarment and Blacklisting', 
     'The bidder must tender a legally binding affidavit affirming that neither the corporate entity nor its Board of Directors is currently debarred, suspended, or blacklisted by any Central/State Government department, Public Sector Undertaking (PSU), or autonomous body under the Ministry of Finance guidelines (DoE OM No. F.1/20/2018-PPD).'),

    ('7. Goods and Services Tax (GST) and Fiscal Compliance', 
     'Absolute compliance with the Central Goods and Services Tax (CGST) Act, 2017 is non-negotiable. The bidder must possess an active GSTIN and furnish proof of uninterrupted filing of GSTR-1 and GSTR-3B returns for the trailing twelve months. Any suppression of tax liabilities detected via API triangulation will trigger automated bid rejection.'),

    ('8. Liquidated Damages (LD) and Performance Guarantees', 
     'Time is the essence of this contract. Failure to deliver the stipulated milestones within the mandated timeframe shall invite Liquidated Damages (LD) assessed at 0.5% of the delayed milestone value per week, capped at a maximum of 10% of the total contract value. A Performance Security equivalent to 5% of the contract value must be deposited within 14 days of the Letter of Award (LoA).'),

    ('9. Force Majeure and Exigency Clauses', 
     "Neither party shall be liable for punitive damages in the event of performance delays catalyzed by Force Majeure events, explicitly defined as Acts of God, sovereign embargos, state-wide pandemics recognized by the WHO, or systemic civil unrest. The affected party must issue a formal notice within 7 days of the exigency's onset to invoke this clause."),

    ('10. Dispute Resolution and Exclusive Arbitral Jurisdiction', 
     'Any disputes, contentions, or claims arising out of this procurement contract shall initially be subjected to amicable conciliation. In the event of an impasse, the dispute shall be referred to a Sole Arbitrator appointed by the Secretary, DPIIT. The arbitral proceedings shall be governed by the Arbitration and Conciliation Act, 1996, with the exclusive legal venue restricted to the judicial courts of New Delhi.')
]

for title, desc in rules:
    story.append(Paragraph(title, heading_style))
    story.append(Paragraph(desc, body_style))

doc.build(story)
print('Updated PDF generated at:', os.path.abspath('Custom_Tender_Rules.pdf'))
