"""
Generates a properly rendered Telugu tender PDF using Playwright + Chromium.
Chromium uses HarfBuzz for full OpenType shaping — Telugu renders perfectly.
"""
import asyncio, base64, os
from playwright.async_api import async_playwright

# Embed the Noto Sans Telugu font as base64 so Chromium can load it offline
with open("NotoSansTelugu-Regular.ttf", "rb") as f:
    font_b64 = base64.b64encode(f.read()).decode()

HTML = f"""<!DOCTYPE html>
<html lang="te">
<head>
<meta charset="UTF-8">
<style>
  @font-face {{
    font-family: 'NotoTelugu';
    src: url('data:font/truetype;base64,{font_b64}') format('truetype');
    font-weight: normal;
  }}
  * {{ margin: 0; padding: 0; box-sizing: border-box; }}
  body {{
    font-family: 'NotoTelugu', 'Noto Sans Telugu', serif;
    font-size: 12pt;
    color: #212121;
    background: white;
    padding: 1.5cm 2cm;
    line-height: 2.0;
  }}
  .en {{ font-family: Arial, Helvetica, sans-serif; }}

  /* Header */
  .header {{ text-align: center; margin-bottom: 10pt; }}
  .header .title-te {{ font-size: 22pt; color: #1a237e; margin-bottom: 4pt; }}
  .header .sub-te  {{ font-size: 13pt; color: #1a237e; margin-bottom: 2pt; }}
  .header .sub-en  {{ font-family: Arial; font-size: 9pt; color: #666; }}

  .gold-bar {{ height: 4pt; background: #f57f17; margin: 8pt 0; border-radius: 2pt; }}

  .doc-title {{ font-size: 17pt; color: #1a237e; text-align: center; }}
  .tender-no {{ font-family: Arial; font-size: 10pt; color: #b71c1c; text-align: center; margin-top: 2pt; }}

  /* Meta table */
  .meta {{ width: 100%; border-collapse: collapse; margin: 14pt 0; }}
  .meta td {{ padding: 7pt 10pt; border: 0.5pt solid #c5cae9; font-size: 11pt; vertical-align: top; }}
  .meta tr:nth-child(even) td {{ background: #f5f5f5; }}
  .meta .lbl {{ color: #1a237e; font-size: 10pt; width: 35%; }}
  .meta .lbl-en {{ font-family: Arial; font-size: 8pt; color: #999; display: block; }}

  /* Section */
  .section {{ margin-top: 18pt; border-top: 2pt solid #1a237e; padding-top: 6pt; margin-bottom: 8pt; }}
  .section h3 {{ font-size: 14pt; color: #1a237e; }}
  .section .en-label {{ font-family: Arial; font-size: 8pt; color: #888; }}

  /* Rule card */
  .rule {{ border-left: 4pt solid #1a237e; background: #fafafa; padding: 8pt 12pt; margin-bottom: 10pt; border-radius: 2pt; }}
  .rule-title {{ font-size: 12pt; color: #1a237e; margin-bottom: 3pt; font-weight: bold; }}
  .rule-body  {{ font-size: 11.5pt; color: #333; margin-bottom: 3pt; }}
  .rule-hint  {{ font-family: Arial; font-size: 8pt; color: #888; margin-top: 2pt; }}

  /* Footer */
  .footer {{ margin-top: 20pt; border-top: 1pt solid #e0e0e0; padding-top: 8pt; text-align: center; }}
  .footer .te-note {{ font-size: 9pt; color: #777; }}
  .footer .en-note {{ font-family: Arial; font-size: 8pt; color: #aaa; }}
</style>
</head>
<body>

<!-- ══ HEADER ══ -->
<div class="header">
  <div class="title-te">భారత ప్రభుత్వం</div>
  <div class="sub-te">ప్రభుత్వ ఇ-మార్కెట్‌ప్లేస్ (GeM) సంగ్రహణ విభాగం</div>
  <div class="sub-en en">GOVERNMENT OF INDIA — GeM Procurement Division</div>
</div>
<div class="gold-bar"></div>
<div class="doc-title">ప్రామాణిక బిడ్ పత్రం (SBD)</div>
<div class="sub-en en" style="text-align:center; margin-top:3pt;">Standard Bid Document — Regional Infrastructure Services</div>
<div class="tender-no en">Tender No: GeM/TE/2026/INFRA/KA/0047</div>

<!-- ══ META TABLE ══ -->
<table class="meta">
  <tr>
    <td class="lbl">విభాగం <span class="lbl-en en">Department</span></td>
    <td>రహదారులు మరియు మౌలిక సదుపాయాల మంత్రిత్వ శాఖ</td>
  </tr>
  <tr>
    <td class="lbl">ప్రాజెక్ట్ పేరు <span class="lbl-en en">Project Name</span></td>
    <td>రాష్ట్రీయ రహదారి నిర్మాణం మరియు నిర్వహణ</td>
  </tr>
  <tr>
    <td class="lbl">స్థానం <span class="lbl-en en">Location</span></td>
    <td>కర్ణాటక రాష్ట్రం — బెంగళూరు-మైసూరు కారిడార్</td>
  </tr>
  <tr>
    <td class="lbl">సమర్పణ తేదీ <span class="lbl-en en">Submission Date</span></td>
    <td>30/09/2026 సాయంత్రం 5:00 గంటల వరకు</td>
  </tr>
  <tr>
    <td class="lbl">అంచనా విలువ <span class="lbl-en en">Estimated Value</span></td>
    <td>₹ 48,00,00,000 (రూ. నలభై ఎనిమిది కోట్లు)</td>
  </tr>
</table>

<!-- ══ ELIGIBILITY SECTION ══ -->
<div class="section">
  <h3>విభాగం 1: అర్హత ప్రమాణాలు</h3>
  <div class="en-label en">Section 1: Eligibility Criteria — All 6 conditions are mandatory</div>
</div>

<div class="rule">
  <div class="rule-title">నియమం 1 — ఆర్థిక సామర్థ్యం</div>
  <div class="rule-body">బిడ్డర్ వార్షిక టర్నోవర్ <strong>రూ. 10 కోట్లు</strong> లేదా అంతకంటే తక్కువ ఉండాలి. MSMED చట్టం 2006 ప్రకారం సూక్ష్మ పరిశ్రమగా Udyam నమోదు ఉండాలి.</div>
  <div class="rule-hint en">↳  Financial Capacity: Turnover ≤ Rs. 10 Crores — MSME Micro Enterprise</div>
</div>

<div class="rule">
  <div class="rule-title">నియమం 2 — మేక్ ఇన్ ఇండియా స్థానిక కంటెంట్</div>
  <div class="rule-body">మొత్తం ప్రాజెక్ట్ విలువలో కనీసం <strong>50%</strong> స్థానిక కంటెంట్ (Local Content) ఉండాలి. క్లాస్-I స్థానిక సరఫరాదారులకు ప్రాధాన్యత ఇవ్వబడుతుంది.</div>
  <div class="rule-hint en">↳  Make in India: Minimum 50% Local Content — Class-I Local Suppliers preferred</div>
</div>

<div class="rule">
  <div class="rule-title">నియమం 3 — ఉప-కాంట్రాక్టింగ్ పరిమితి</div>
  <div class="rule-body">ఉప-కాంట్రాక్టింగ్ మొత్తం విలువలో గరిష్టంగా <strong>20%</strong> మాత్రమే అనుమతించబడుతుంది. సంయుక్త సాహసాలు (JVs) ముందస్తు అనుమతి లేకుండా నిషేధించబడ్డాయి.</div>
  <div class="rule-hint en">↳  Sub-contracting capped at 20% — JVs prohibited without prior written approval</div>
</div>

<div class="rule">
  <div class="rule-title">నియమం 4 — GST చట్టబద్ధత</div>
  <div class="rule-body">గత <strong>12 నెలలు</strong> నిరంతరంగా GSTR-1 మరియు GSTR-3B రిటర్న్‌లు ఫైల్ చేయబడి ఉండాలి. ఏ నెల అంతరాయం ఆటోమేటిక్ అనర్హతకు దారి తీస్తుంది.</div>
  <div class="rule-hint en">↳  GST Compliance: 12 months uninterrupted GSTR-1 &amp; GSTR-3B filing</div>
</div>

<div class="rule">
  <div class="rule-title">నియమం 5 — EMD మినహాయింపు</div>
  <div class="rule-body">చెల్లుబాటు అయ్యే Udyam నమోదు సర్టిఫికేట్ కలిగిన సూక్ష్మ మరియు చిన్న సంస్థలు (MSEs) <strong>2% EMD</strong> నుండి మినహాయించబడ్డాయి. Bid Security Declaration సమర్పించాలి.</div>
  <div class="rule-hint en">↳  EMD Exemption: MSEs with valid Udyam Certificate exempt from 2% Earnest Money Deposit</div>
</div>

<div class="rule">
  <div class="rule-title">నియమం 6 — నిషేధించబడిన జాబితా తనిఖీ</div>
  <div class="rule-body">బిడ్డర్ మరియు వారి అన్ని డైరెక్టర్లు ఏ ప్రభుత్వ సంస్థచే నిషేధించబడి లేదా బ్లాక్‌లిస్ట్ చేయబడి ఉండకూడదు. GFR 2017 నియమం 151 వర్తిస్తుంది.</div>
  <div class="rule-hint en">↳  Debarment Check: No blacklisting by any Government entity (GFR 2017 Rule 151)</div>
</div>

<!-- ══ FOOTER ══ -->
<div class="footer">
  <div class="gold-bar"></div>
  <div class="te-note">గమనిక: ఈ పత్రం GeM AI కంప్లయన్స్ ప్లాట్‌ఫారమ్ ద్వారా భాషిణి AI ద్వారా స్వయంచాలకంగా ధృవీకరించబడుతుంది.</div>
  <div class="en-note en">Auto-verified via GeM AI Compliance Platform — Bhashini OCR Pipeline (MeitY) | GeM/TE/2026/INFRA/KA/0047</div>
</div>

</body>
</html>"""

OUT = "frontend/public/telugu_tender_demo.pdf"

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()
        await page.set_content(HTML, wait_until="networkidle")
        # Give font time to load
        await page.wait_for_timeout(1500)
        await page.pdf(
            path=OUT,
            format="A4",
            margin={"top": "1cm", "bottom": "1cm", "left": "1.5cm", "right": "1.5cm"},
            print_background=True,
        )
        await browser.close()
    print(f"Generated: {OUT}")

asyncio.run(main())
