from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, HRFlowable, Table, TableStyle

OUTPUT_PATH = "frontend/public/bidder_foxtrot.pdf"

doc = SimpleDocTemplate(
    OUTPUT_PATH, pagesize=A4,
    rightMargin=2.5*cm, leftMargin=2.5*cm,
    topMargin=2*cm, bottomMargin=2*cm
)
styles = getSampleStyleSheet()

title_style = ParagraphStyle('T', parent=styles['Title'], fontSize=18, textColor=colors.HexColor('#0A3D6B'), spaceAfter=6)
sub_style   = ParagraphStyle('S', parent=styles['Normal'], fontSize=11, textColor=colors.HexColor('#1e5fa8'), spaceAfter=16)
h2_style    = ParagraphStyle('H2', parent=styles['Heading2'], fontSize=12, textColor=colors.HexColor('#b91c1c'), spaceAfter=6)
body_style  = ParagraphStyle('B', parent=styles['Normal'], fontSize=10, spaceAfter=12, leading=15)

def hr(): return HRFlowable(width='100%', thickness=1, color=colors.HexColor('#e2e8f0'), spaceAfter=12)

story = []

story.append(Paragraph("TECHNICAL BID & SELF-DECLARATION FORM", title_style))
story.append(Paragraph("GeM Tender Reference: KL/INFRA/2026/2000CR/001 — Kerala Smart Highway Corridor Phase II", sub_style))
story.append(hr())

# --- Identity Table ---
story.append(Paragraph("1. Bidder Identity & Statutory Registration", h2_style))
data = [
    ["Field", "Declared Details"],
    ["Registered Name of Entity", "Foxtrot Infrastructure Pvt. Ltd."],
    ["PAN (Permanent Account Number)", "FXINF7890K"],
    ["GSTIN (GST Identification Number)", "32FXINF7890K1Z4"],
    ["Udyam Registration No.", "UDYAM-KL-11-0078432"],
    ["Enterprise Classification", "MICRO ENTERPRISE"],
    ["Registered Office", "Plot 14-B, Kakkanad IT Park, Kochi, Kerala – 682030"],
]
t = Table(data, colWidths=[7*cm, 9*cm])
t.setStyle(TableStyle([
    ('BACKGROUND',  (0,0), (-1,0), colors.HexColor('#0A3D6B')),
    ('TEXTCOLOR',   (0,0), (-1,0), colors.white),
    ('FONTNAME',    (0,0), (-1,0), 'Helvetica-Bold'),
    ('FONTSIZE',    (0,0), (-1,-1), 9),
    ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.HexColor('#f8fafc'), colors.white]),
    ('GRID',        (0,0), (-1,-1), 0.5, colors.HexColor('#cbd5e1')),
    ('TOPPADDING',  (0,0), (-1,-1), 5),
    ('BOTTOMPADDING', (0,0), (-1,-1), 5),
]))
story.append(t)
story.append(Spacer(1, 0.4*cm))

# --- Financial ✅ PASS ---
story.append(Paragraph("2. Financial Capacity & MSME Eligibility", h2_style))
story.append(Paragraph(
    "Foxtrot Infrastructure Pvt. Ltd. hereby declares that its audited annual turnover for FY 2024–25 "
    "stands at <b>Rs. 7.2 Crores</b>, as duly certified by the statutory auditor M/s. Nair & Associates, "
    "Chartered Accountants (ICAI Reg. No. 004729S). The enterprise is registered as a "
    "<b>Micro Enterprise</b> vide Udyam Registration No. UDYAM-KL-11-0078432.", body_style))

# --- Make in India ❌ FAIL — claims only 35% ---
story.append(Paragraph("3. Make in India — Local Content Declaration", h2_style))
story.append(Paragraph(
    "The bidder declares that the proposed goods and services to be supplied under this contract "
    "shall incorporate a <b>local content of 35% (Thirty-Five Percent)</b> of the total contract "
    "value. Precision electronic sensors and SCADA hardware components shall be imported from "
    "certified OEM partners based in Germany and South Korea, owing to the non-availability of "
    "equivalent tested alternatives within the domestic market.", body_style))

# --- Sub-contracting ✅ PASS ---
story.append(Paragraph("4. Sub-Contracting Declaration", h2_style))
story.append(Paragraph(
    "No Joint Venture or Consortium arrangement has been entered into for this tender. "
    "Sub-contracting shall be limited to <b>15% (Fifteen Percent)</b> of the aggregate contract "
    "value, solely for ancillary civil foundation works. All sub-contracted work shall require "
    "prior written authorisation from the Competent Authority.", body_style))

# --- EMD ✅ PASS ---
story.append(Paragraph("5. Bid Security / Earnest Money Deposit (EMD)", h2_style))
story.append(Paragraph(
    "The bidder submits a <b>Bid Security Declaration</b> in lieu of the monetary EMD, as permitted "
    "under Ministry of Finance OM F.9/4/2020-PPD dated 12.11.2020 for registered MSMEs. "
    "The bid shall remain valid for 180 days from the date of submission.", body_style))

# --- GST ❌ FAIL — admits gaps ---
story.append(Paragraph("6. GST & Tax Compliance Declaration", h2_style))
story.append(Paragraph(
    "The bidder confirms that GSTIN <b>32FXINF7890K1Z4</b> is currently active. The entity "
    "acknowledges that <b>GSTR-3B returns for 3 months (April, May, June 2025) were delayed</b> "
    "due to a transition in the internal accounting system. Rectification filings have been "
    "submitted with applicable interest under Section 50 of the CGST Act.", body_style))

# --- Debarment ✅ PASS ---
story.append(Paragraph("7. Debarment & Integrity Declaration (GFR 175)", h2_style))
story.append(Paragraph(
    "Neither the firm, nor any of its Directors or Key Managerial Personnel are currently "
    "debarred, blacklisted, or prohibited from Government procurement by any Ministry, "
    "Department, State Government, or PSU as on the date of bid submission.", body_style))

story.append(hr())
story.append(Paragraph(
    "<b>Declaration:</b> I/We hereby certify that all information furnished above is true and correct. "
    "Any misrepresentation shall render the bid liable for rejection under applicable statutes.", body_style))
story.append(Spacer(1, 0.8*cm))
story.append(Paragraph("Authorised Signatory: _______________________", body_style))
story.append(Paragraph("Designation: Managing Director | Date: 15-October-2026", body_style))

doc.build(story)
print(f"Generated: {OUTPUT_PATH}")
