import os
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import cm
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable, Image as RLImage
from reportlab.graphics.shapes import Drawing, Rect, String
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT, TA_JUSTIFY

OUT = r'C:/Users/Suhaas/.gemini/antigravity/scratch/gem_compliance/frontend/public'
B  = colors.HexColor('#003580')
LB = colors.HexColor('#dce9f7')
R  = colors.HexColor('#c0392b')
G  = colors.HexColor('#1a7a4a')
O  = colors.HexColor('#d35400')
N  = colors.HexColor('#1a237e')
GR = colors.HexColor('#f5f5f5')
MG = colors.HexColor('#888888')
BR = colors.HexColor('#b0bec5')

def P(t, sz=9, bold=False, col=None, al=TA_LEFT):
    if col is None: col = colors.black
    fn = 'Helvetica-Bold' if bold else 'Helvetica'
    return Paragraph(t, ParagraphStyle('p', fontName=fn, fontSize=sz, textColor=col, alignment=al, leading=sz+3))

def H(t, sz=12, col=None, bold=True):
    if col is None: col = B
    fn = 'Helvetica-Bold' if bold else 'Helvetica'
    return Paragraph(t, ParagraphStyle('h', fontName=fn, fontSize=sz, textColor=col, alignment=TA_CENTER, leading=sz+5))

def KV(rows, cw=None, hdr=None):
    cw = cw or [7.5*cm, 8.5*cm]
    data = []
    if hdr:
        data.append([P(hdr[0], bold=True, col=colors.white, sz=9), P(hdr[1], bold=True, col=colors.white, sz=9)])
    for row in rows:
        bv = row[2] if len(row) > 2 else False
        cv = row[3] if len(row) > 3 else colors.black
        data.append([P(row[0], bold=True, sz=8), P(row[1], bold=bv, sz=8, col=cv)])
    t = Table(data, colWidths=cw)
    st = [('GRID',(0,0),(-1,-1),0.4,BR),('ROWBACKGROUNDS',(0,1 if hdr else 0),(-1,-1),[colors.white,GR]),
          ('TOPPADDING',(0,0),(-1,-1),5),('BOTTOMPADDING',(0,0),(-1,-1),5),
          ('LEFTPADDING',(0,0),(-1,-1),8),('VALIGN',(0,0),(-1,-1),'TOP')]
    if hdr: st.append(('BACKGROUND',(0,0),(-1,0),N))
    t.setStyle(TableStyle(st)); return t

def BAN(lbl, val, lc=None, vc=None, bg=None):
    if lc is None: lc = B
    if vc is None: vc = B
    if bg is None: bg = LB
    t = Table([[P(lbl,bold=True,sz=8,col=lc), P(val,bold=True,sz=20,col=vc,al=TA_CENTER)]], colWidths=[4.5*cm,11.5*cm])
    t.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,-1),bg),('BOX',(0,0),(-1,-1),1.5,lc),
                            ('VALIGN',(0,0),(-1,-1),'MIDDLE'),('TOPPADDING',(0,0),(-1,-1),10),
                            ('BOTTOMPADDING',(0,0),(-1,-1),10),('LEFTPADDING',(0,0),(0,0),10)]))
    return t

def FTR(s, url, note=None):
    s += [Spacer(1,0.4*cm), HRFlowable(width='100%',thickness=1,color=B), Spacer(1,0.15*cm),
          P(f'Verify at: {url}', sz=7, col=MG, al=TA_CENTER)]
    if note: s.append(P(note, sz=7, col=R, al=TA_CENTER))
    s.append(P('Government of India -- All Rights Reserved', sz=7, col=MG, al=TA_CENTER))


def SIG_STAMP(title="AUTHORIZED SIGNATORY", name="OFFICIAL SEAL", date_str="01-Aug-2026"):
    stamp_path = os.path.join(OUT, 'stamps', 'stamp_director.png')
    sig_path = os.path.join(OUT, 'stamps', 'sig_director.png')
    
    t_data = [[
        P(f"<b>{title}</b><br/>{name}<br/>Date: {date_str}<br/><font color='#1a7a4a'><b>DULY SIGNED & STAMPED</b></font>", sz=8),
        RLImage(sig_path, width=3.2*cm, height=1.1*cm),
        RLImage(stamp_path, width=2.2*cm, height=2.2*cm)
    ]]
    t = Table(t_data, colWidths=[7*cm, 5*cm, 3*cm])
    t.setStyle(TableStyle([('VALIGN', (0,0), (-1,-1), 'MIDDLE')]))
    return t

def D(path):
    return SimpleDocTemplate(path, pagesize=A4, rightMargin=2*cm, leftMargin=2*cm, topMargin=1.5*cm, bottomMargin=1.5*cm)


