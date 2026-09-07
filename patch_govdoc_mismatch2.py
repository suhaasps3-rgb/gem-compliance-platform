import re

with open(r'frontend\src\GovDocPanel.jsx', 'r', encoding='utf-8') as f:
    content = f.read()

# Replace the GSTR-3B panel
gstr3b_regex = r'\{gstr3bResult && \([\s\S]*?</Panel>\s*\)\}'
new_gstr3b = """{gstr3bResult && (
        <Panel title="GSTR-3B Return" color="indigo" icon="📄" onClear={clearGstr3b}>
          <Field label="Entity Name" value={gstr3bResult.extracted?.entity_name} status={gstr3bNameMismatch ? 'fail' : 'ok'} />
          <Field label="Filing Status" value={gstr3bResult.extracted?.filing_status} status={gstr3bResult.extracted?.filing_status === 'FILED' ? 'ok' : 'fail'} />
          <Field label="Return Period" value={gstr3bResult.extracted?.return_period} status="ok" />
          <Field label="Tax Payable" value={gstr3bResult.extracted?.tax_payable} />
          <Field label="Tax Paid" value={gstr3bResult.extracted?.tax_paid} status="ok" />
          
          {gstr3bNameMismatch && (
            <div className="mt-3 text-[11px] font-bold text-red-700 bg-red-50 p-2.5 border-2 border-red-300 rounded shadow-sm flex items-start gap-2">
              <svg className="w-4 h-4 shrink-0 mt-0.5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z"/></svg>
              POTENTIAL FORGERY MISMATCH: The entity name in this document does not match the registered profile for {bidderDetails?.name?.toUpperCase() || 'the selected bidder'}.
            </div>
          )}
          
          <div className="mt-2 text-[10px] text-indigo-700 bg-indigo-50 p-2 border border-indigo-200 rounded">
            {gstr3bResult.verification?.note}
          </div>
        </Panel>
      )}"""

content = re.sub(gstr3b_regex, new_gstr3b, content)

# Replace the Debarment panel
debarment_regex = r'\{debarmentResult && \([\s\S]*?</Panel>\s*\)\}'
new_debarment = """{debarmentResult && (
        <Panel title="Debarment Declaration" color="rose" icon="🚨" onClear={clearDebarment}>
          <Field label="Entity Name" value={debarmentResult.extracted?.entity_name} status={debarmentNameMismatch ? 'fail' : 'ok'} />
          <Field label="Declaration" value={debarmentResult.extracted?.declaration} status="ok" />
          
          {debarmentNameMismatch && (
            <div className="mt-3 text-[11px] font-bold text-red-700 bg-red-50 p-2.5 border-2 border-red-300 rounded shadow-sm flex items-start gap-2">
              <svg className="w-4 h-4 shrink-0 mt-0.5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z"/></svg>
              POTENTIAL FORGERY MISMATCH: The entity name in this document does not match the registered profile for {bidderDetails?.name?.toUpperCase() || 'the selected bidder'}.
            </div>
          )}
          
          <div className="mt-2 text-[10px] text-rose-700 bg-rose-50 p-2 border border-rose-200 rounded">
            {debarmentResult.verification?.note}
          </div>
        </Panel>
      )}"""

content = re.sub(debarment_regex, new_debarment, content)

with open(r'frontend\src\GovDocPanel.jsx', 'w', encoding='utf-8') as f:
    f.write(content)
