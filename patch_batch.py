import os

file_path = 'generate_batch_demo.py'
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

acme_insert = """
zf.writestr("Acme_Corp/itr_return.pdf", make_pdf(
    "INCOME TAX RETURN (ITR-6)",
    ["Assessment Year: 2025-26", "Name: Acme Corp Pvt Ltd", "PAN: BKKPA1234F", "Status: FILED"],
    "Income Tax Dept", "Digital Signature"
))
zf.writestr("Acme_Corp/mii_declaration.pdf", make_pdf(
    "MAKE IN INDIA (MII) LOCAL CONTENT DECLARATION",
    ["Entity: Acme Corp Pvt Ltd", "Supplier Class: Class-I Local Supplier", "Local Content: 70%", "Status: Certified"],
    "John Doe", "CEO, Acme Corp Pvt Ltd"
))
zf.writestr("Acme_Corp/gstr3b_return.pdf", make_pdf(
    "GSTR-3B MONTHLY RETURN",
    ["Entity: Acme Corp Pvt Ltd", "Period: August 2026", "Filing Status: FILED", "Tax Paid: INR 45,000"],
    "GSTN Authority", "Digital Signature"
))
zf.writestr("Acme_Corp/esic_challan.pdf", make_pdf(
    "ESIC MONTHLY CHALLAN",
    ["Employer: Acme Corp Pvt Ltd", "Period: August 2026", "Status: PAID"],
    "ESIC Dept", "Digital Stamp"
))
zf.writestr("Acme_Corp/startup_india_cert.pdf", make_pdf(
    "STARTUP INDIA RECOGNITION CERTIFICATE",
    ["Name: Acme Corp Pvt Ltd", "DIPP Number: DIPP12345", "Status: ACTIVE"],
    "DIPP Authority", "Digital Signature"
))
zf.writestr("Acme_Corp/nsic_certificate.pdf", make_pdf(
    "NSIC REGISTRATION CERTIFICATE",
    ["Name: Acme Corp Pvt Ltd", "Status: ACTIVE", "EMD Exemption: Supported"],
    "NSIC Official", "Digital Signature"
))
"""

beta_insert = """
zf.writestr("Beta_LLC/itr_return.pdf", make_pdf(
    "INCOME TAX RETURN (ITR-6)",
    ["Assessment Year: 2025-26", "Name: BETA LLC", "PAN: ABCDE5678G", "Status: FILED"],
    "Income Tax Dept", "Digital Signature"
))
zf.writestr("Beta_LLC/mii_declaration.pdf", make_pdf(
    "MAKE IN INDIA (MII) LOCAL CONTENT DECLARATION",
    ["Entity: BETA LLC", "Supplier Class: Class-I Local Supplier", "Local Content: 65%", "Status: Certified"],
    "Sanjay Verma", "Director, BETA LLC"
))
zf.writestr("Beta_LLC/gstr3b_return.pdf", make_pdf(
    "GSTR-3B MONTHLY RETURN",
    ["Entity: BETA LLC", "Period: August 2026", "Filing Status: FILED", "Tax Paid: INR 22,000"],
    "GSTN Authority", "Digital Signature"
))
zf.writestr("Beta_LLC/esic_challan.pdf", make_pdf(
    "ESIC MONTHLY CHALLAN",
    ["Employer: BETA LLC", "Period: August 2026", "Status: PAID"],
    "ESIC Dept", "Digital Stamp"
))
zf.writestr("Beta_LLC/startup_india_cert.pdf", make_pdf(
    "STARTUP INDIA RECOGNITION CERTIFICATE",
    ["Name: BETA LLC", "DIPP Number: DIPP67890", "Status: ACTIVE"],
    "DIPP Authority", "Digital Signature"
))
zf.writestr("Beta_LLC/nsic_certificate.pdf", make_pdf(
    "NSIC REGISTRATION CERTIFICATE",
    ["Name: BETA LLC", "Status: ACTIVE", "EMD Exemption: Supported"],
    "NSIC Official", "Digital Signature"
))
"""

gamma_insert = """
zf.writestr("Gamma_Tech/itr_return.pdf", make_pdf(
    "INCOME TAX RETURN (ITR-6)",
    ["Assessment Year: 2025-26", "Name: Gamma Technologies Pvt Ltd", "PAN: REAL9999X", "Status: FILED"],
    "Income Tax Dept", "Digital Signature"
))
zf.writestr("Gamma_Tech/mii_declaration.pdf", make_pdf(
    "MAKE IN INDIA (MII) LOCAL CONTENT DECLARATION",
    ["Entity: Gamma Technologies Pvt Ltd", "Supplier Class: Class-II", "Local Content: 40%", "Status: Certified"],
    "Gamma Auth", "Signatory"
))
zf.writestr("Gamma_Tech/gstr3b_return.pdf", make_pdf(
    "GSTR-3B MONTHLY RETURN",
    ["Entity: Gamma Technologies Pvt Ltd", "Period: April 2026", "Filing Status: PENDING", "Tax Paid: INR 0"],
    "GSTN Authority", "Digital Signature"
))
zf.writestr("Gamma_Tech/esic_challan.pdf", make_pdf(
    "ESIC MONTHLY CHALLAN",
    ["Employer: Gamma Technologies Pvt Ltd", "Period: August 2026", "Status: PENDING"],
    "ESIC Dept", "Digital Stamp"
))
zf.writestr("Gamma_Tech/debarment_declaration.pdf", make_pdf(
    "SELF-DECLARATION OF NON-DEBARMENT",
    ["Date: 01-09-2026", "We, Gamma Technologies Pvt Ltd, hereby declare..."],
    "Gamma Auth", "Signatory"
))
"""

if "itr_return.pdf" not in content:
    content = content.replace(
        '# BIDDER B: Beta_LLC',
        acme_insert + '\n# BIDDER B: Beta_LLC'
    )
    content = content.replace(
        '# BIDDER C: Gamma_Tech',
        beta_insert + '\n# BIDDER C: Gamma_Tech'
    )
    content = content.replace(
        'zf.close()',
        gamma_insert + '\nzf.close()'
    )

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)

print('generate_batch_demo.py patched successfully.')