def ca_turnover():
    p = os.path.join(OUT, 'ca_turnover.pdf'); d = D(p); s = []
    s += [H('INSTITUTE OF CHARTERED ACCOUNTANTS OF INDIA (ICAI)', 11, N),
          H('CERTIFICATE OF ANNUAL TURNOVER AND NET WORTH', 13, N),
          P('[Sec. 44AB of the Income-tax Act, 1961 | Rule 6G of the IT Rules, 1962]', 7, col=MG, al=TA_CENTER),
          Spacer(1,0.3*cm), HRFlowable(width='100%',thickness=2,color=N), Spacer(1,0.3*cm),
          P('I, <b>CA Ramesh Kumar Iyer</b>, Chartered Accountant (Membership No. <b>123456</b>, FCA), practicing at B-204, Maker Chambers IV, Nariman Point, Mumbai 400021, holding a valid Certificate of Practice issued by the ICAI Council, do hereby certify as follows:', 9, al=TA_JUSTIFY), Spacer(1,0.25*cm)]
    rows = [
        ('Name of Entity (Auditee)', 'ACME CORP PRIVATE LIMITED'),
        ('CIN / Registration No.', 'U29299MH2014PTC254781'),
        ('Registered Office', 'Unit 7, Bandra-Kurla Complex, Mumbai 400051, Maharashtra'),
        ('PAN of Entity', 'ACMEC1234Q'),
        ('GSTIN', '27ACMEC1234Q1ZV'),
        ('Assessment Year under Tax Audit', 'AY 2025-26 (Financial Year 2024-25)'),
        ('Nature of Audit', 'Statutory Tax Audit u/s 44AB -- Turnover exceeds prescribed threshold'),
        ('Audited Financial Statements Ref.', 'Balance Sheet and P&L Account dated 31-March-2025'),
        ('Annual Turnover (FY 2024-25)', 'INR 12,00,00,000/- (Rupees Twelve Crore Only)', True, G),
        ('Net Worth (31 Mar 2025)', 'INR 4,37,52,000/- (Rupees Four Crore Thirty-Seven Lakh)'),
        ('Operating EBITDA Margin', '18.4% (Net Revenue INR 11.78 Crore)'),
        ('Certification Basis', 'Audited books, ledger extracts, Form 26AS (TRACES) reconciliation'),
        ('UDIN (Unique Document Identification No.)', '25123456AABCDE9812', True, N),
        ('Date of Issue', '01-August-2026'),
    ]
    s += [KV(rows, hdr=('Particulars', 'Details')), Spacer(1,0.4*cm),
          P('I further certify that the above turnover has been computed per the Guidance Note on Tax Audit u/s 44AB (Revised 2014 Edition), ICAI. Figures reconcile with GSTR-1/GSTR-3B and TDS certificates (Form 16A). No qualifications or adverse remarks have been issued in the audit report.', 8, al=TA_JUSTIFY),
          Spacer(1,0.5*cm)]
    stamp_img = RLImage(os.path.join(OUT, 'stamps', 'stamp_ca_acme.png'), width=2.4*cm, height=2.4*cm)
    sig_img = RLImage(os.path.join(OUT, 'stamps', 'sig_ca_iyer.png'), width=3.4*cm, height=1.2*cm)
    
    sig = Table([[
        P('<b>For CA Ramesh Kumar Iyer & Associates</b><br/>Chartered Accountants<br/>Firm Reg. No.: 012345W<br/><b>CA Ramesh Kumar Iyer</b> | M.No. 123456<br/>UDIN: 25123456AABCDE9812', sz=8),
        sig_img,
        stamp_img
    ]], colWidths=[8*cm, 4.5*cm, 3.5*cm])
    sig.setStyle(TableStyle([('VALIGN',(0,0),(-1,-1),'MIDDLE')])); s.append(sig)
    FTR(s, 'https://udin.icai.org', 'Verify UDIN before reliance. Certificate invalid without UDIN verification.')
    d.build(s); print('  ca_turnover.pdf')


def epfo():
    p = os.path.join(OUT, 'epfo_demo.pdf'); d = D(p); s = []
    s += [H('EMPLOYEES PROVIDENT FUND ORGANISATION', 13, B),
          H('Ministry of Labour and Employment, Government of India', 9, B, bold=False),
          HRFlowable(width='100%',thickness=2.5,color=B),
          H('ELECTRONIC CHALLAN CUM RETURN (ECR) -- PAYMENT RECEIPT', 11, B),
          P('[EPF and Miscellaneous Provisions Act, 1952 -- Para 38 of EPF Scheme, 1952]', 7, col=MG, al=TA_CENTER),
          Spacer(1,0.3*cm), BAN('ECR Reference / Challan No.','ECR000123456789'), Spacer(1,0.3*cm)]
    rows = [
        ('Establishment Name', 'ACME CORP PRIVATE LIMITED'),
        ('Establishment Code (ECO No.)', 'MHBAN0012345'),
        ('Regional PF Office', 'EPFO Regional Office, Bandra, Mumbai'),
        ('Wage Month / Return Period', 'August 2026 (01/08/2026 to 31/08/2026)'),
        ('Total Employees on Roll', '22 (Twenty-Two)'),
        ('EPF Wages (capped at INR 15,000 per EE)', 'INR 15,00,000/-'),
        ('Employee Contribution (EE) @ 12%', 'INR 1,80,000/-'),
        ('Employer Contribution EPF @ 3.67%', 'INR 55,050/-'),
        ('Employer Contribution EPS @ 8.33%', 'INR 1,24,950/-'),
        ('EDLI Contribution @ 0.50%', 'INR 7,500/-'),
        ('EPF Admin Charges @ 0.50%', 'INR 7,500/-'),
        ('Total Challan Amount', 'INR 3,75,000/-', True, G),
        ('Date of Payment', '05-Sep-2026 (within statutory due date of 15-Sep-2026)'),
        ('NEFT Reference No.', 'SBIN2609051234567890'),
        ('TRRN (Temporary Return Reference No.)', 'MH23456789012'),
        ('Payment Status', 'PAID -- Challan Generated and Amount Credited', True, G),
    ]
    s += [KV(rows, hdr=('Field','Details')), Spacer(1,0.3*cm),
          P('Statutory Note: Contributions under Para 38 EPF Scheme, 1952 are due by the 15th of the following month. Delayed payment attracts interest @ 12% p.a. under Sec. 7Q and damages under Sec. 14B of EP&MP Act, 1952. Verify TRRN at the EPFO Unified Portal.', 7.5, al=TA_JUSTIFY)]
    s.append(SIG_STAMP()); FTR(s, 'https://unifiedportal-emp.epfindia.gov.in', 'Verify TRRN on EPFO Unified Portal before reliance.')
    d.build(s); print('  epfo_demo.pdf')


