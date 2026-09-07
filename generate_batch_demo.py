"""
generate_batch_demo.py — Generates the 3-bidder batch demo ZIP file for pitching to judges.
Bidder A: Acme_Corp (Green — 100/100, Low Risk)
Bidder B: Beta_LLC (Yellow — 65/100, Medium Risk)
Bidder C: Gamma_Tech (Red — 10/100, Critical Risk)
"""
import os
import zipfile
import io
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.colors import blue, black

def draw_signature(c, x, y, name, role):
    c.setFont("Helvetica-BoldOblique", 14)
    c.setFillColor(blue)
    c.drawString(x, y + 15, "[ SIGNED & STAMPED ]")
    c.setFont("Helvetica-Oblique", 18)
    c.drawString(x, y - 5, name)
    c.setFont("Helvetica", 12)
    c.setFillColor(black)
    c.drawString(x, y - 25, role)

def make_pdf(title, lines, sign_name=None, sign_role=None):
    buf = io.BytesIO()
    c = canvas.Canvas(buf, pagesize=A4)
    c.setFont("Helvetica-Bold", 16)
    c.drawString(50, 800, title)
    c.setFont("Helvetica", 12)
    y = 760
    for line in lines:
        c.drawString(50, y, line)
        y -= 20
    if sign_name:
        draw_signature(c, 50, 150, sign_name, sign_role or "Authorized Signatory")
    c.save()
    return buf.getvalue()

output_path = r"C:\Users\Suhaas\Downloads\GeM_Compliance_Test_Files\batch_demo_3_bidders.zip"
os.makedirs(os.path.dirname(output_path), exist_ok=True)

zf = zipfile.ZipFile(output_path, 'w', zipfile.ZIP_DEFLATED)

# ═══════════════════════════════════════════════
# BIDDER A: Acme_Corp (Target: bidder-acme-001)
# Clean, fully verified supplier -> Score: 100 / LOW
# ═══════════════════════════════════════════════

zf.writestr("Acme_Corp/gst_certificate.pdf", make_pdf(
    "GST REGISTRATION CERTIFICATE (Form REG-06)",
    ["GSTIN: 27AABCA1234F1Z5",
     "Legal Name: Acme Corp Pvt Ltd",
     "Trade Name: Acme Corp",
     "Type of Registration: Regular",
     "Date of Registration: 01-04-2020",
     "State: Maharashtra",
     "Status: Active"]
))

zf.writestr("Acme_Corp/udyam_certificate.pdf", make_pdf(
    "UDYAM REGISTRATION CERTIFICATE",
    ["Udyam Registration Number: UDYAM-MH-01-0012345",
     "Enterprise Name: Acme Corp Pvt Ltd",
     "Type of Enterprise: Micro",
     "Major Activity: Manufacturing",
     "Turnover: INR 4.5 Crore"]
))

zf.writestr("Acme_Corp/epfo_ecr_statement.pdf", make_pdf(
    "EPFO ELECTRONIC CHALLAN CUM RETURN",
    ["Establishment Name: Acme Corp Pvt Ltd",
     "Employer Code: MHBAN0012345",
     "Wage Month: August-2026",
     "No of Employees: 48",
     "Total Contribution: Rs. 2,70,000",
     "Status: PAID"]
))

zf.writestr("Acme_Corp/work_order_ongc.pdf", make_pdf(
    "WORK ORDER",
    ["Work Order No: WO-2024-ONGC-447",
     "Order Date: 15-03-2024",
     "Client: ONGC Corporation",
     "Vendor: Acme Corp Pvt Ltd",
     "Order Value: INR 3.2 Crore",
     "Status: Completed"],
    "Director of Procurement", "ONGC Corporation"
))

zf.writestr("Acme_Corp/work_order_hpcl.pdf", make_pdf(
    "WORK ORDER",
    ["Work Order No: WO-2023-HPCL-889",
     "Order Date: 01-08-2023",
     "Client: HPCL Corporation",
     "Vendor: Acme Corp Pvt Ltd",
     "Order Value: INR 2.5 Crore",
     "Status: Completed"],
    "Chief Materials Manager", "HPCL Corporation"
))

zf.writestr("Acme_Corp/turnover_ca_certificate.pdf", make_pdf(
    "AUDITED BALANCE SHEET & TURNOVER CERTIFICATE",
    ["Company Name: Acme Corp Pvt Ltd",
     "Financial Year: 2024-25",
     "Annual Turnover: INR 8.50 Crore",
     "Name of CA: CA Rahul Sharma",
     "Membership No: 123456",
     "UDIN: 24123456ABCDEF9876"],
    "CA Rahul Sharma", "Chartered Accountant (FCA)"
))

zf.writestr("Acme_Corp/technical_catalog.pdf", make_pdf(
    "TECHNICAL SPECIFICATIONS — ACME PUMP X200",
    ["Product Name: Catalog Item",
     "Pump Capacity: 520 L/min",
     "Pressure: 22 bar",
     "Efficiency: 91%",
     "Voltage: 415V"],
    "Jane Smith", "Technical Director, Acme Corp Pvt Ltd"
))

