import re

with open(r'frontend\src\GovDocPanel.jsx', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Update mismatch logic block
mismatch_vars = """// -- Mismatch Detection Logic --
  const normalize = (name) => name?.toLowerCase().replace(/ private limited/g, '').replace(/ pvt ltd/g, '').replace(/ ltd/g, '').replace(/ corp/g, '').replace(/ llc/g, '').trim() || '';
  const checkMismatch = (extractedName) => {
    if (!bidderDetails?.name || !extractedName) return false;
    return !normalize(extractedName).includes(normalize(bidderDetails.name)) && !normalize(bidderDetails.name).includes(normalize(extractedName));
  };

  const gstNameMismatch = checkMismatch(gstResult?.extracted?.legal_name);
  const udyamNameMismatch = checkMismatch(udyamResult?.extracted?.enterprise_name);
  const epfoNameMismatch = checkMismatch(epfoResult?.extracted?.employer_name);
  const esicNameMismatch = checkMismatch(esicResult?.extracted?.employer_name);
  const startupNameMismatch = checkMismatch(startupResult?.extracted?.entity_name);
  const nsicNameMismatch = checkMismatch(nsicResult?.extracted?.entity_name);
  const turnoverNameMismatch = checkMismatch(turnoverResult?.extracted?.entity_name);
  
  const itrNameMismatch = checkMismatch(itrResult?.extracted?.name);
  const itrPanMismatch = !!(bidderDetails?.pan && itrResult?.extracted?.pan && itrResult.extracted.pan !== bidderDetails.pan);
  const isItrMismatch = itrNameMismatch || itrPanMismatch;

  const miiNameMismatch = checkMismatch(miiResult?.extracted?.entity_name);
  const isMiiMismatch = miiNameMismatch;
  const gstr3bNameMismatch = checkMismatch(gstr3bResult?.extracted?.entity_name);
  const debarmentNameMismatch = checkMismatch(debarmentResult?.extracted?.entity_name);"""

content = re.sub(r'// -- Mismatch Detection Logic --[\s\S]*?const debarmentNameMismatch = [^\n]+;', mismatch_vars, content)

# 2. Inject `status={...Mismatch ? 'fail' : 'ok'}` and the warning banners for each panel.
# GST
content = content.replace(
    '<Field label="Legal Name"           value={gstResult.extracted?.legal_name}           status="ok" />',
    '<Field label="Legal Name"           value={gstResult.extracted?.legal_name}           status={gstNameMismatch ? "fail" : "ok"} />'
)
gst_banner = """{gstNameMismatch && (
            <div className="mt-3 text-[11px] font-bold text-red-700 bg-red-50 p-2.5 border-2 border-red-300 rounded shadow-sm flex items-start gap-2">
              <svg className="w-4 h-4 shrink-0 mt-0.5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z"/></svg>
              POTENTIAL FORGERY MISMATCH: The entity name in this document does not match the registered profile for {bidderDetails?.name?.toUpperCase() || 'the selected bidder'}.
            </div>
          )}"""
content = content.replace(
    '<Field label="Active Status"        value={gstResult.verification?.registration_active ? \'ACTIVE\' : \'INACTIVE\'}',
    gst_banner + '\n            <Field label="Active Status"        value={gstResult.verification?.registration_active ? \'ACTIVE\' : \'INACTIVE\'}'
)

# Udyam
content = content.replace(
    '<Field label="Enterprise Name" value={udyamResult.extracted?.enterprise_name} status="ok" />',
    '<Field label="Enterprise Name" value={udyamResult.extracted?.enterprise_name} status={udyamNameMismatch ? "fail" : "ok"} />'
)
udyam_banner = """{udyamNameMismatch && (
            <div className="mt-3 text-[11px] font-bold text-red-700 bg-red-50 p-2.5 border-2 border-red-300 rounded shadow-sm flex items-start gap-2">
              <svg className="w-4 h-4 shrink-0 mt-0.5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z"/></svg>
              POTENTIAL FORGERY MISMATCH: The entity name in this document does not match the registered profile for {bidderDetails?.name?.toUpperCase() || 'the selected bidder'}.
            </div>
          )}"""
content = content.replace(
    '<Field label="Major Activity" value={udyamResult.extracted?.major_activity} />',
    udyam_banner + '\n            <Field label="Major Activity" value={udyamResult.extracted?.major_activity} />'
)

# EPFO
content = content.replace(
    '<Field label="Employer Name" value={epfoResult.extracted?.employer_name} status="ok" />',
    '<Field label="Employer Name" value={epfoResult.extracted?.employer_name} status={epfoNameMismatch ? "fail" : "ok"} />'
)
epfo_banner = """{epfoNameMismatch && (
            <div className="mt-3 text-[11px] font-bold text-red-700 bg-red-50 p-2.5 border-2 border-red-300 rounded shadow-sm flex items-start gap-2">
              <svg className="w-4 h-4 shrink-0 mt-0.5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z"/></svg>
              POTENTIAL FORGERY MISMATCH: The entity name in this document does not match the registered profile for {bidderDetails?.name?.toUpperCase() || 'the selected bidder'}.
            </div>
          )}"""
content = content.replace(
    '<Field label="Employer Code"',
    epfo_banner + '\n            <Field label="Employer Code"'
)

# ESIC
content = content.replace(
    '<Field label="Employer Name" value={esicResult.extracted?.employer_name} status="ok" />',
    '<Field label="Employer Name" value={esicResult.extracted?.employer_name} status={esicNameMismatch ? "fail" : "ok"} />'
)
esic_banner = """{esicNameMismatch && (
            <div className="mt-3 text-[11px] font-bold text-red-700 bg-red-50 p-2.5 border-2 border-red-300 rounded shadow-sm flex items-start gap-2">
              <svg className="w-4 h-4 shrink-0 mt-0.5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z"/></svg>
              POTENTIAL FORGERY MISMATCH: The entity name in this document does not match the registered profile for {bidderDetails?.name?.toUpperCase() || 'the selected bidder'}.
            </div>
          )}"""
content = content.replace(
    '<Field label="Employer Code" value={esicResult.extracted?.employer_code}',
    esic_banner + '\n            <Field label="Employer Code" value={esicResult.extracted?.employer_code}'
)

# Startup
content = content.replace(
    '<Field label="Entity Name" value={startupResult.extracted?.entity_name} status="ok" />',
    '<Field label="Entity Name" value={startupResult.extracted?.entity_name} status={startupNameMismatch ? "fail" : "ok"} />'
)
startup_banner = """{startupNameMismatch && (
            <div className="mt-3 text-[11px] font-bold text-red-700 bg-red-50 p-2.5 border-2 border-red-300 rounded shadow-sm flex items-start gap-2">
              <svg className="w-4 h-4 shrink-0 mt-0.5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z"/></svg>
              POTENTIAL FORGERY MISMATCH: The entity name in this document does not match the registered profile for {bidderDetails?.name?.toUpperCase() || 'the selected bidder'}.
            </div>
          )}"""
content = content.replace(
    '<Field label="DIPP Number"',
    startup_banner + '\n            <Field label="DIPP Number"'
)

# NSIC
content = content.replace(
    '<Field label="Entity Name" value={nsicResult.extracted?.entity_name} status="ok" />',
    '<Field label="Entity Name" value={nsicResult.extracted?.entity_name} status={nsicNameMismatch ? "fail" : "ok"} />'
)
nsic_banner = """{nsicNameMismatch && (
            <div className="mt-3 text-[11px] font-bold text-red-700 bg-red-50 p-2.5 border-2 border-red-300 rounded shadow-sm flex items-start gap-2">
              <svg className="w-4 h-4 shrink-0 mt-0.5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z"/></svg>
              POTENTIAL FORGERY MISMATCH: The entity name in this document does not match the registered profile for {bidderDetails?.name?.toUpperCase() || 'the selected bidder'}.
            </div>
          )}"""
content = content.replace(
    '<Field label="Certificate No"',
    nsic_banner + '\n            <Field label="Certificate No"'
)

# Turnover
content = content.replace(
    '<Field label="Entity Name" value={turnoverResult.extracted?.entity_name} status="ok" />',
    '<Field label="Entity Name" value={turnoverResult.extracted?.entity_name} status={turnoverNameMismatch ? "fail" : "ok"} />'
)
turnover_banner = """{turnoverNameMismatch && (
            <div className="mt-3 text-[11px] font-bold text-red-700 bg-red-50 p-2.5 border-2 border-red-300 rounded shadow-sm flex items-start gap-2">
              <svg className="w-4 h-4 shrink-0 mt-0.5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z"/></svg>
              POTENTIAL FORGERY MISMATCH: The entity name in this document does not match the registered profile for {bidderDetails?.name?.toUpperCase() || 'the selected bidder'}.
            </div>
          )}"""
content = content.replace(
    '<Field label="Financial Year"',
    turnover_banner + '\n            <Field label="Financial Year"'
)

with open(r'frontend\src\GovDocPanel.jsx', 'w', encoding='utf-8') as f:
    f.write(content)
