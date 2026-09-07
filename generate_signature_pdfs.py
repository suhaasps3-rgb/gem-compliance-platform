import os
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.colors import blue, black, red

def draw_signature(c, x, y, name, role):
    # Blue ink signature
    c.setFont("Helvetica-BoldOblique", 14)
    c.setFillColor(blue)
    c.drawString(x, y + 15, f"[ SIGNED & STAMPED ]")
    c.setFont("Helvetica-Oblique", 18)
    c.drawString(x, y - 5, f"{name}")
    
    # Black text below
    c.setFont("Helvetica", 12)
    c.setFillColor(black)
    c.drawString(x, y - 25, role)

def generate_pdf(filename, title, content_lines, sign=False, sign_name="John Doe", sign_role="Authorized Signatory"):
    c = canvas.Canvas(filename, pagesize=A4)
    c.setFont("Helvetica-Bold", 16)
    c.drawString(50, 800, title)
    
    c.setFont("Helvetica", 12)
    y = 760
    for line in content_lines:
        c.drawString(50, y, line)
        y -= 20
        
    if sign:
        draw_signature(c, 50, 150, sign_name, sign_role)
        
    c.save()

output_dir = r"C:\Users\Suhaas\Downloads\GeM_Compliance_Test_Files\Signature_Testing"
os.makedirs(output_dir, exist_ok=True)

# 1. CA Turnover
content = [
    "CERTIFICATE OF TURNOVER",
    "",
    "We have reviewed the books of accounts of Acme Corp.",
    "The turnover for the last 3 financial years is as follows:",
    "FY 2023-24: 5.2 Crore",
    "FY 2024-25: 6.1 Crore",
    "FY 2025-26: 7.5 Crore",
    "",
    "UDIN: 23123456ABCDEF7890"
]
generate_pdf(os.path.join(output_dir, "turnover_signed.pdf"), "CA TURNOVER CERTIFICATE", content, True, "CA Rahul Sharma", "Chartered Accountant (M.No: 123456)")
generate_pdf(os.path.join(output_dir, "turnover_unsigned.pdf"), "CA TURNOVER CERTIFICATE", content, False)

# 2. Work Order
content = [
    "WORK ORDER / CONTRACT AGREEMENT",
    "Order No: WO-2025-998",
    "Client: Ministry of Defence",
    "Vendor: Acme Corp",
    "",
    "This is to certify that Acme Corp has successfully supplied",
    "goods worth 5.0 Crore."
]
generate_pdf(os.path.join(output_dir, "work_order_signed.pdf"), "WORK ORDER", content, True, "Director of Procurement", "Ministry of Defence, Govt of India")
generate_pdf(os.path.join(output_dir, "work_order_unsigned.pdf"), "WORK ORDER", content, False)

# 3. Technical Catalog
content = [
    "TECHNICAL SPECIFICATIONS - ACME PUMP X200",
    "",
    "Product Name: Catalog Item",
    "Pump Capacity: 520 L/min",
    "Pressure: 22 bar",
    "Efficiency: 91%",
    "Voltage: 415V"
]
generate_pdf(os.path.join(output_dir, "technical_signed.pdf"), "PRODUCT DATASHEET", content, True, "Jane Smith", "Technical Director, Acme Corp")
generate_pdf(os.path.join(output_dir, "technical_unsigned.pdf"), "PRODUCT DATASHEET", content, False)

# 4. MII Declaration
content = [
    "MAKE IN INDIA (MII) LOCAL CONTENT DECLARATION",
    "",
    "Entity Name: Acme Corp",
    "We hereby declare that the local content in our",
    "offered product is 65%.",
    "",
    "We qualify as a Class-I Local Supplier under the",
    "Public Procurement (Preference to Make in India) Order."
]
generate_pdf(os.path.join(output_dir, "mii_signed.pdf"), "MII DECLARATION", content, True, "John Doe", "CEO, Acme Corp")
generate_pdf(os.path.join(output_dir, "mii_unsigned.pdf"), "MII DECLARATION", content, False)

# 5. Debarment
content = [
    "SELF-DECLARATION OF NON-DEBARMENT",
    "",
    "Entity Name: Acme Corp",
    "We hereby declare that our company is not blacklisted",
    "or debarred by any Govt department, PSU, or autonomous",
    "body as of the date of submission of this bid."
]
generate_pdf(os.path.join(output_dir, "debarment_signed.pdf"), "DEBARMENT DECLARATION", content, True, "John Doe", "CEO, Acme Corp")
generate_pdf(os.path.join(output_dir, "debarment_unsigned.pdf"), "DEBARMENT DECLARATION", content, False)

print("PDFs generated successfully at:", output_dir)