def esic():
    p = os.path.join(OUT, 'esic_demo.pdf'); d = D(p); s = []
    s += [H('EMPLOYEES STATE INSURANCE CORPORATION', 13, B),
          H('Ministry of Labour and Employment, Government of India', 9, B, bold=False),
          HRFlowable(width='100%',thickness=2.5,color=B),
          H('CONTRIBUTION PAYMENT RECEIPT -- FORM ESI-5 (ELECTRONIC)', 11, B),
          P('[Sec. 40 of the Employees State Insurance Act, 1948 -- Payment of Contribution]', 7, col=MG, al=TA_CENTER),
          Spacer(1,0.25*cm), BAN('ESI Challan Reference No.','031261234567890'), Spacer(1,0.3*cm)]
    rows = [
        ('Employer Name (Registered)', 'ACME CORP PRIVATE LIMITED'),
        ('Employer Code (ESIC)', '31000123450000100'),
        ('Unit Type', 'Factory/Establishment -- Permanent Registration'),
        ('Region / Sub-Region Office', 'ESIC Regional Office -- Mumbai, Maharashtra'),
        ('Contribution Period', 'August 2026 (01-Aug to 31-Aug 2026)'),
        ('Total Insured Persons (IPs)', '22'),
        ('Total Wages Disbursed', 'INR 16,50,000/-'),
        ('Employer Contribution @ 3.25%', 'INR 53,625/-'),
        ('Employee Contribution @ 0.75%', 'INR 12,375/-'),
        ('Total ESI Contribution', 'INR 66,000/-', True, G),
        ('Date of Remittance', '06-Sep-2026'),
        ('UTR No. / Bank Reference', 'PUNB2609062345678'),
        ('Payment Status', 'PAID -- Contribution Received and Allocated', True, G),
        ('Compliance Status', 'REGULAR -- No overdue or arrears outstanding'),
    ]
    s += [KV(rows, hdr=('Field','Details')), Spacer(1,0.3*cm),
          P('Regulatory Note: Under Regulation 31 of the ESI (General) Regulations, 1950, contributions are payable on or before the 21st day of the month following the contribution period. Late remittance attracts interest @ 12% p.a. plus damages under Regulation 31-C. This receipt is system-generated by the ESIC Portal.', 7.5, al=TA_JUSTIFY)]
    s.append(SIG_STAMP()); FTR(s, 'https://esic.nic.in', 'Cross-verify IP count and contributions on ESIC Employer Portal.')
    d.build(s); print('  esic_demo.pdf')


def startup_india():
    p = os.path.join(OUT, 'startup_india_demo.pdf'); d = D(p); s = []
    RED = colors.HexColor('#E74C3C')
    s += [H('GOVERNMENT OF INDIA', 12, N),
          H('Department for Promotion of Industry and Internal Trade (DPIIT)', 10, N, bold=False),
          H('Ministry of Commerce and Industry', 9, N, bold=False),
          HRFlowable(width='100%',thickness=3,color=RED),
          H('STARTUP INDIA -- DPIIT RECOGNITION CERTIFICATE', 14, RED),
          P('[Startup India Initiative -- Notif. No. G.S.R. 127(E) dated 19 Feb 2019]', 7, col=MG, al=TA_CENTER),
          Spacer(1,0.3*cm), BAN('DPIIT Recognition No.','DIPP12345', RED, RED, bg=colors.HexColor('#fdecea')), Spacer(1,0.35*cm)]
    rows = [
        ('Legal Name of Entity', 'INDIGO INNOVATIONS PRIVATE LIMITED'),
        ('Type of Entity', 'Company incorporated under Companies Act, 2013'),
        ('CIN', 'U72900DL2021PTC385501'),
        ('PAN', 'INDGO9012P'),
        ('Date of Incorporation', '12-April-2021'),
        ('Sector / Industry', 'Technology / AI-Based Procurement Automation'),
        ('Nature of Innovation', 'AI-powered compliance analytics for public procurement -- NLP-based rule extraction and cross-validation against statutory registries (GSTN, MCA21, EPFO, Udyam)'),
        ('DPIIT Recognition Number', 'DIPP12345'),
        ('Date of Recognition', '15-May-2022'),
        ('Validity of Recognition', '14-May-2027 (Five years from date of recognition)'),
        ('EMD Exemption Eligibility', 'YES -- Eligible under MeitY/DPIIT GeM EMD Waiver Policy 2022', True, G),
        ('Tax Exemption u/s 80-IAC', 'Applied -- Exemption period FY 2022-23 to FY 2024-25'),
        ('Certificate Status', 'ACTIVE -- Valid as of issue date', True, G),
    ]
    s += [KV(rows, hdr=('Field','Details')), Spacer(1,0.35*cm),
          P('This certificate is issued pursuant to the entity successful self-certification under the Startup India portal and DPIIT validation. Recognition implies eligibility for GeM EMD/PBG waivers, fast-track patent examination, and compliance relaxation per notification dated 19-Feb-2019. The entity must intimate DPIIT within 30 days of ceasing to qualify as a Startup.', 7.5, al=TA_JUSTIFY)]
    FTR(s, 'https://startupindia.gov.in', 'Verify recognition number on Startup India Portal before reliance.')
    d.build(s); print('  startup_india_demo.pdf')


