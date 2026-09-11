import zipfile
import os
import shutil

base_dir = "frontend/public"
output_zip = "batch_demo.zip"

bidders = {
    "Acme_Corp": [
        ("ca_turnover_acme.pdf", "CA_Turnover.pdf"),
        ("epfo_demo.pdf", "EPFO_Statement.pdf"),
        ("esic_demo.pdf", "ESIC_Statement.pdf"),
        ("startup_india_demo.pdf", "Startup_India.pdf"),
        ("nsic_demo.pdf", "NSIC_Certificate.pdf"),
        ("work_order_1.pdf", "Work_Order_1.pdf"),
        ("work_order_2.pdf", "Work_Order_2.pdf"),
        ("work_order_3.pdf", "Work_Order_3.pdf"),
        ("work_order_unsigned.pdf", "Work_Order_Unsigned.pdf"),
        ("gst_demo.pdf", "GST_Certificate.pdf"),
        ("udyam_demo.pdf", "Udyam_Certificate.pdf"),
        ("gstr3b_demo.pdf", "GSTR3B_Statement.pdf"),
        ("debarment_demo.pdf", "Debarment_Notice.pdf"),
        ("tender_demo.pdf", "Tender_Document.pdf")
    ],
    "Beta_LLC": [
        ("ca_turnover_beta.pdf", "CA_Turnover.pdf"),
        ("epfo_demo.pdf", "EPFO_Statement.pdf"),
        ("esic_demo.pdf", "ESIC_Statement.pdf"),
        ("startup_india_demo.pdf", "Startup_India.pdf"),
        ("nsic_demo.pdf", "NSIC_Certificate.pdf"),
        ("work_order_1.pdf", "Work_Order_1.pdf"),
        ("work_order_2.pdf", "Work_Order_2.pdf"),
        ("work_order_3.pdf", "Work_Order_3.pdf"),
        ("work_order_unsigned.pdf", "Work_Order_Unsigned.pdf"),
        ("gst_demo.pdf", "GST_Certificate.pdf"),
        ("udyam_demo.pdf", "Udyam_Certificate.pdf"),
        ("gstr3b_demo.pdf", "GSTR3B_Statement.pdf"),
        ("debarment_demo.pdf", "Debarment_Notice.pdf"),
        ("tender_demo.pdf", "Tender_Document.pdf")
    ],
    "Gamma_Technologies": [
        ("ca_turnover_gamma.pdf", "CA_Turnover.pdf"),
        ("epfo_demo.pdf", "EPFO_Statement.pdf"),
        ("esic_demo.pdf", "ESIC_Statement.pdf"),
        ("startup_india_demo.pdf", "Startup_India.pdf"),
        ("nsic_demo.pdf", "NSIC_Certificate.pdf"),
        ("work_order_1.pdf", "Work_Order_1.pdf"),
        ("work_order_2.pdf", "Work_Order_2.pdf"),
        ("work_order_3.pdf", "Work_Order_3.pdf"),
        ("work_order_unsigned.pdf", "Work_Order_Unsigned.pdf"),
        ("gst_demo.pdf", "GST_Certificate.pdf"),
        ("udyam_demo.pdf", "Udyam_Certificate.pdf"),
        ("gstr3b_demo.pdf", "GSTR3B_Statement.pdf"),
        ("debarment_demo.pdf", "Debarment_Notice.pdf"),
        ("tender_demo.pdf", "Tender_Document.pdf")
    ]
}

with zipfile.ZipFile(output_zip, 'w') as zf:
    for bidder, files in bidders.items():
        for src, dst in files:
            src_path = os.path.join(base_dir, src)
            if os.path.exists(src_path):
                zf.write(src_path, arcname=f"{bidder}/{dst}")
            else:
                print(f"Missing {src_path}")

print("Created diverse batch_demo.zip")

targets = [
    r"C:\Users\Suhaas\OneDrive\Desktop\batch_demo.zip",
    r"C:\Users\Suhaas\Desktop\batch_demo.zip",
    r"C:\Users\Suhaas\Downloads\batch_demo.zip"
]
for t in targets:
    try:
        os.makedirs(os.path.dirname(t), exist_ok=True)
        shutil.copyfile(output_zip, t)
        print(f"Copied batch_demo.zip to {t}")
    except Exception as e:
        pass
