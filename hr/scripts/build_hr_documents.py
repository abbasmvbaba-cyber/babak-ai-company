#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Build the static HR personnel-document vault from the generated employee data."""
from __future__ import annotations

import html
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPO_ROOT = ROOT.parent
data = json.loads((ROOT / "data" / "employees.json").read_text(encoding="utf-8"))
employees = data["employees"]

DEPT_LABELS = {
    "مدیریت عامل": "Management",
    "استراتژی": "Strategy",
    "بازاریابی": "Marketing",
    "فروش": "Sales",
    "تحلیل و هوش تجاری": "Intelligence",
    "منابع انسانی": "HR",
    "مالی": "Finance",
    "توسعه محصول": "Product Development",
    "طراحی": "Design",
    "فناوری اطلاعات": "IT",
    "عملیات": "Operations",
    "آموزش و محتوا": "Training & Content",
}

embedded = json.dumps(employees, ensure_ascii=False, separators=(",", ":"))

department_options = "".join(
    f'<option value="{html.escape(label)}">{html.escape(label)}</option>'
    for label in sorted(set(DEPT_LABELS.values()))
)

css = r'''
:root{--bg:#060a14;--panel:#0d1729;--panel2:#111f36;--line:#243754;--text:#edf5ff;--muted:#94a7c5;--quiet:#627695;--cyan:#55ead7;--purple:#ad83ff;--pink:#ff78aa;--gold:#f4ca6a;--green:#5ce6a5;--blue:#77a8ff;--shadow:0 22px 58px #0005}
*{box-sizing:border-box}html{scroll-behavior:smooth}body{margin:0;min-height:100vh;color:var(--text);font-family:Inter,ui-sans-serif,system-ui,-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif;background:radial-gradient(circle at 10% -10%,#1b2c4c 0,#070b16 38%,#050810 100%);-webkit-font-smoothing:antialiased}body:before{content:"";position:fixed;inset:0;pointer-events:none;opacity:.07;background-image:linear-gradient(#fff 1px,transparent 1px),linear-gradient(90deg,#fff 1px,transparent 1px);background-size:60px 60px;mask-image:linear-gradient(to bottom,black,transparent 75%)}a{color:inherit;text-decoration:none}button,input,select{font:inherit}.shell{max-width:1580px;margin:auto;padding:0 28px 38px}.topbar{height:78px;display:flex;justify-content:space-between;align-items:center;gap:18px;border-bottom:1px solid var(--line)}.brand{display:flex;align-items:center;gap:10px}.brand img{width:37px;height:37px}.brand-label{font-weight:800;font-size:12px;letter-spacing:.04em}.brand-sub{margin-top:1px;color:var(--cyan);font-size:8px;letter-spacing:.18em}.toplinks{display:flex;align-items:center;gap:8px}.toplinks a{padding:8px 11px;border:1px solid var(--line);border-radius:10px;color:var(--muted);font-size:10px;background:#0b1425aa}.toplinks a:hover{color:var(--text);border-color:var(--cyan)}.crumbs{margin-top:25px;color:var(--quiet);font-size:10px}.crumbs strong{color:var(--cyan);font-weight:600}.hero{display:flex;justify-content:space-between;align-items:end;gap:20px;margin:12px 0 20px}.kicker{color:var(--cyan);font-size:10px;letter-spacing:.16em;text-transform:uppercase;font-weight:750}.hero h1{margin:7px 0 6px;font-size:clamp(28px,4vw,43px);letter-spacing:-.05em;line-height:1.05}.hero p{margin:0;color:var(--muted);font-size:12px}.hero-side{color:var(--muted);font-size:10px;text-align:right;line-height:1.65}.hero-side b{color:var(--text)}.notice{display:flex;align-items:flex-start;gap:10px;padding:12px 15px;border:1px solid #665226;border-radius:14px;color:#f8dfa0;background:#2a210f;margin-bottom:17px;font-size:11px;line-height:1.55}.notice-icon{color:var(--gold);font-size:15px;line-height:1}.stats{display:grid;grid-template-columns:repeat(4,1fr);gap:12px;margin-bottom:14px}.stat{position:relative;overflow:hidden;padding:15px;border:1px solid var(--line);border-radius:16px;background:linear-gradient(145deg,#13233c,#0c1424)}.stat:after{content:"";position:absolute;right:-26px;top:-44px;width:100px;height:100px;border-radius:50%;background:var(--accent);opacity:.1}.stat-label{color:var(--muted);font-size:10px}.stat-value{margin-top:6px;color:var(--accent);font-size:26px;font-weight:750;letter-spacing:-.05em}.stat-foot{color:var(--quiet);font-size:9px}.panel{border:1px solid var(--line);border-radius:20px;background:rgba(10,18,32,.88);box-shadow:var(--shadow)}.toolbar{display:flex;align-items:end;gap:10px;flex-wrap:wrap;padding:17px;border-bottom:1px solid var(--line)}.control{display:grid;gap:6px;min-width:160px;flex:1}.control.search-control{min-width:280px;flex:2}.control label{color:var(--quiet);font-size:9px;letter-spacing:.08em;text-transform:uppercase}.control input,.control select{width:100%;height:39px;border:1px solid var(--line);border-radius:10px;outline:0;color:var(--text);background:#091323;padding:0 11px;font-size:11px}.control input:focus,.control select:focus{border-color:var(--cyan);box-shadow:0 0 0 3px #55ead71c}.toolbar-link{height:39px;display:inline-flex;align-items:center;padding:0 11px;border:1px solid var(--line);border-radius:10px;color:var(--muted);font-size:10px;white-space:nowrap}.toolbar-link:hover{color:var(--cyan);border-color:var(--cyan)}.table-head{display:flex;justify-content:space-between;align-items:center;gap:10px;padding:16px 17px 10px}.table-title{font-size:14px;font-weight:750}.table-sub{margin-top:2px;color:var(--muted);font-size:10px}.result{color:var(--muted);font-size:10px}.result b{color:var(--cyan)}.table-wrap{overflow-x:auto}.docs-table{width:100%;min-width:960px;border-collapse:collapse}.docs-table th{padding:10px 17px;color:var(--quiet);background:rgba(9,16,29,.6);border-top:1px solid rgba(156,187,231,.08);border-bottom:1px solid var(--line);font-size:9px;font-weight:600;letter-spacing:.08em;text-align:left;text-transform:uppercase;white-space:nowrap}.docs-table td{padding:12px 17px;border-bottom:1px solid rgba(156,187,231,.1);vertical-align:middle;font-size:10px}.docs-table tr:hover td{background:rgba(36,63,97,.14)}.person{display:flex;align-items:center;gap:9px;min-width:175px}.person-mark{width:31px;height:31px;display:grid;place-items:center;flex:none;border:1px solid rgba(85,234,215,.27);border-radius:9px;color:var(--cyan);background:linear-gradient(135deg,#143c4b,#312358);font-size:9px;font-weight:800}.person-name{color:var(--text);font-size:11px;font-weight:700;white-space:nowrap}.person-id{margin-top:1px;color:var(--cyan);font-size:9px}.role{min-width:155px;color:#bccbe1;line-height:1.45}.dept{color:var(--muted);line-height:1.45}.dept b{display:block;color:var(--text);font-weight:600}.doc-list{display:flex;flex-wrap:wrap;gap:5px;min-width:390px}.doc-link{display:inline-flex;align-items:center;min-height:24px;padding:3px 7px;border:1px solid rgba(119,168,255,.22);border-radius:7px;color:#bcd2ff;background:rgba(51,86,144,.16);font-size:9px;white-space:nowrap}.doc-link:hover{color:#fff;border-color:var(--cyan);background:rgba(85,234,215,.11)}.doc-link.profile{color:#bfa6ff;border-color:rgba(173,131,255,.28);background:rgba(91,57,155,.16)}.doc-link.check{color:#f5d588;border-color:rgba(244,202,106,.25);background:rgba(122,85,22,.15)}.status{display:inline-flex;align-items:center;gap:5px;padding:5px 7px;border:1px solid rgba(244,202,106,.25);border-radius:7px;color:#ebcf88;background:rgba(104,73,18,.16);font-size:9px;white-space:nowrap}.status i{width:5px;height:5px;border-radius:50%;background:var(--gold);box-shadow:0 0 7px var(--gold)}.open-profile{display:inline-flex;align-items:center;padding:6px 8px;border:1px solid rgba(85,234,215,.27);border-radius:8px;color:var(--cyan);font-size:9px;white-space:nowrap}.open-profile:hover{background:rgba(85,234,215,.09)}.empty{padding:45px;color:var(--muted);text-align:center;font-size:12px}.footer{display:flex;justify-content:space-between;gap:20px;margin-top:17px;color:var(--quiet);font-size:9px}.footer a{color:var(--cyan)}@media(max-width:800px){.shell{padding:0 15px 28px}.topbar{height:68px}.toplinks a:nth-child(2){display:none}.hero{align-items:flex-start;flex-direction:column}.hero-side{text-align:left}.stats{grid-template-columns:repeat(2,1fr)}.toolbar{display:grid;grid-template-columns:1fr 1fr}.control.search-control{min-width:0;grid-column:1/-1}.toolbar-link{justify-content:center}}@media(max-width:500px){.toplinks a:nth-child(3){display:none}.stats{gap:8px}.stat{padding:12px}.stat-value{font-size:22px}.toolbar{display:grid;grid-template-columns:1fr}.control.search-control{grid-column:auto}.footer{align-items:flex-start;flex-direction:column}}
'''