def nsic():
    p = os.path.join(OUT, 'nsic_demo.pdf'); d = D(p); s = []
    s += [H('NATIONAL SMALL INDUSTRIES CORPORATION LIMITED', 13, B),
          H('(A Government of India Enterprise -- Ministry of MSME)', 9, B, bold=False),
          H('Corporate Office: NSIC Bhavan, Okhla Industrial Estate, New Delhi 110020', 8, MG, bold=False),
          HRFlowable(width='100%',thickness=2.5,color=B),
          H('ENLISTMENT CERTIFICATE -- SINGLE POINT REGISTRATION SCHEME (SPRS)', 11, B),
          P('[Issued under the NSIC SPRS for MSMEs for Central Government Purchases]', 7, col=MG, al=TA_CENTER),
          Spacer(1,0.3*cm), BAN('NSIC Certificate No.','NS/MC/CH/2023/01234'), Spacer(1,0.3*cm)]
    rows = [
        ('Name of Micro/Small Enterprise', 'INDIGO INNOVATIONS PRIVATE LIMITED'),
        ('Udyam Registration No.', 'UDYAM-DL-07-0123456'),
        ('Registered Office', 'C-14, 2nd Floor, Lajpat Nagar-II, New Delhi 110024'),
        ('MSME Category', 'Category-I -- Micro Enterprise'),
        ('Monetary Limit (EMD Exemption)', 'INR 25,00,000/- per tender (MoF circular 23-Mar-2012)'),
        ('Items / Products Registered', 'ICT Equipment; AI-Based Software Systems; Procurement Analytics Platforms'),
        ('NIC Code', '62011 -- Custom Computer Programming Activities'),
        ('Date of Enlistment', '10-Jun-2023'),
        ('Valid Upto', '09-Jun-2026'),
        ('EMD Exemption Eligible', 'YES -- Under MSME Development Act, 2006 (Sec. 11)', True, G),
        ('Tender Fee Exemption', 'Applicable -- MoF OM No. F.9/4/2018-PPD'),
        ('SPRS Status', 'ACTIVE -- Current', True, G),
        ('Issuing Authority', 'Deputy General Manager, NSIC Branch Office, Chandigarh'),
    ]
    s += [KV(rows, hdr=('Field','Details')), Spacer(1,0.35*cm),
          P('This certificate entitles the registered MSME to exemption from EMD and tender document fees in Central Government purchases subject to the monetary limit. Monetary Limit is subject to annual revision based on audited turnover. Renewal must be applied at least 60 days prior to expiry.', 7.5, al=TA_JUSTIFY)]
    s.append(SIG_STAMP()); FTR(s, 'https://www.nsic.co.in/SPRS', 'Verify certificate number and validity at NSIC SPRS portal before submission.')
    d.build(s); print('  nsic_demo.pdf')


def wo1():
    p = os.path.join(OUT, 'work_order_1.pdf'); d = D(p); s = []
    hdr = Table([[P('RELIANCE INDUSTRIES LIMITED\nCIN: L17110MH1973PLC019786\nMaker Chambers IV, Nariman Point, Mumbai 400021\nGSTIN: 27AAACR5055K1ZB', bold=True, sz=9, col=N),
                  P('PURCHASE ORDER\nNo: WO-RIL/MH/2023/1023\nDate: 01-April-2023\nFY: 2023-24', sz=9, al=TA_RIGHT, col=N)]],
                colWidths=[9*cm,7*cm])
    hdr.setStyle(TableStyle([('VALIGN',(0,0),(-1,-1),'TOP')])); s.append(hdr)
    s += [HRFlowable(width='100%',thickness=2,color=N), Spacer(1,0.2*cm),
          H('PURCHASE ORDER -- CAPITAL EQUIPMENT PROCUREMENT', 12, N), Spacer(1,0.2*cm),
          P('<b>To M/s:</b>', sz=9), P('ACME CORP PRIVATE LIMITED', bold=True, sz=11, col=B),
          P('Unit 7, Bandra-Kurla Complex, Mumbai 400051 | GSTIN: 27ACMEC1234Q1ZV | PAN: ACMEC1234Q', sz=8), Spacer(1,0.25*cm)]
    rows = [
        ('PO No.', 'WO-RIL/MH/2023/1023'),
        ('Vendor Code (SAP)', 'VND-MH-002341'),
        ('Description', 'Supply, Installation, Testing and Commissioning (SITC) of AP-X500 Series High-Capacity Centrifugal Pump Systems conforming to IS 5120:2019 and API 610 (12th Edition)'),
        ('Quantity', '04 (Four) Units -- Model AP-X500-HCP'),
        ('Basic Order Value (excl. GST)', 'INR 2,18,10,000/-'),
        ('IGST @ 18% (HSN 84137000)', 'INR 39,25,800/-'),
        ('Total PO Value (incl. GST)', 'INR 2,57,35,800/- (Two Crore Fifty-Seven Lakh)', True, N),
        ('Delivery Schedule', '180 days from PO date -- 30-Sep-2023'),
        ('Delivery Destination', 'Jamnagar Refinery Complex, Gujarat -- Unit-III Pump House'),
        ('Performance Bank Guarantee (PBG)', '10% of Basic PO Value -- BG valid 18 months post FAT'),
        ('Liquidated Damages (LD)', '0.5% per week of delay, max 5% of PO value'),
        ('Payment Terms', '30% Advance against BG; 60% against dispatch docs; 10% on Factory Acceptance Test'),
        ('Applicable Standards', 'IS 5120:2019; API 610; IS 1367; ISO 9001:2015'),
        ('Status', 'COMPLETED -- FAT Cleared and Final Invoice Settled (07-Oct-2023)', True, G),
    ]
    s += [KV(rows, hdr=('Clause','Details')), Spacer(1,0.3*cm)]
    sig = Table([[P('For RELIANCE INDUSTRIES LIMITED',bold=True,sz=9), P('Accepted by -- ACME CORP PVT LTD',bold=True,sz=9)],
                 [P('_________________________\nVP Supply Chain and Procurement\nDIN: 00345612 | Emp: RIL-SC-00214\n01-April-2023',sz=8,col=MG),
                  P('_________________________\nDirector / Authorised Signatory\nDSC Token: ACME-DSC-2023\n03-April-2023',sz=8,col=MG)]],
                colWidths=[8*cm,8*cm])
    sig.setStyle(TableStyle([('VALIGN',(0,0),(-1,-1),'TOP'),('LINEAFTER',(0,0),(0,-1),0.5,BR),('LEFTPADDING',(1,0),(1,-1),20)]))
    s.append(sig)
    FTR(s, 'https://www.ril.com/vendor-portal')
    d.build(s); print('  work_order_1.pdf')


