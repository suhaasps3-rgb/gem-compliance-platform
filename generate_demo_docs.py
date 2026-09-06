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
    </body></html>
    """,
    "startup_india_demo.pdf": """
    <html><body style="font-family: Arial; padding: 40px;">
        <h1 style="text-align:center; color: #E74C3C;">STARTUP INDIA</h1>
        <h2 style="text-align:center;">CERTIFICATE OF RECOGNITION</h2>
        <hr/>
        <p>This is to certify that</p>
        <h3 style="text-align:center;">Acme Innovations Pvt Ltd</h3>
        <p>has been recognized as a Startup by the Department for Promotion of Industry and Internal Trade (DPIIT).</p>
        <p><b>Recognition Number:</b> DIPP12345</p>
        <p><b>Date of Recognition:</b> 15-05-2023</p>
        <p><b>Valid Till:</b> 14-05-2033 (Perpetual)</p>
        <h3 style="color: green; text-align: center;">Status: ACTIVE / Recognized</h3>
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
        <p><b>Order Value:</b> Rs. 2.10 Crore</p>
        <p><b>Date of Completion:</b> 30-09-2023</p>
        <h3 style="color: green;">Status: Completed</h3>
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
    </body></html>
    """,
    "ca_turnover.pdf": """
    <html><body style="font-family: Arial; padding: 40px;">
        <h1 style="text-align:center;">TO WHOMSOEVER IT MAY CONCERN</h1>
        <h2 style="text-align:center;">TURNOVER CERTIFICATE</h2>
        <hr/>
        <p>This is to certify that the Annual Turnover of <b>Acme Innovations Pvt Ltd</b> for the financial years is as follows:</p>
        <table border="1" cellpadding="8" style="border-collapse: collapse; width: 100%;">
            <tr><th>Financial Year</th><th>Turnover (INR)</th></tr>
            <tr><td>2022-23</td><td>Rs. 4.10 Crore</td></tr>
            <tr><td>2023-24</td><td>Rs. 6.20 Crore</td></tr>
            <tr><td><b>2024-25</b></td><td><b>Rs. 8.5 Crore</b></td></tr>
        </table>
        <br/>
        <p><b>Name of CA:</b> CA Ramesh Kumar</p>
        <p><b>Membership No:</b> 123456</p>
        <p><b>UDIN:</b> 24333ABC123456</p>
        <p><b>Certificate Date:</b> 01-08-2026</p>
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
