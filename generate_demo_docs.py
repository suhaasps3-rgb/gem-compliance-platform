import asyncio
from playwright.async_api import async_playwright
import os

ROOT = r'C:\Users\Suhaas\.gemini\antigravity\scratch\gem_compliance\frontend\public'

HTML_TEMPLATES = {
    "epfo_demo.pdf": """
    <html><body style="font-family: Arial; padding: 40px;">
        <h1 style="text-align:center;">EMPLOYEES' PROVIDENT FUND ORGANIZATION</h1>
        <h2 style="text-align:center;">ELECTRONIC CHALLAN CUM RETURN (ECR)</h2>
        <hr/>
        <p><b>Employer Name:</b> Acme Innovations Pvt Ltd</p>
        <p><b>Establishment Code:</b> MHBAN0012345</p>
        <p><b>Wage Month / Period:</b> August 2026</p>
        <p><b>No of Employees:</b> 25</p>
        <br/>
        <table border="1" cellpadding="8" style="border-collapse: collapse; width: 100%;">
            <tr><th>Particulars</th><th>Amount (₹)</th></tr>
            <tr><td>Employee Contribution (EE Share)</td><td>60,000</td></tr>
            <tr><td>Employer Contribution (ER Share)</td><td>60,000</td></tr>
            <tr><td><b>Total Amount</b></td><td><b>1,20,000</b></td></tr>
        </table>
        <br/>
        <p><b>Challan No:</b> 000123456789</p>
        <h3 style="color: green;">Status: PAID / Payment Successful</h3>
        <p>This is a computer generated statement.</p>
        <div style="margin-top: 50px; display: inline-block; border: 3px solid #2980b9; color: #2980b9; padding: 15px; border-radius: 5px; font-family: monospace; font-weight: bold; transform: rotate(-5deg);">
            ★ AUTHORIZED SIGNATORY ★<br/>
            <span style="font-size: 10px;">[Digitally Signed & Stamped]</span>
        </div>
    </body></html>
    """,
    "esic_demo.pdf": """
    <html><body style="font-family: Arial; padding: 40px;">
        <h1 style="text-align:center;">EMPLOYEES' STATE INSURANCE CORPORATION</h1>
        <h2 style="text-align:center;">E-CHALLAN</h2>
        <hr/>
        <p><b>Employer Name:</b> Acme Innovations Pvt Ltd</p>
        <p><b>Employer Code:</b> 31000123450000100</p>
        <p><b>Contribution Period:</b> August 2026</p>
        <p><b>Insured Persons:</b> 25</p>
        <p><b>Contribution Amount:</b> ₹45,000</p>
        <p><b>Challan No:</b> 03126123456789</p>
        <br/>
        <h3 style="color: green;">Status: PAID / Challan Paid</h3>
        <div style="margin-top: 50px; display: inline-block; border: 3px solid #2980b9; color: #2980b9; padding: 15px; border-radius: 5px; font-family: monospace; font-weight: bold; transform: rotate(-5deg);">
            ★ AUTHORIZED SIGNATORY ★<br/>
            <span style="font-size: 10px;">[Digitally Signed & Stamped]</span>
        </div>
    </body></html>
    """,
    "startup_india_demo.pdf": """
    <html><body style="font-family: Arial; padding: 40px;">
        <h1 style="text-align:center; color: #E74C3C;">STARTUP INDIA</h1>
        <h2 style="text-align:center;">CERTIFICATE OF REGISTRATION</h2>
        <hr/>
        <p>This is to certify that</p>
        <h3 style="text-align:center;">Acme Innovations Pvt Ltd</h3>
        <p>was previously registered as a Startup by the Department for Promotion of Industry and Internal Trade (DPIIT).</p>
        <p><b>Registration Number:</b> DIPP12345</p>
        <p><b>Date of Registration:</b> 15-05-2023</p>
        <p><b>Expired On:</b> 14-05-2024</p>
        <h3 style="color: red; text-align: center;">Status: INACTIVE / Revoked</h3>
        <div style="margin-top: 50px; display: inline-block; border: 3px solid #2980b9; color: #2980b9; padding: 15px; border-radius: 5px; font-family: monospace; font-weight: bold; transform: rotate(-5deg);">
            ★ AUTHORIZED SIGNATORY ★<br/>
            <span style="font-size: 10px;">[Digitally Signed & Stamped]</span>
        </div>
    </body></html>
    """,
    "nsic_demo.pdf": """
    <html><body style="font-family: Arial; padding: 40px;">
        <h1 style="text-align:center; color: #2980B9;">NATIONAL SMALL INDUSTRIES CORPORATION LTD.</h1>
        <h2 style="text-align:center;">ENLISTMENT CERTIFICATE</h2>
        <hr/>
        <p><b>Certificate No:</b> NS/MC/CH/2023/01234</p>
        <p><b>Name of Enterprise:</b> Acme Innovations Pvt Ltd</p>
        <p><b>Category:</b> Category-I (Micro)</p>
        <p><b>Date of Issue:</b> 10-06-2023</p>
        <p><b>Valid Upto:</b> 09-06-2025</p>
        <p>Registered under single point registration scheme for EMD exemption.</p>
        <div style="margin-top: 50px; display: inline-block; border: 3px solid #2980b9; color: #2980b9; padding: 15px; border-radius: 5px; font-family: monospace; font-weight: bold; transform: rotate(-5deg);">
            ★ AUTHORIZED SIGNATORY ★<br/>
            <span style="font-size: 10px;">[Digitally Signed & Stamped]</span>
        </div>
    </body></html>
    """,
    "work_order_1.pdf": """
    <html><body style="font-family: Arial; padding: 40px;">
        <h2>WORK ORDER</h2>
        <hr/>
        <p><b>To:</b> Acme Innovations Pvt Ltd</p>
        <p><b>From:</b> Reliance Industries Ltd</p>
        <p><b>Work Order No:</b> WO-1023</p>
        <p><b>Order Date:</b> 01-04-2023</p>
        <br/>
        <p><b>Scope:</b> Supply and commissioning of industrial pump systems.</p>
        <p><b>Order Value:</b> Rs. 21.81 Crore</p>
        <p><b>Date of Completion:</b> 30-09-2023</p>
        <h3 style="color: green;">Status: Completed</h3>
        <div style="margin-top: 50px; display: inline-block; border: 3px solid #2980b9; color: #2980b9; padding: 15px; border-radius: 5px; font-family: monospace; font-weight: bold; transform: rotate(-5deg);">
            ★ AUTHORIZED SIGNATORY ★<br/>
            <span style="font-size: 10px;">[Digitally Signed & Stamped]</span>
        </div>
    </body></html>
    """,
    "work_order_2.pdf": """
    <html><body style="font-family: Arial; padding: 40px;">
        <h2>PURCHASE ORDER</h2>
        <hr/>
        <p><b>To M/s:</b> Acme Innovations Pvt Ltd</p>
        <p><b>Client:</b> ONGC</p>
        <p><b>PO No:</b> WO-1187</p>
        <p><b>Issue Date:</b> 15-09-2022</p>
        <br/>
        <p><b>Subject:</b> Maintenance and overhaul of pumping stations.</p>
        <p><b>Total Amount:</b> Rs. 1.75 Crore</p>
        <p><b>Completed on:</b> 10-03-2023</p>
        <h3 style="color: green;">Status: Executed</h3>
        <div style="margin-top: 50px; display: inline-block; border: 3px solid #2980b9; color: #2980b9; padding: 15px; border-radius: 5px; font-family: monospace; font-weight: bold; transform: rotate(-5deg);">
            ★ AUTHORIZED SIGNATORY ★<br/>
            <span style="font-size: 10px;">[Digitally Signed & Stamped]</span>
        </div>
    </body></html>
    """,
    "work_order_3.pdf": """
    <html><body style="font-family: Arial; padding: 40px;">
        <h2>CONTRACT AGREEMENT</h2>
        <hr/>
        <p><b>Contractor:</b> Acme Innovations Pvt Ltd</p>
        <p><b>Buyer:</b> HPCL</p>
        <p><b>Reference No:</b> WO-1452</p>
        <p><b>Date of Order:</b> 10-12-2024</p>
        <br/>
        <p><b>Description:</b> Installation of high-pressure liquid transport systems.</p>
        <p><b>Contract Value:</b> ₹ 3.50 Crore</p>
        <p><b>Completion Date:</b> 25-05-2025</p>
        <h3 style="color: green;">Status: Executed</h3>
        <div style="margin-top: 50px; display: inline-block; border: 3px solid #2980b9; color: #2980b9; padding: 15px; border-radius: 5px; font-family: monospace; font-weight: bold; transform: rotate(-5deg);">
            ★ AUTHORIZED SIGNATORY ★<br/>
            <span style="font-size: 10px;">[Digitally Signed & Stamped]</span>
        </div>
    </body></html>
    """,
    "ca_turnover.pdf": """
    <html><body style="font-family: Arial; padding: 40px;">
        <h1 style="text-align:center;">TO WHOMSOEVER IT MAY CONCERN</h1>
        <h2 style="text-align:center;">TURNOVER CERTIFICATE</h2>
        <hr/>
        <p>This is to certify the financial details based on the audited balance sheets.</p>
        <p><b>Name of Company:</b> Acme Innovations Pvt Ltd</p>
        <p><b>Financial Year:</b> 2024-25</p>
        <p><b>Annual Turnover:</b> Rs. 8.50 Crore</p>
        <br/>
        <p><b>Name of CA:</b> CA Ramesh Kumar</p>
        <p><b>Membership No:</b> 123456</p>
        <p><b>UDIN:</b> 24123456ABCDEF9876</p>
        <p><b>Certificate Date:</b> 01-08-2026</p>
        <div style="margin-top: 50px; display: inline-block; border: 3px solid #2980b9; color: #2980b9; padding: 15px; border-radius: 5px; font-family: monospace; font-weight: bold; transform: rotate(-5deg);">
            ★ AUTHORIZED SIGNATORY ★<br/>
            <span style="font-size: 10px;">[Digitally Signed & Stamped]</span>
        </div>
    </body></html>
    """,
    "technical_catalog.pdf": """
    <html><body style="font-family: Arial; padding: 40px;">
        <h1 style="text-align:center;">PRODUCT DATASHEET - ACME PUMPS</h1>
        <hr/>
        <h2>Model: AP-X500 High Capacity Centrifugal Pump</h2>
        <br/>
        <h3>Technical Specifications</h3>
        <ul>
            <li><b>Pump Capacity:</b> 520 m³/hr</li>
            <li><b>Discharge Pressure:</b> 22 bar</li>
            <li><b>Pump Efficiency:</b> 91 %</li>
            <li><b>Supply Voltage:</b> 415 V</li>
            <li><b>Motor Power:</b> 45 kW</li>
            <li><b>Casing Material:</b> Stainless Steel 316L</li>
            <li><b>Impeller Material:</b> Bronze</li>
        </ul>
        <br/>
        <p>Certified for continuous heavy-duty industrial applications.</p>
    </body></html>
    """,
    "work_order_unsigned.pdf": """
    <html><body style="font-family: Arial; padding: 40px;">
        <h2>PURCHASE ORDER</h2>
        <hr/>
        <p><b>To M/s:</b> Echo Enterprises</p>
        <p><b>Client:</b> BSNL</p>
        <p><b>PO No:</b> WO-9999</p>
        <p><b>Issue Date:</b> 01-01-2024</p>
        <br/>
        <p><b>Subject:</b> Supply of networking equipment.</p>
        <p><b>Total Amount:</b> Rs. 4.20 Crore</p>
        <p><b>Completed on:</b> 10-10-2024</p>
        <h3 style="color: green;">Status: Executed</h3>
    </body></html>
    """
}

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()
        
        for filename, html_content in HTML_TEMPLATES.items():
            path = os.path.join(ROOT, filename)
            await page.set_content(html_content)
            await page.pdf(path=path, format="A4", margin={"top": "20px", "bottom": "20px", "left": "20px", "right": "20px"})
            print(f"Generated {filename}")
            
        await browser.close()

if __name__ == "__main__":
    asyncio.run(main())