def wo2():
    p = os.path.join(OUT, 'work_order_2.pdf'); d = D(p); s = []
    hdr = Table([[P('OIL AND NATURAL GAS CORPORATION LIMITED\nA Navratna CPSE -- Govt of India\nCIN: L74899DL1993GOI054155\nGST No.: 05AABCO1505F1ZZ', bold=True, sz=9, col=G),
                  P('PURCHASE ORDER\nRef: ONGC/WZ/PROC/2022/WO-1187\nDate: 15-Sep-2022\nFY: 2022-23', sz=9, al=TA_RIGHT, col=G)]],
                colWidths=[9*cm,7*cm])
    hdr.setStyle(TableStyle([('VALIGN',(0,0),(-1,-1),'TOP')])); s.append(hdr)
    s += [HRFlowable(width='100%',thickness=2,color=G), Spacer(1,0.2*cm),
          H('PURCHASE ORDER -- ANNUAL MAINTENANCE CONTRACT (AMC)', 12, G), Spacer(1,0.2*cm),
          P('<b>To M/s:</b>', sz=9), P('ACME CORP PRIVATE LIMITED', bold=True, sz=11, col=B),
          P('Unit 7, Bandra-Kurla Complex, Mumbai 400051 | GSTIN: 27ACMEC1234Q1ZV', sz=8), Spacer(1,0.25*cm)]
    rows = [
        ('PO Ref. No.', 'ONGC/WZ/PROC/2022/WO-1187'),
        ('Tender Ref.', 'ONGC/WZ/TND/2022/AMC-PUMP-071'),
        ('Vendor Code (SAP)', 'VND-ONGC-WZ-00512'),
        ('Description', 'Comprehensive Annual Maintenance Contract for centrifugal pump stations at Uran Processing Plant -- Preventive maintenance, 4-hour breakdown SLA, OEM spares supply, Thermography and Vibration analysis per ISO 10816-3'),
        ('Contract Period', '12 months -- 15-Sep-2022 to 14-Sep-2023'),
        ('Contract Value (Lump Sum)', 'INR 1,75,00,000/- (One Crore Seventy-Five Lakh)', True, G),
        ('IGST @ 18%', 'INR 31,50,000/-'),
        ('Total (incl. GST)', 'INR 2,06,50,000/-'),
        ('Performance Guarantee', '5% of contract value -- BG No. SBI-2022-BG-00231'),
        ('LD Clause', 'INR 5,000/- per hour for SLA breach beyond 4 hrs'),
        ('Applicable Standards', 'OISD-STD-108; ASME B73.1; IS 1520:2019'),
        ('Status', 'EXECUTED AND CLOSED -- Final Payment Settled 10-Mar-2023', True, G),
    ]
    s += [KV(rows, hdr=('Clause','Details')), Spacer(1,0.3*cm),
          P('_________________________\n<b>For ONGC Limited</b>\nGM (Procurement) -- Western Offshore\nEmployee: ONGC-WZ-00782\nDated: 15-September-2022', sz=8, col=MG)]
    FTR(s, 'https://tender.ongc.co.in')
    d.build(s); print('  work_order_2.pdf')


