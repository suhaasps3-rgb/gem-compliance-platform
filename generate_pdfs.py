from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.colors import blue, black
import os

def draw_signature(c, x, y):
    # Draw blue ink signature to pass the visual authenticity checker
    c.setStrokeColor(blue)
    c.setLineWidth(2)
    # Draw a squiggly line resembling a signature
    path = c.beginPath()
    path.moveTo(x, y)
    path.curveTo(x+20, y+20, x+40, y-10, x+60, y+10)
    path.curveTo(x+80, y+30, x+100, y-20, x+120, y+5)
    c.drawPath(path)
    # Add a blue stamp
    c.setFillColor(blue)
    c.setFont("Helvetica-Bold", 10)
    c.drawString(x, y-20, "[ SIGNED & STAMPED ]")
    # Reset to black
    c.setFillColor(black)
    c.setStrokeColor(black)
    c.setFont("Helvetica", 12)

def generate_gstr3b(filename):
    c = canvas.Canvas(filename, pagesize=letter)
    c.setFont("Helvetica-Bold", 16)
    c.drawString(200, 750, "FORM GSTR-3B")
    c.setFont("Helvetica", 12)
    c.drawString(100, 700, "GSTIN: 27ACME1234Q1Z5")
    c.drawString(100, 680, "Legal Name: Acme Corp")
    c.drawString(100, 660, "Return Period: August 2026")
    c.drawString(100, 620, "3.1 Details of Outward Supplies")
    c.drawString(100, 600, "(a) Total Taxable Value: Rs. 10,00,000")
    c.drawString(100, 580, "(b) Total Tax Paid: Rs. 2,45,000")
    c.drawString(100, 540, "Status: FILED")
    c.drawString(100, 520, "Date of Filing: 15-09-2026")
    
    # Add signature block at the bottom
    c.drawString(100, 400, "Authorized Signatory:")
    draw_signature(c, 100, 360)
    
    c.showPage()
    c.save()

def generate_debarment(filename):
    c = canvas.Canvas(filename, pagesize=letter)
    c.setFont("Helvetica-Bold", 16)
    c.drawString(150, 750, "SELF-DECLARATION OF NON-DEBARMENT")
    c.setFont("Helvetica", 12)
    c.drawString(100, 700, "Date: 01-09-2026")
    c.drawString(100, 670, "To whomsoever it may concern,")
    c.drawString(100, 640, "We, Acme Corp, hereby declare that our company is not blacklisted")
    c.drawString(100, 620, "or debarred by any Government department, PSU, or autonomous body")
    c.drawString(100, 600, "as of the date of submission of this bid.")
    
    c.drawString(100, 500, "Authorized Signatory,")
    draw_signature(c, 100, 460)
    c.drawString(100, 420, "John Doe")
    c.drawString(100, 400, "CEO, Acme Corp")
    
    c.showPage()
    c.save()

os.makedirs('backend/static', exist_ok=True)
generate_gstr3b('backend/static/gstr3b_demo.pdf')
generate_debarment('backend/static/debarment_demo.pdf')