html_doc = f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="theme-color" content="#070b16"><link rel="icon" type="image/svg+xml" href="assets/babak-logo.svg">
<title>Babak's Ai Company - AI Company OS</title><style>{css}</style>
</head>
<body>
<main class="shell">
<header class="topbar"><a class="brand" href="dashboard.html"><img src="assets/babak-logo.svg" alt="Babak AI Company logo"><div><div class="brand-label">BABAK AI COMPANY</div><div class="brand-sub">AI COMPANY OS</div></div></a><nav class="toplinks"><a href="dashboard.html">← Dashboard</a><a href="hr/index.html">People directory</a><a href="hr/data/employees-list.md">Plain list</a></nav></header>
<div class="crumbs">Company OS <span> / </span> Departments <span> / </span> <strong>HR · Personnel Documents</strong></div>
<section class="hero"><div><div class="kicker">HR DOCUMENT VAULT / 02</div><h1>Personnel Documents</h1><p>Every employee file, document link and verification status in one place.</p></div><div class="hero-side"><b>72 employee files</b><br>Static demo vault · ready for private storage</div></section>
<div class="notice"><span class="notice-icon">◈</span><div><b>Demo document vault.</b> All records below are synthetic. Identity documents, signed contracts, insurance and tax originals are intentionally marked as pending and must never be stored in this public repository.</div></div>
<section class="stats"><div class="stat" style="--accent:var(--cyan)"><div class="stat-label">Employee files</div><div class="stat-value">72</div><div class="stat-foot">One folder per person</div></div><div class="stat" style="--accent:var(--purple)"><div class="stat-label">Internal documents</div><div class="stat-value">360</div><div class="stat-foot">5 generated records each</div></div><div class="stat" style="--accent:var(--gold)"><div class="stat-label">Originals pending</div><div class="stat-value">72</div><div class="stat-foot">Private upload required</div></div><div class="stat" style="--accent:var(--pink)"><div class="stat-label">Departments</div><div class="stat-value">12</div><div class="stat-foot">HR directory mapped</div></div></section>
<section class="panel"><div class="toolbar"><div class="control search-control"><label for="search">Search employee files</label><input id="search" type="search" placeholder="Name, personnel ID, role or department…"></div><div class="control"><label for="department">Department</label><select id="department"><option value="">All departments</option>{department_options}</select></div><div class="control"><label for="docType">Document type</label><select id="docType"><option value="all">All documents</option><option value="profile">Personnel file</option><option value="employment">Employment</option><option value="education">Education</option><option value="compensation">Compensation</option><option value="family">Family</option><option value="checklist">Checklist</option></select></div><div class="control"><label for="statusFilter">Verification</label><select id="statusFilter"><option value="all">All statuses</option><option value="demo">Demo files ready</option><option value="pending">Original documents pending</option></select></div><a class="toolbar-link" href="hr/data/employees.csv" download>Download CSV ↓</a></div>
<div class="table-head"><div><div class="table-title">All employee files</div><div class="table-sub">Select a document to open it, or open the full profile.</div></div><div class="result">Showing <b id="resultCount">72</b> of 72</div></div>
<div class="table-wrap"><table class="docs-table"><thead><tr><th>Employee</th><th>Role</th><th>Department</th><th>Document set</th><th>Originals</th><th>Profile</th></tr></thead><tbody id="documentRows"></tbody></table></div></section>
<footer class="footer"><span>Babak's Ai Company · AI Company OS · HR module</span><span>Next step: connect this vault to private Supabase storage and role-based access.</span></footer>
</main>
<script>
const employees = {embedded};
const departmentLabels = {json.dumps(DEPT_LABELS, ensure_ascii=False, separators=(',', ':'))};
const documentRows = document.getElementById('documentRows');
const resultCount = document.getElementById('resultCount');
const search = document.getElementById('search');
const department = document.getElementById('department');
const docType = document.getElementById('docType');
const statusFilter = document.getElementById('statusFilter');
const esc = value => String(value ?? '').replace(/[&<>"']/g, c => ({{'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}}[c]));
const initials = value => String(value).trim().split(/\\s+/).slice(0,2).map(part => part[0] || '').join('').toUpperCase();
const documentMeta = [
  ['profile','Personnel file','profile.md','profile'],
  ['employment','Employment','documents/employment-record.md',''],
  ['education','Education','documents/education-record.md',''],
  ['compensation','Compensation','documents/compensation-record.md',''],
  ['family','Family','documents/family-record.md',''],
  ['checklist','Checklist','documents/document-checklist.md','check'],
];
function render() {{
  const query = search.value.trim().toLowerCase();
  const selectedDepartment = department.value;
  const selectedType = docType.value;
  const selectedStatus = statusFilter.value;
  const list = employees.filter(e => {{
    const departmentName = departmentLabels[e.department] || e.department;
    const haystack = [e.full_name,e.employee_id,e.role,e.department,departmentName].join(' ').toLowerCase();
    return (!query || haystack.includes(query)) && (!selectedDepartment || departmentName === selectedDepartment) && (selectedType === 'all' || documentMeta.some(doc => doc[0] === selectedType)) && (selectedStatus === 'all' || selectedStatus === 'demo' || selectedStatus === 'pending');
  }});
  resultCount.textContent = list.length.toLocaleString('en-US');
  if (!list.length) {{ documentRows.innerHTML = '<tr><td colspan="6"><div class="empty">No employee files match these filters.</div></td></tr>'; return; }}
  documentRows.innerHTML = list.map(e => {{
    const base = 'hr/employees/' + encodeURIComponent(e.employee_id) + '/';
    const docs = documentMeta.filter(doc => selectedType === 'all' || doc[0] === selectedType).map(doc => `<a class="doc-link ${{doc[3]}}" href="${{base + doc[2]}}">${{doc[1]}}</a>`).join('');
    return `<tr><td><div class="person"><span class="person-mark">${{esc(initials(e.full_name))}}</span><div><div class="person-name">${{esc(e.full_name)}}</div><div class="person-id">${{esc(e.employee_id)}}</div></div></div></td><td><div class="role">${{esc(e.role)}}</div></td><td><div class="dept"><b>${{esc(departmentLabels[e.department] || e.department)}}</b><span>${{esc(e.department)}}</span></div></td><td><div class="doc-list">${{docs}}</div></td><td><span class="status"><i></i>Pending originals</span></td><td><a class="open-profile" href="${{base}}index.html">Open file ↗</a></td></tr>`;
  }}).join('');
}}
[search,department,docType,statusFilter].forEach(el => el.addEventListener('input', render));
render();
</script>
</body></html>
'''
(ROOT.parent / "hr-documents.html").write_text(html_doc, encoding="utf-8")
print(f"built {ROOT.parent / 'hr-documents.html'} with {len(employees)} employee files")