def wo3():
    p = os.path.join(OUT, 'work_order_3.pdf'); d = D(p); s = []
    hdr = Table([[P('HINDUSTAN PETROLEUM CORPORATION LIMITED\nA Maharatna CPSE -- Ministry of Petroleum and Natural Gas\nCIN: L23201MH1952GOI008858\nGST No.: 27AAACH4366J1ZV', bold=True, sz=9, col=O),
                  P('CONTRACT AGREEMENT\nRef: HPCL/MR/PROC/2024/WO-1452\nDate: 10-Dec-2024\nFY: 2024-25', sz=9, al=TA_RIGHT, col=O)]],
                colWidths=[9*cm,7*cm])
    hdr.setStyle(TableStyle([('VALIGN',(0,0),(-1,-1),'TOP')])); s.append(hdr)
    s += [HRFlowable(width='100%',thickness=2,color=O), Spacer(1,0.2*cm),
          H('CONTRACT FOR SUPPLY AND ERECTION OF HIGH-PRESSURE PIPELINE SYSTEMS', 11, O), Spacer(1,0.2*cm),
          P('<b>To M/s:</b>', sz=9), P('ACME CORP PRIVATE LIMITED', bold=True, sz=11, col=B),
          P('Unit 7, Bandra-Kurla Complex, Mumbai 400051 | GSTIN: 27ACMEC1234Q1ZV', sz=8), Spacer(1,0.25*cm)]
    rows = [
        ('Contract No.', 'HPCL/MR/PROC/2024/WO-1452'),
        ('Tender Ref.', 'HPCL/MR/TND/2024/PIPE-0094'),
        ('SAP WBS Element', 'P-HPCL-MR-2024-PL-094'),
        ('Description', 'Engineering, Procurement, Supply, Erection, Testing and Commissioning (EPSC) of DN 300/PN 40 High-Pressure Liquid Transport Pipeline at Mumbai Refinery Unit-V -- 2,400 running metres incl. isolation valves, expansion joints, cathodic protection per NACE SP0169-2013'),
        ('Contract Type', 'Lump Sum Turnkey (LSTK)'),
        ('Contract Value (ex-GST)', 'INR 3,50,00,000/- (Three Crore Fifty Lakh)', True, O),
        ('IGST @ 18%', 'INR 63,00,000/-'),
        ('Total (incl. GST)', 'INR 4,13,00,000/-'),
        ('Completion Schedule', '165 calendar days from LOA -- 25-May-2025'),
        ('Defect Liability Period (DLP)', '12 months from Mechanical Completion Certificate (MCC)'),
        ('Applicable Standards', 'ASME B31.3; IS 1239; IS 3589; NACE SP0169-2013'),
        ('Insurance', 'CAR Policy + TPL -- Sum Insured min. INR 5 Crore'),
        ('Status', 'EXECUTED -- MCC Issued 22-May-2025; DLP Running', True, G),
    ]
    s += [KV(rows, hdr=('Clause','Details')), Spacer(1,0.3*cm),
          P('_________________________\n<b>For HPCL</b>\nDGM (Projects) -- Mumbai Refinery\nEmployee No.: HPCL-MR-00341\nDated: 10-December-2024', sz=8, col=MG)]
    FTR(s, 'https://www.hindustanpetroleum.com/tenders')
    d.build(s); print('  work_order_3.pdf')


def wo_unsigned():
    p = os.path.join(OUT, 'work_order_unsigned.pdf'); d = D(p); s = []
    s += [H('BHARAT SANCHAR NIGAM LIMITED (BSNL)', 13, B),
          H('A Government of India Undertaking -- Dept. of Telecommunications', 9, B, bold=False),
          HRFlowable(width='100%',thickness=2,color=B),
          H('PURCHASE ORDER -- NETWORKING INFRASTRUCTURE EQUIPMENT', 11, B), Spacer(1,0.2*cm),
          P('<b>To M/s:</b>', sz=9), P('ECHO ENTERPRISES', bold=True, sz=11, col=R), Spacer(1,0.2*cm)]
    rows = [
        ('PO Ref. No.', 'BSNL/CHQ/PROC/2024/WO-9999'),
        ('Description', 'Supply of 48-Port PoE+ Gigabit Managed Switches (L3), Core Routers (MPLS/BGP capable), and SFP+ transceivers conforming to ITU-T G.711 and IEEE 802.3at standards'),
        ('Quantity', '25 Switches + 06 Core Routers + Ancillaries'),
        ('Total PO Value (incl. GST)', 'INR 4,20,00,000/- (Four Crore Twenty Lakh)'),
        ('IGST @ 18% (SAC 85176990)', 'INR 64,06,780/-'),
        ('Delivery Schedule', '90 days from PO -- 31-March-2024'),
        ('Payment Terms', '60% against Bill of Lading; 40% after UAT sign-off'),
        ('PBG Required', '10% of PO value -- Valid 24 months'),
        ('Status', 'EXECUTED -- Final Acceptance Certificate: 10-Oct-2024', True, G),
    ]
    s += [KV(rows, hdr=('Clause','Details')), Spacer(1,0.5*cm),
          P('Authorised Signatory:', bold=True, sz=9), Spacer(1,1.5*cm),
          P('Name: ____________________________         Designation: ____________________________', sz=9, col=MG), Spacer(1,0.4*cm),
          P('Date: ____________________________          Seal/Stamp: ____________________________', sz=9, col=MG)]
    FTR(s, 'https://www.bsnl.co.in/tenders')
    d.build(s); print('  work_order_unsigned.pdf')


def gst():
    p = os.path.join(OUT, 'gst_demo.pdf'); d = D(p); s = []
    s += [H('GOVERNMENT OF INDIA', 11, B),
          H('MINISTRY OF FINANCE -- DEPARTMENT OF REVENUE', 9, B),
          H('GOODS AND SERVICES TAX NETWORK (GSTN)', 9, B),
          HRFlowable(width='100%',thickness=2,color=B),
          H('CERTIFICATE OF REGISTRATION -- FORM GST REG-06', 13, B),
          P('[Rule 10(1) of the Central GST Rules, 2017 (as amended)]', 7, col=MG, al=TA_CENTER),
          Spacer(1,0.3*cm), BAN('GSTIN','27ACMEC1234Q1ZV'), Spacer(1,0.3*cm)]
    rows = [
        ('Legal Name (as per PAN)', 'ACME CORP PRIVATE LIMITED'),
        ('Trade Name', 'ACME CORP'),
        ('PAN', 'ACMEC1234Q'),
        ('Constitution of Business', 'Private Limited Company -- Companies Act, 2013'),
        ('Type of Registration', 'Regular Taxpayer (Non-Composition) -- Eligible for B2G contracts'),
        ('Principal Place of Business', 'Unit 7, Bandra-Kurla Complex, Bandra (East), Mumbai 400051'),
        ('Nature of Business', 'Manufacturer/Supplier -- Industrial Pumps and Fluid Handling Equipment'),
        ('HSN / SAC Codes', '8413 -- Pumps for Liquids; 8414 -- Air/Gas Pumps; 9987 -- Maintenance Services'),
        ('Date of Liability', '01-April-2017'),
        ('Period of Validity', '01-April-2017 to Till Cancellation'),
        ('Approving Authority', 'Asst. Commissioner, Ward 27, GST Mumbai-West Commissionerate'),
        ('Date of Issue', '03-April-2017'),
        ('GSTIN Status', 'ACTIVE -- Returns Filed Regularly', True, G),
    ]
    s += [KV(rows, hdr=('Field','Details')), Spacer(1,0.3*cm),
          P('Important: Regular taxpayer status is mandatory for B2G (Business-to-Government) supply contracts. Composition scheme taxpayers cannot collect GST from recipients and are NOT eligible for government procurement.', 7.5, al=TA_JUSTIFY)]
    s.append(SIG_STAMP()); FTR(s, 'https://www.gst.gov.in/taxpayerSearch', 'Verify GSTIN status at GST Portal before reliance on this certificate.')
    d.build(s); print('  gst_demo.pdf')


