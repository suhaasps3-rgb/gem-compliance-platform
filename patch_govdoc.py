import re

with open(r'frontend\src\GovDocPanel.jsx', 'r', encoding='utf-8') as f:
    content = f.read()

# Add to state pulls
content = content.replace("const miiResult = useDashboardStore(s => s.miiParseResult);", 
"""const miiResult = useDashboardStore(s => s.miiParseResult);
  const gstr3bResult = useDashboardStore(s => s.gstr3bParseResult);
  const debarmentResult = useDashboardStore(s => s.debarmentParseResult);""")

content = content.replace("const clearMii = useDashboardStore(s => s.clearMiiParseResult);",
"""const clearMii = useDashboardStore(s => s.clearMiiParseResult);
  const clearGstr3b = useDashboardStore(s => s.clearGstr3bParseResult);
  const clearDebarment = useDashboardStore(s => s.clearDebarmentParseResult);""")

content = content.replace("&& !itrResult && !miiResult) return null;",
"&& !itrResult && !miiResult && !gstr3bResult && !debarmentResult) return null;")

# Add panels at the end
panels = """
      {gstr3bResult && (
        <Panel title="GSTR-3B Return" color="indigo" icon="📄" onClear={clearGstr3b}>
          <Field label="Filing Status" value={gstr3bResult.extracted?.filing_status} status={gstr3bResult.extracted?.filing_status === 'FILED' ? 'ok' : 'fail'} />
          <Field label="Return Period" value={gstr3bResult.extracted?.return_period} status="ok" />
          <Field label="Tax Payable" value={gstr3bResult.extracted?.tax_payable} />
          <Field label="Tax Paid" value={gstr3bResult.extracted?.tax_paid} status="ok" />
          
          <div className="mt-2 text-[10px] text-indigo-700 bg-indigo-50 p-2 border border-indigo-200 rounded">
            {gstr3bResult.verification?.note}
          </div>
        </Panel>
      )}

      {debarmentResult && (
        <Panel title="Debarment Declaration" color="rose" icon="🚨" onClear={clearDebarment}>
          <Field label="Entity Name" value={debarmentResult.extracted?.entity_name} status="ok" />
          <Field label="Declaration" value={debarmentResult.extracted?.declaration} status="ok" />
          
          <div className="mt-2 text-[10px] text-rose-700 bg-rose-50 p-2 border border-rose-200 rounded">
            {debarmentResult.verification?.note}
          </div>
        </Panel>
      )}
    </div>
  );
}
"""

content = re.sub(r'    </div>\s*\);\s*}\s*$', panels, content)

with open(r'frontend\src\GovDocPanel.jsx', 'w', encoding='utf-8') as f:
    f.write(content)
