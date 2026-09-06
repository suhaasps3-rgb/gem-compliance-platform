import os
import zipfile
import shutil

ROOT = r'C:\Users\Suhaas\.gemini\antigravity\scratch\gem_compliance'
PUBLIC_DIR = os.path.join(ROOT, 'frontend', 'public')
ZIP_PATH = os.path.join(ROOT, 'batch_demo.zip')

bidders = [
    "Acme_Innovations",
    "Delta_Solutions",
    "Theta_Logistics",
    "Echo_Enterprises",
    "Foxtrot_Systems"
]

files_to_include = [
    "gst_tender_demo.pdf",
    "udyam_tender_demo.pdf",
    "epfo_demo.pdf",
    "work_order_1.pdf"
]

with zipfile.ZipFile(ZIP_PATH, 'w') as zf:
    for bidder in bidders:
        for f in files_to_include:
            source = os.path.join(PUBLIC_DIR, f)
            if os.path.exists(source):
                # Write to zip under the bidder's folder
                # rename generic files to something more realistic for the zip
                target_name = f
                if 'gst' in f: target_name = "GST_Certificate.pdf"
                elif 'udyam' in f: target_name = "Udyam_Registration.pdf"
                elif 'epfo' in f: target_name = "EPFO_Statement.pdf"
                elif 'work_order' in f: target_name = "WorkOrder_01.pdf"
                
                arcname = f"{bidder}/{target_name}"
                zf.write(source, arcname)
            else:
                print(f"Warning: {source} not found")

print(f"Successfully created {ZIP_PATH}")