def udyam():
    p = os.path.join(OUT, 'udyam_demo.pdf'); d = D(p); s = []
    s += [H('GOVERNMENT OF INDIA', 12, N),
          H('Ministry of Micro, Small and Medium Enterprises', 10, N),
          HRFlowable(width='100%',thickness=3,color=O),
          H('UDYAM REGISTRATION CERTIFICATE', 16, N),
          HRFlowable(width='100%',thickness=1,color=O), Spacer(1,0.25*cm)]
    urn = Table([[P('UDYAM REGISTRATION NUMBER',bold=True,sz=9,col=N,al=TA_CENTER)],
                 [P('UDYAM-MH-27-0054781',bold=True,sz=22,col=O,al=TA_CENTER)]],
                colWidths=[16*cm])
    urn.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,-1),colors.HexColor('#e3f2fd')),('BOX',(0,0),(-1,-1),2,N),('ALIGN',(0,0),(-1,-1),'CENTER'),('TOPPADDING',(0,0),(-1,-1),8),('BOTTOMPADDING',(0,0),(-1,-1),8)]))
    s += [urn, Spacer(1,0.35*cm)]
    fields = [
        ('Name of Enterprise', 'ACME CORP PRIVATE LIMITED'),
        ('Type of Organisation', 'Private Limited Company -- Companies Act, 2013'),
        ('CIN', 'U29299MH2014PTC254781'),
        ('PAN', 'ACMEC1234Q'),
        ('Date of Incorporation', '12-March-2014'),
        ('Major Activity', 'Manufacturing -- Pumps and Fluid Handling Equipment'),
        ('NIC Code (2-digit)', '28 -- Manufacture of Machinery and Equipment NEC'),
        ('NIC Code (5-digit)', '28131 -- Manufacture of Centrifugal Pumps for Liquids'),
        ('Investment in Plant and Machinery', 'INR 48,00,000/- (Forty-Eight Lakh)'),
        ('Annual Turnover (last IT Return)', 'INR 12,00,00,000/- (Twelve Crore)'),
        ('State / UT', 'Maharashtra'),
        ('District', 'Mumbai (Suburban)'),
        ('Date of Udyam Registration', '15-April-2021'),
        ('Enterprise Classification', 'MICRO ENTERPRISE -- Turnover <= INR 25 Crore; Investment <= INR 1 Crore'),
    ]
    tbl = [[P('Field',bold=True,sz=9,col=colors.white), P('Details',bold=True,sz=9,col=colors.white)]]
    for label, value in fields:
        is_class = 'MICRO' in value
        tbl.append([P(label,bold=True,sz=8), P(value,bold=is_class,sz=8 if not is_class else 9, col=G if is_class else colors.black)])
    det = Table(tbl, colWidths=[7.5*cm,8.5*cm])
    det.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),N),('BACKGROUND',(0,-1),(-1,-1),colors.HexColor('#e8f5e9')),('ROWBACKGROUNDS',(0,1),(-1,-2),[colors.white,GR]),('GRID',(0,0),(-1,-1),0.4,BR),('TOPPADDING',(0,0),(-1,-1),5),('BOTTOMPADDING',(0,0),(-1,-1),5),('LEFTPADDING',(0,0),(-1,-1),8),('VALIGN',(0,0),(-1,-1),'MIDDLE')]))
    s += [det, Spacer(1,0.3*cm),
          P('Issued under MSME Development Act, 2006 and Udyam Registration Notification dated 26-June-2020 (S.O. 2119(E)). Classification based on composite criteria of investment in plant and machinery and annual turnover per revised MSME definition w.e.f. 01-July-2020. Any suppression of facts may lead to de-registration under Section 11 of the MSMED Act, 2006.', 7.5, al=TA_JUSTIFY)]
    s.append(SIG_STAMP()); FTR(s, 'https://udyamregistration.gov.in', 'This certificate does not require physical signature or stamp.')
    d.build(s); print('  udyam_demo.pdf')


