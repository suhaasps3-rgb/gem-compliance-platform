import os

ROOT = r'C:\Users\Suhaas\.gemini\antigravity\scratch\gem_compliance'

# 1. Patch ContradictionReview.jsx
f = os.path.join(ROOT, 'frontend', 'src', 'ContradictionReview.jsx')
with open(f, 'r', encoding='utf-8') as file:
    content = file.read()

content = content.replace(
    'console.log("Dismissed contradiction:", contradictionId);',
    '''console.log("Dismissed contradiction:", contradictionId);
    setLocalContradictions(localContradictions.filter(c => c.contradiction_id !== contradictionId));'''
)
content = content.replace(
    'console.log("Downloading PDF for", selectedContradiction.contradiction_id);',
    '''console.log("Downloading PDF for", selectedContradiction.contradiction_id);
    alert("Action log exported securely for audit (Mock Demo)");'''
)
with open(f, 'w', encoding='utf-8') as file:
    file.write(content)
print('ContradictionReview.jsx patched')

# 2. Patch Dashboard.jsx
f = os.path.join(ROOT, 'frontend', 'src', 'Dashboard.jsx')
with open(f, 'r', encoding='utf-8') as file:
    content = file.read()

dashboard_imports = """
import GovDocPanel from './GovDocPanel';
import ComplianceScorecard from './components/ComplianceScorecard';
import ExperiencePanel from './components/ExperiencePanel';
import TechnicalMatrix from './components/TechnicalMatrix';
"""
if 'import ComplianceScorecard' not in content:
    content = content.replace("import GovDocPanel from './GovDocPanel';", dashboard_imports)

dashboard_panels = """
        <GovDocPanel />
        <ExperiencePanel />
        <TechnicalMatrix />
"""
if '<ComplianceScorecard />' not in content:
    content = content.replace("<GovDocPanel />", dashboard_panels)
    content = content.replace(
        '<h1 className="text-3xl font-bold text-gray-800 tracking-tight">AI Compliance Officer</h1>',
        '''<h1 className="text-3xl font-bold text-gray-800 tracking-tight">AI Compliance Officer</h1>
        <ComplianceScorecard />'''
    )

with open(f, 'w', encoding='utf-8') as file:
    file.write(content)
print('Dashboard.jsx patched')

# 3. Patch App.jsx
f = os.path.join(ROOT, 'frontend', 'src', 'App.jsx')
with open(f, 'r', encoding='utf-8') as file:
    content = file.read()

app_imports = """
import { useDashboardStore } from './store/dashboardStore';
import BatchProcessor from './pages/BatchProcessor';
"""
if 'import BatchProcessor' not in content:
    content = content.replace("import { useState, useEffect } from 'react';", "import { useState, useEffect } from 'react';\n" + app_imports)

if 'const { batchModeActive, setBatchModeActive } = useDashboardStore();' not in content:
    content = content.replace(
        'const [showCartelModal, setShowCartelModal] = useState(false);',
        '''const [showCartelModal, setShowCartelModal] = useState(false);
  const { batchModeActive, setBatchModeActive } = useDashboardStore();'''
    )

batch_btn = """
          <button 
            onClick={() => setBatchModeActive(true)}
            className="flex items-center gap-2 bg-indigo-600 text-white px-4 py-2 rounded font-medium hover:bg-indigo-700 transition"
          >
            <span>⚡</span> Batch Mode
          </button>
          <button 
"""
if 'Batch Mode' not in content:
    content = content.replace('<button \n            onClick={() => setShowCartelModal(true)}', batch_btn)

if '<BatchProcessor />' not in content:
    content = content.replace(
        '{showCartelModal && <AntiCartelModal onClose={() => setShowCartelModal(false)} />}',
        '''{showCartelModal && <AntiCartelModal onClose={() => setShowCartelModal(false)} />}
      {batchModeActive && <BatchProcessor />}'''
    )

with open(f, 'w', encoding='utf-8') as file:
    file.write(content)
print('App.jsx patched')
