import re

with open(r'frontend\src\EvidenceGraph.jsx', 'r', encoding='utf-8') as f:
    content = f.read()

new_legend = """
      <div className="flex flex-col gap-2 px-5 py-3 border-b border-slate-100 bg-white">
        <div className="flex items-center gap-2 text-[10px] font-bold text-slate-500 uppercase tracking-widest">
            <svg className="w-4 h-4 text-blue-500" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M13 10V3L4 14h7v7l9-11h-7z"></path></svg>
            Interactive Evidence Provenance Graph
        </div>
        <div className="flex items-center gap-1.5 text-[9px] font-bold uppercase tracking-widest text-slate-500">
           <span>Flow:</span>
           <span className="bg-blue-100 text-blue-700 px-1.5 py-0.5 rounded">Requirement</span>
           <span>→</span>
           <span className="bg-blue-100 text-blue-700 px-1.5 py-0.5 rounded">Document</span>
           <span>→</span>
           <span className="bg-blue-100 text-blue-700 px-1.5 py-0.5 rounded">Claim</span>
           <span>→</span>
           <span className="bg-emerald-100 text-emerald-700 px-1.5 py-0.5 rounded">Evidence</span>
           <span>→</span>
           <span className="bg-slate-200 text-slate-700 px-1.5 py-0.5 rounded">Rule</span>
           <span>→</span>
           <span className="bg-red-100 text-red-700 px-1.5 py-0.5 rounded">Contradiction</span>
           <span>→</span>
           <span className="bg-orange-100 text-orange-700 px-1.5 py-0.5 rounded">Risk</span>
           <span>→</span>
           <span className="bg-purple-100 text-purple-700 px-1.5 py-0.5 rounded">Recommendation</span>
        </div>
      </div>
"""

content = re.sub(r'<div className="flex gap-4 px-5 py-2 border-b border-slate-100 bg-white text-\[10px\]">.*?</div>\s*</div>', new_legend, content, flags=re.DOTALL)

with open(r'frontend\src\EvidenceGraph.jsx', 'w', encoding='utf-8') as f:
    f.write(content)
