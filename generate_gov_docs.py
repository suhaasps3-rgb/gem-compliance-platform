"""
Generate realistic mock GST Certificate (Form GST REG-06) and Udyam Registration Certificate
that mimic the layout of actual Indian government documents.
"""
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.lib import colors
from reportlab.platypus import (SimpleDocTemplate, Paragraph, Spacer, Table,
                                TableStyle, HRFlowable, Image)
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
import io

W, H = A4

# ─── Shared helpers ──────────────────────────────────────────────────────────
def cell(text, bold=False, size=9, color=colors.black, align=TA_LEFT, bg=None):
    style = ParagraphStyle('c', fontName='Helvetica-Bold' if bold else 'Helvetica',
                           fontSize=size, textColor=color, alignment=align,
                           leading=size + 3)
    return Paragraph(text, style)


# ════════════════════════════════════════════════════════════════════════════
# 1.  GST REGISTRATION CERTIFICATE  (Form GST REG-06)
# ════════════════════════════════════════════════════════════════════════════
def make_gst():
    path = "frontend/public/gst_tender_demo.pdf"
    doc = SimpleDocTemplate(path, pagesize=A4,
                            rightMargin=1.8*cm, leftMargin=1.8*cm,
                            topMargin=1.5*cm, bottomMargin=1.5*cm)
    s = getSampleStyleSheet()
    BLUE  = colors.HexColor('#003580')
    LBLUE = colors.HexColor('#dce9f7')
    RED   = colors.HexColor('#c0392b')
    GREY  = colors.HexColor('#f2f4f7')

    def h(text, size=10, bold=True, align=TA_CENTER, color=colors.black):
        return Paragraph(text, ParagraphStyle('h', fontName='Helvetica-Bold' if bold else 'Helvetica',
                                              fontSize=size, textColor=color, alignment=align, leading=size+4))

    story = []

    # ── Ministry Header ──
    story.append(h("GOVERNMENT OF INDIA", 11, color=BLUE))
    story.append(h("MINISTRY OF FINANCE — DEPARTMENT OF REVENUE", 9, color=BLUE))
    story.append(h("GOODS AND SERVICES TAX NETWORK (GSTN)", 9, color=BLUE))
    story.append(Spacer(1, 0.2*cm))
    story.append(HRFlowable(width='100%', thickness=2, color=BLUE))
    story.append(Spacer(1, 0.15*cm))
    story.append(h("CERTIFICATE OF REGISTRATION", 14, color=BLUE))
    story.append(h("[See Rule 10(1) of the Central Goods and Services Tax Rules, 2017]", 8, bold=False, color=colors.HexColor('#555')))
    story.append(h("FORM GST REG-06", 9, color=RED))
    story.append(Spacer(1, 0.3*cm))

    # ── GSTIN Banner ──
    gstin_tbl = Table([
        [cell("GSTIN", bold=True, size=9, color=BLUE),
         cell("32FXINF7890K1Z4", bold=True, size=18, color=BLUE, align=TA_CENTER)]
    ], colWidths=[4*cm, 12*cm])
    gstin_tbl.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), LBLUE),
        ('BOX', (0,0), (-1,-1), 1.5, BLUE),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 8),
        ('BOTTOMPADDING', (0,0), (-1,-1), 8),
        ('LEFTPADDING', (0,0), (0,0), 10),
    ]))
    story.append(gstin_tbl)
    story.append(Spacer(1, 0.4*cm))

    # ── Registration Details Table ──
    rows = [
        ["1.", "Legal Name of Business", "Foxtrot Infrastructure Private Limited"],
        ["2.", "Trade Name (if any)", "FOXTROT INFRA"],
        ["3.", "Constitution of Business", "Private Limited Company"],
        ["4.", "Address of Principal Place of Business",
                "Plot 14-B, Kakkanad IT Park,\nErnakulam District, Kochi, Kerala – 682030"],
        ["5.", "Date of Liability", "14/03/2017"],
        ["6.", "Period of Validity", "14/03/2017 to Till Cancellation"],
        ["7.", "Type of Registration", "Composition"],          # ← FAIL: can't do B2G contracts
        ["8.", "Particulars of Approving Authority", ""],
        ["",   "Name", "ASST. COMMISSIONER — WARD 14, ERNAKULAM"],
        ["",   "Designation", "State Tax Officer, Kerala GST Department"],
        ["",   "Jurisdiction", "State — Kerala / Centre — Ernakulam-II"],
        ["9.", "Date of Issue of Certificate", "15/03/2017"],
        ["10.","Note",
                "⚠  Composition scheme taxpayers CANNOT collect GST from recipients.\n"
                "Supplies to Government entities may require transition to Regular scheme."],
    ]

    tbl_data = []
    for r in rows:
        tbl_data.append([
            cell(r[0], size=8),
            cell(r[1], bold=True, size=8),
            cell(r[2], size=8),
        ])

    det_tbl = Table(tbl_data, colWidths=[0.8*cm, 7*cm, 8.2*cm])
    det_tbl.setStyle(TableStyle([
        ('GRID', (0,0), (-1,-1), 0.4, colors.HexColor('#c5d5e8')),
        ('ROWBACKGROUNDS', (0,0), (-1,-1), [colors.white, GREY]),
        ('TOPPADDING', (0,0), (-1,-1), 5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
        ('LEFTPADDING', (0,0), (-1,-1), 6),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
    ]))
    story.append(det_tbl)
    story.append(Spacer(1, 0.5*cm))

    # ── Signature Block ──
    sig = Table([
        [cell("This is a system generated certificate. No signature required.", size=8,
              color=colors.HexColor('#666'), align=TA_CENTER),
         cell("Verified via GST Portal\nwww.gst.gov.in", size=8,
              color=BLUE, align=TA_RIGHT)],
    ], colWidths=[10*cm, 6*cm])
    sig.setStyle(TableStyle([('VALIGN', (0,0), (-1,-1), 'TOP')]))
    story.append(sig)
    story.append(Spacer(1, 0.3*cm))
    story.append(HRFlowable(width='100%', thickness=1, color=BLUE))
    story.append(Spacer(1, 0.15*cm))
    story.append(h("Important: This certificate is valid only if the taxpayer's GSTIN status is ACTIVE on the GST Portal.", 7, bold=False, color=RED))

    doc.build(story)
    print(f"Generated: {path}")


# ════════════════════════════════════════════════════════════════════════════
# 2.  UDYAM REGISTRATION CERTIFICATE
# ════════════════════════════════════════════════════════════════════════════
def make_udyam():
    path = "frontend/public/udyam_tender_demo.pdf"
    doc = SimpleDocTemplate(path, pagesize=A4,
                            rightMargin=1.8*cm, leftMargin=1.8*cm,
                            topMargin=1.5*cm, bottomMargin=1.5*cm)

    DBLUE  = colors.HexColor('#1a237e')
    LBLUE  = colors.HexColor('#e3f2fd')
    ORANGE = colors.HexColor('#e65100')
    GREY   = colors.HexColor('#f5f5f5')

    def h(text, size=10, bold=True, align=TA_CENTER, color=colors.black):
        return Paragraph(text, ParagraphStyle('h', fontName='Helvetica-Bold' if bold else 'Helvetica',
                                              fontSize=size, textColor=color, alignment=align, leading=size+4))

    story = []

    # ── Header ──
    story.append(h("भारत सरकार / GOVERNMENT OF INDIA", 11, color=DBLUE))
    story.append(h("Ministry of Micro, Small and Medium Enterprises", 10, color=DBLUE))
    story.append(Spacer(1, 0.15*cm))
    story.append(HRFlowable(width='100%', thickness=3, color=ORANGE))
    story.append(Spacer(1, 0.15*cm))
    story.append(h("UDYAM REGISTRATION CERTIFICATE", 15, color=DBLUE))
    story.append(Spacer(1, 0.15*cm))
    story.append(HRFlowable(width='100%', thickness=1, color=ORANGE))
    story.append(Spacer(1, 0.3*cm))

    # ── Udyam Number Banner ──
    urn_tbl = Table([[
        cell("UDYAM REGISTRATION NUMBER", bold=True, size=9, color=DBLUE, align=TA_CENTER),
    ], [
        cell("UDYAM-KL-11-0078432", bold=True, size=20, color=ORANGE, align=TA_CENTER),
    ]], colWidths=[16*cm])
    urn_tbl.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), LBLUE),
        ('BOX', (0,0), (-1,-1), 2, DBLUE),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('TOPPADDING', (0,0), (-1,-1), 8),
        ('BOTTOMPADDING', (0,0), (-1,-1), 8),
    ]))
    story.append(urn_tbl)
    story.append(Spacer(1, 0.4*cm))

    # ── Details ──
    fields = [
        ("Name of Enterprise",         "FOXTROT INFRASTRUCTURE PRIVATE LIMITED"),
        ("Type of Organisation",        "Private Limited Company"),
        ("Date of Incorporation",       "14/03/2017"),
        ("Date of Commencement of Production/Business", "01/04/2017"),
        ("Major Activity",              "Services"),
        ("National Industry Classification (NIC) Code", "42101 — Construction of Roads and Highways"),
        ("Social Category of Entrepreneur", "General"),
        ("Name of District",            "Ernakulam"),
        ("Name of State / UT",          "Kerala"),
        ("PIN",                         "682030"),
        ("Official Email",              "compliance@foxtrotinfra.in"),
        ("Mobile",                      "+91-9400123456"),
        ("Flat / Door No.",             "Plot 14-B"),
        ("Name of Premises / Building", "Kakkanad IT Park"),
        ("City",                        "Kochi"),
        ("District",                    "Ernakulam"),
        ("Date of Udyam Registration",  "20/03/2017"),
    ]

    tbl_data = [[
        cell("Field", bold=True, size=9, color=colors.white),
        cell("Details", bold=True, size=9, color=colors.white)
    ]]
    for label, value in fields:
        tbl_data.append([
            cell(label, bold=True, size=8),
            cell(value, size=8),
        ])

    # Enterprise classification row — highlighted with SMALL (mismatch with bidder's MICRO claim)
    tbl_data.append([
        cell("Enterprise Classification", bold=True, size=9, color=DBLUE),
        cell("SMALL ENTERPRISE", bold=True, size=11, color=colors.HexColor('#c0392b')),   # ← MISMATCH
    ])

    det = Table(tbl_data, colWidths=[8*cm, 8*cm])
    row_styles = [
        ('BACKGROUND', (0,0), (-1,0), DBLUE),
        ('BACKGROUND', (0,-1), (-1,-1), LBLUE),
        ('ROWBACKGROUNDS', (0,1), (-1,-2), [colors.white, GREY]),
        ('GRID', (0,0), (-1,-1), 0.4, colors.HexColor('#b0bec5')),
        ('TOPPADDING', (0,0), (-1,-1), 5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
        ('LEFTPADDING', (0,0), (-1,-1), 8),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
    ]
    det.setStyle(TableStyle(row_styles))
    story.append(det)
    story.append(Spacer(1, 0.5*cm))

    # ── Footer ──
    story.append(HRFlowable(width='100%', thickness=1.5, color=ORANGE))
    story.append(Spacer(1, 0.2*cm))
    story.append(h("This is a computer generated certificate. It does not require any signature.", 8, bold=False,
                   color=colors.HexColor('#555')))
    story.append(h("Verify at: https://udyamregistration.gov.in", 8, bold=False, color=DBLUE))
    story.append(Spacer(1, 0.15*cm))
    story.append(h("© Government of India — Ministry of MSME", 7, bold=False,
                   color=colors.HexColor('#888')))

    doc.build(story)
    print(f"Generated: {path}")


if __name__ == "__main__":
    make_gst()
    make_udyam()
    print("All documents generated.")
