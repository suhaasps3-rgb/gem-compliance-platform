import zipfile
import os
import shutil

# Make sure all demo docs exist
os.system("python generate_demo_docs.py")

base_dir = "frontend/public"
output_zip = "batch_demo.zip"

bidders = {
    "Acme_Innovations": [
        ("work_order_3.pdf", "Work_Order_Large.pdf"), # 8.5 Cr
        ("epfo_demo.pdf", "EPFO_Statement.pdf"),
        ("ca_turnover.pdf", "CA_Turnover.pdf"),
        ("technical_catalog.pdf", "Technical_Spec.pdf")
    ],
    "Delta_Solutions": [
        ("work_order_1.pdf", "Work_Order_Small.pdf"), # 2.1 Cr
        ("esic_demo.pdf", "ESIC_Statement.pdf"),
        ("nsic_demo.pdf", "NSIC_Certificate.pdf")
    ],
    "Echo_Enterprises": [
        ("startup_india_demo.pdf", "Startup_India.pdf"), # Revoked
        ("work_order_2.pdf", "Work_Order_Mid.pdf") # 4.5 Cr
    ],
    "Foxtrot_Systems": [
        ("epfo_demo.pdf", "EPFO.pdf"),
        ("work_order_1.pdf", "PO_1.pdf"),
        ("work_order_2.pdf", "PO_2.pdf") # 2.1 + 4.5 = 6.6 Cr
    ],
    "Theta_Logistics": [
        ("ca_turnover.pdf", "Turnover.pdf")
    ]
}

with zipfile.ZipFile(output_zip, 'w') as zf:
    for bidder, files in bidders.items():
        # Just create the folder entry implicitly by adding files
        for src, dst in files:
            src_path = os.path.join(base_dir, src)
            if os.path.exists(src_path):
                zf.write(src_path, arcname=f"{bidder}/{dst}")
            else:
                print(f"Missing {src_path}")

print("Created diverse batch_demo.zip")