zf.writestr("Acme_Corp/debarment_declaration.pdf", make_pdf(
    "SELF-DECLARATION OF NON-DEBARMENT",
    ["Date: 01-09-2026",
     "We, Acme Corp Pvt Ltd, hereby declare that our company",
     "is not blacklisted or debarred by any Government department,",
     "PSU, or autonomous body."],
    "John Doe", "CEO, Acme Corp Pvt Ltd"
))

# ═══════════════════════════════════════════════
# BIDDER B: Beta_LLC (Target: bidder-beta-002)
# Needs Review (1 contradiction: reported turnover mismatch) -> Score: 65 / MEDIUM
# ═══════════════════════════════════════════════

zf.writestr("Beta_LLC/gst_certificate.pdf", make_pdf(
    "GST REGISTRATION CERTIFICATE (Form REG-06)",
    ["GSTIN: 27AABCB2345G1Z6",
     "Legal Name: BETA LLC",
     "Trade Name: Beta Solutions",
     "Type of Registration: Regular",
     "State: Maharashtra",
     "Status: Active"]
))

zf.writestr("Beta_LLC/udyam_certificate.pdf", make_pdf(
    "UDYAM REGISTRATION CERTIFICATE",
    ["Udyam Registration Number: UDYAM-MH-02-0056789",
     "Enterprise Name: BETA LLC",
     "Type of Enterprise: Micro",
     "Major Activity: Services"]
))

zf.writestr("Beta_LLC/epfo_ecr_statement.pdf", make_pdf(
    "EPFO ELECTRONIC CHALLAN CUM RETURN",
    ["Establishment Name: BETA LLC",
     "Employer Code: MHBAN0056789",
     "Wage Month: August-2026",
     "Total Contribution: Rs. 1,50,000",
     "Status: PAID"]
))

zf.writestr("Beta_LLC/work_order_nhai.pdf", make_pdf(
    "WORK ORDER",
    ["Work Order No: WO-2024-NHAI-331",
     "Order Date: 10-02-2024",
     "Client: NHAI Corporation",
     "Vendor: BETA LLC",
     "Order Value: INR 5.5 Crore",
     "Status: Completed"],
    "Project Director", "NHAI Corporation"
))

zf.writestr("Beta_LLC/turnover_ca_certificate.pdf", make_pdf(
    "AUDITED BALANCE SHEET & TURNOVER CERTIFICATE",
    ["Company Name: BETA LLC",
     "Financial Year: 2024-25",
     "Annual Turnover: INR 4.80 Crore",
     "Name of CA: CA Sunil Mehta",
     "Membership No: 654321",
     "UDIN: 24654321ABCDEF1234"],
    "CA Sunil Mehta", "Chartered Accountant"
))

zf.writestr("Beta_LLC/technical_catalog.pdf", make_pdf(
    "TECHNICAL SPECIFICATIONS — BETA PUMP",
    ["Product Name: Catalog Item",
     "Pump Capacity: 505 L/min",
     "Pressure: 21 bar",
     "Efficiency: 90%",
     "Voltage: 415V"],
    "Sanjay Verma", "Director, BETA LLC"
))

zf.writestr("Beta_LLC/debarment_declaration.pdf", make_pdf(
    "SELF-DECLARATION OF NON-DEBARMENT",
    ["Date: 01-09-2026",
     "We, BETA LLC, hereby declare that our company",
     "is not blacklisted or debarred by any Government body."],
    "Sanjay Verma", "Director, BETA LLC"
))

# ═══════════════════════════════════════════════
# BIDDER C: Gamma_Tech (Target: bidder-gamma-003)
# Critical Fraud (Non-compliant: 2 contradictions) -> Score: 10 / CRITICAL
# ═══════════════════════════════════════════════

zf.writestr("Gamma_Tech/gst_certificate.pdf", make_pdf(
    "GST REGISTRATION CERTIFICATE (Form REG-06)",
    ["GSTIN: 33AABCG9012H1Z7",
     "Legal Name: Gamma Technologies Pvt Ltd",
     "Trade Name: Gamma Tech",
     "Type of Registration: Regular",
     "State: Tamil Nadu",
     "Status: Active"]
))

zf.writestr("Gamma_Tech/udyam_certificate.pdf", make_pdf(
    "UDYAM REGISTRATION CERTIFICATE",
    ["Udyam Registration Number: UDYAM-TN-03-0054321",
     "Enterprise Name: Gamma Technologies Pvt Ltd",
     "Type of Enterprise: Micro",
     "Major Activity: Manufacturing"]
))

zf.writestr("Gamma_Tech/work_order_unsigned.pdf", make_pdf(
    "WORK ORDER",
    ["Work Order No: WO-2024-BSNL-221",
     "Order Date: 01-02-2024",
     "Client: BSNL Corporation",
     "Vendor: Gamma Technologies Pvt Ltd",
     "Order Value: INR 1.5 Crore",
     "Status: In Progress"]
    # Unsigned
))

zf.writestr("Gamma_Tech/technical_datasheet.pdf", make_pdf(
    "PRODUCT SPECIFICATIONS — GAMMA PUMP",
    ["Product Name: Catalog Item",
     "Pump Capacity: 480 L/min",
     "Pressure: 18 bar",
     "Efficiency: 85%",
     "Voltage: 415V"]
))

zf.close()

print(f"Batch demo ZIP regenerated at: {output_path}")