def gstr3b():
    p = os.path.join(OUT, 'gstr3b_demo.pdf'); d = D(p); s = []
    s += [H('GOODS AND SERVICES TAX NETWORK (GSTN)', 12, B),
          H('Ministry of Finance, Dept. of Revenue, Government of India', 9, B),
          HRFlowable(width='100%',thickness=2,color=B),
          H('FORM GSTR-3B -- MONTHLY RETURN ACKNOWLEDGEMENT', 12, B),
          P('[Sec. 39(1) of CGST Act, 2017 read with Rule 61 of CGST Rules, 2017]', 7, col=MG, al=TA_CENTER),
          Spacer(1,0.3*cm), BAN('GSTIN','27ACMEC1234Q1ZV'), Spacer(1,0.3*cm)]
    rows = [
        ('Legal Name of Taxpayer', 'ACME CORP PRIVATE LIMITED'),
        ('Return Period', 'July 2026 (07/2026)'),
        ('Date of Filing', '19-Aug-2026 (within statutory due date of 20-Aug-2026)'),
        ('Mode of Filing', 'Online -- GST Portal with DSC (Digital Signature Certificate)'),
        ('ARN (Acknowledgement Reference No.)', 'AA27082026000123456'),
        ('Filing Status', 'FILED -- Returns submitted successfully', True, G),
    ]
    s += [KV(rows, hdr=('Field','Details')), Spacer(1,0.3*cm),
          P('<b>Table 3.1(a) -- Outward Taxable Supplies:</b>  Taxable Value: INR 98,50,000/-  |  CGST: INR 8,86,500/-  |  SGST: INR 8,86,500/-', 8), Spacer(1,0.1*cm),
          P('<b>Table 4 -- ITC Claimed:</b>  IGST: INR 3,24,000/-  |  CGST: INR 1,82,500/-  |  SGST: INR 1,82,500/-', 8), Spacer(1,0.1*cm),
          P('<b>Net Tax Payable After ITC:</b>  CGST -- INR 7,22,900/-  |  SGST -- INR 7,22,900/-', 8), Spacer(1,0.1*cm),
          P('<b>Challan Reference:</b>  CIR2026082700123456  |  Date of Payment: 18-Aug-2026', 8), Spacer(1,0.3*cm),
          P('Late filing of GSTR-3B attracts late fee of INR 50/- per day under Section 47 of the CGST Act, 2017. Interest on delayed payment is levied @ 18% p.a. under Section 50. Continuous 12-month filing history is mandatory for GeM/Central Government procurement eligibility.', 7.5, al=TA_JUSTIFY)]
    s.append(SIG_STAMP()); FTR(s, 'https://www.gst.gov.in/returns', 'ARN is the unique identifier for this filing. Verify at gst.gov.in.')
    d.build(s); print('  gstr3b_demo.pdf')


def debarment():
    p = os.path.join(OUT, 'debarment_demo.pdf'); d = D(p); s = []
    s += [H('GOVERNMENT OF INDIA -- MINISTRY OF FINANCE', 11, R),
          H('DEPARTMENT OF EXPENDITURE -- PUBLIC PROCUREMENT DIVISION', 10, R),
          H('CENTRAL VIGILANCE COMMISSION -- VENDOR INTEGRITY REGISTRY', 9, R, bold=False),
          HRFlowable(width='100%',thickness=3,color=R),
          H('NOTICE OF DEBARMENT / BLACKLISTING', 16, R),
          P('[Rule 151 of the General Financial Rules (GFR) 2017 -- Suspension and Debarment of Vendors]', 8, col=MG, al=TA_CENTER),
          Spacer(1,0.3*cm), BAN('CVC Debarment Registry No.','CVC/PPD/DB/2024/00147', R, R, bg=colors.HexColor('#fdecea')), Spacer(1,0.3*cm)]
    rows = [
        ('Name of Debarred Entity', 'GAMMA TECHNOLOGIES PRIVATE LIMITED'),
        ('PAN of Entity', 'BKKPA1234F'),
        ('CIN', 'U72900KA2015PTC082341'),
        ('Registered Office', 'Survey No. 18, Electronics City Phase-I, Bengaluru 560100'),
        ('GSTIN', '29BKKPA1234F1ZR'),
        ('Basis of Debarment', 'Rule 151(iii) GFR 2017 -- Fraudulent misrepresentation of MSME status and submission of fabricated technical qualification documents in Tender No. DRDO/PY/2024/ELEC-089. FIR No. CR-0284/2024 registered with CBI-ACB, Bengaluru.'),
        ('Debarring Authority', 'Ministry of Finance, Dept. of Expenditure -- Secretary (Expenditure)'),
        ('Date of Debarment Order', '15-February-2024'),
        ('Period of Debarment', '15-February-2024 to 14-February-2027 (Three years)', True, R),
        ('Scope of Debarment', 'ALL Central Government Ministries, CPSEs, Autonomous Bodies, and GeM Portal -- Nationwide'),
        ('Associated Entities Debarred', 'Gamma Tech Solutions (Prop.), Reg. No. MH14C02345 -- Sister entity under same management'),
        ('GeM Portal Action', 'Account suspended -- GSTIN blocked on Government e-Marketplace'),
        ('CVC Case Reference', 'CVC Case No. 002/VIC/24 -- Under Active Vigilance Inquiry'),
        ('Current Status', 'ACTIVELY DEBARRED -- All procurement agencies notified', True, R),
        ('Registry Last Updated', '01-September-2026'),
    ]
    s += [KV(rows, hdr=('Field','Details')), Spacer(1,0.3*cm),
          P('Statutory Warning: Any procurement entity that knowingly awards a contract to a debarred vendor shall be liable under Rule 154 of GFR 2017 and the Prevention of Corruption Act, 1988. Vendors attempting to participate through shell or associated entities during debarment are liable to prosecution under Section 420 IPC and Section 13(2) of the PC Act, 1988.', 7.5, col=colors.black, al=TA_JUSTIFY)]
    s.append(SIG_STAMP()); FTR(s, 'https://mofdoe.gov.in/debarment-registry', 'This debarment is mandatory to check before award of any Government contract.')
    d.build(s); print('  debarment_demo.pdf')


print('Generating all 13 realistic demo documents...')
ca_turnover()
epfo()
esic()
startup_india()
nsic()
wo1()
wo2()
wo3()
wo_unsigned()
gst()
udyam()
gstr3b()
debarment()
print('All 13 documents generated successfully.')
