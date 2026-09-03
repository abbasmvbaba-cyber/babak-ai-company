#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Build the static Persian HR directory from hr/data/employees.json."""
from __future__ import annotations

import json
import html
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
data = json.loads((ROOT / "data" / "employees.json").read_text(encoding="utf-8"))
employees = data["employees"]
counts = data["counts"]
departments = sorted({e["department"] for e in employees})
embedded = json.dumps(employees, ensure_ascii=False, separators=(",", ":"))

css = r'''
:root{--bg:#060a14;--panel:#0f1829;--panel2:#111f35;--line:#233653;--text:#edf5ff;--muted:#91a4c4;--cyan:#39e7d4;--purple:#aa83ff;--pink:#ff6b9d;--amber:#ffd166;--green:#55e6a5}
*{box-sizing:border-box}html{scroll-behavior:smooth}body{margin:0;min-height:100vh;background:radial-gradient(ellipse at 8% 0%,#182d4c 0,#070b16 35%,#050810 100%);color:var(--text);font-family:Tahoma,Arial,sans-serif;line-height:1.7}body:before{content:"";position:fixed;inset:0;pointer-events:none;opacity:.14;background-image:linear-gradient(#fff 1px,transparent 1px),linear-gradient(90deg,#fff 1px,transparent 1px);background-size:56px 56px;mask-image:linear-gradient(to bottom,black,transparent 70%)}a{color:inherit}.wrap{max-width:1440px;margin:0 auto;padding:24px}.topbar{display:flex;align-items:center;justify-content:space-between;gap:18px;margin-bottom:26px}.brand{display:flex;gap:12px;align-items:center}.brandmark{width:42px;height:42px;display:grid;place-items:center;border:1px solid var(--cyan);border-radius:13px;color:var(--cyan);font-size:24px;font-weight:bold;box-shadow:0 0 20px #19d3c555}.eyebrow{font-size:11px;color:var(--cyan);letter-spacing:.12em}.brandname{font-size:18px;font-weight:bold}.toplinks{display:flex;gap:10px;align-items:center}.toplinks a{border:1px solid var(--line);border-radius:11px;padding:8px 13px;text-decoration:none;color:var(--muted);font-size:13px;background:#0a1120aa}.toplinks a:hover{border-color:var(--cyan);color:var(--text)}.notice{display:flex;gap:10px;align-items:flex-start;padding:13px 16px;border:1px solid #6e5726;background:#2b2110;border-radius:16px;color:#ffe6a3;font-size:13px;margin-bottom:22px}.notice strong{color:#fff2c8}.hero{display:flex;align-items:flex-end;justify-content:space-between;gap:20px;margin-bottom:20px}.hero h1{font-size:34px;line-height:1.3;margin:5px 0 7px}.hero p{color:var(--muted);margin:0}.updated{font-size:12px;color:var(--muted);text-align:left}.statgrid{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:13px;margin-bottom:14px}.stat{position:relative;overflow:hidden;background:linear-gradient(145deg,#12213a,#0c1322);border:1px solid var(--line);border-radius:18px;padding:17px 18px}.stat:after{content:"";position:absolute;width:100px;height:100px;border-radius:50%;right:-28px;top:-43px;background:var(--accent);opacity:.08;filter:blur(2px)}.statlabel{color:var(--muted);font-size:13px}.statvalue{font-size:30px;font-weight:bold;margin-top:2px;color:var(--accent)}.statfoot{color:var(--muted);font-size:12px}.distribution{display:flex;flex-wrap:wrap;gap:10px;margin:0 0 22px}.dist{display:flex;gap:9px;align-items:center;padding:8px 12px;border:1px solid var(--line);border-radius:999px;background:#0c1424aa;color:var(--muted);font-size:13px}.dist b{color:var(--text)}.dot{width:9px;height:9px;border-radius:50%;background:var(--accent);box-shadow:0 0 11px var(--accent)}.panel{background:rgba(10,18,32,.84);border:1px solid var(--line);border-radius:22px;padding:18px}.filters{display:grid;grid-template-columns:minmax(260px,2fr) repeat(3,minmax(150px,1fr));gap:10px;margin-bottom:15px}.input,.select{width:100%;border:1px solid var(--line);border-radius:12px;background:#0b1424;color:var(--text);padding:11px 13px;font:inherit;font-size:13px;outline:none}.input:focus,.select:focus{border-color:var(--cyan);box-shadow:0 0 0 3px #39e7d422}.resultbar{display:flex;justify-content:space-between;align-items:center;color:var(--muted);font-size:13px;margin-bottom:13px}.resultbar b{color:var(--cyan)}.cards{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:13px}.card{display:flex;flex-direction:column;min-width:0;background:linear-gradient(160deg,#121f35,#0d1525);border:1px solid #233653;border-radius:18px;padding:13px;transition:transform .18s,border-color .18s,box-shadow .18s}.card:hover{transform:translateY(-3px);border-color:#39e7d4aa;box-shadow:0 12px 34px #0007}.cardtop{display:flex;gap:12px;align-items:center}.avatar{width:65px;height:65px;flex:none;border:1px solid #355273;border-radius:15px;background:#091224}.cardname{font-weight:bold;font-size:16px;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}.cardrole{color:#cbd8ef;font-size:12px;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}.id{color:var(--cyan);font-size:11px;margin-top:3px}.tags{display:flex;gap:5px;flex-wrap:wrap;margin:12px 0 9px}.tag{font-size:11px;border-radius:999px;padding:3px 7px;background:#172844;color:var(--muted);border:1px solid #274466}.tag.gender-w{color:#ffadd0;border-color:#6e3654;background:#30192d}.tag.gender-m{color:#95caff;border-color:#315d86;background:#122a43}.detail{display:grid;grid-template-columns:1fr 1fr;gap:7px;border-top:1px solid #20304a;padding-top:10px;margin-top:auto}.detail div{min-width:0}.detail span{display:block;color:var(--muted);font-size:10px}.detail b{display:block;font-size:12px;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}.salary{color:var(--pink)!important}.cardlink{display:block;text-align:center;text-decoration:none;border:1px solid #2a4c61;border-radius:10px;padding:6px 8px;margin-top:12px;color:var(--cyan);font-size:12px}.cardlink:hover{background:#10283a}.empty{text-align:center;padding:48px 20px;color:var(--muted);border:1px dashed #2d4667;border-radius:16px;grid-column:1/-1}.footer{display:flex;justify-content:space-between;gap:20px;align-items:center;color:var(--muted);font-size:12px;padding:20px 3px 8px}.footer a{color:var(--cyan);text-decoration:none}@media(max-width:1100px){.cards{grid-template-columns:repeat(3,minmax(0,1fr))}}@media(max-width:820px){.statgrid{grid-template-columns:repeat(2,minmax(0,1fr))}.filters{grid-template-columns:1fr 1fr}.filters .search{grid-column:1/-1}.hero{align-items:flex-start;flex-direction:column}.updated{text-align:right}}@media(max-width:560px){.wrap{padding:15px}.topbar{align-items:flex-start;flex-direction:column}.toplinks{width:100%}.toplinks a{flex:1;text-align:center}.hero h1{font-size:27px}.cards{grid-template-columns:1fr}.filters{grid-template-columns:1fr}.filters .search{grid-column:auto}.footer{align-items:flex-start;flex-direction:column}}
'''

html_doc = f'''<!doctype html>
<html lang="fa" dir="rtl">
<head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="theme-color" content="#070b16">
<title>دایرکتوری پرسنلی | کمپانی هوش مصنوعی بابک</title>
<style>{css}</style>
</head>
<body>
<main class="wrap">
  <header class="topbar">
    <div class="brand"><div class="brandmark">ب</div><div><div class="eyebrow">BABAK AI COMPANY</div><div class="brandname">کمپانی هوش مصنوعی بابک · منابع انسانی</div></div></div>
    <nav class="toplinks"><a href="../index.html">داشبورد اصلی</a><a href="data/employees.csv" download>دریافت CSV</a><a href="data/employees.json" download>دریافت JSON</a></nav>
  </header>
  <div class="notice"><span>◈</span><div><strong>محیط نمونه‌سازی HR</strong> — همهٔ رکوردها ساختگی هستند. کدهای ملی عمداً غیرمعتبرند و تصویرها آواتار برداری‌اند؛ هیچ اطلاعات هویتی واقعی را در رپوی عمومی ذخیره نکنید.</div></div>
  <section class="hero"><div><div class="eyebrow">HR DIRECTORY / 01</div><h1>دایرکتوری ۷۲ نفره شرکت</h1><p>فهرست مرکزی پرسنل، دپارتمان‌ها و لینک ورود به پروندهٔ اختصاصی هر نفر</p></div><div class="updated">آخرین تولید داده: <b>{html.escape(data['generated_at'])}</b><br>نسخهٔ نمایشی قابل اتصال به Supabase</div></section>
  <section class="statgrid">
    <div class="stat" style="--accent:var(--cyan)"><div class="statlabel">کل پرسنل</div><div class="statvalue">۷۲</div><div class="statfoot">رکورد فعال نمونه</div></div>
    <div class="stat" style="--accent:var(--pink)"><div class="statlabel">خانم‌ها</div><div class="statvalue">۵۸</div><div class="statfoot">۸۰٫۶٪ از شرکت</div></div>
    <div class="stat" style="--accent:#7ab9ff"><div class="statlabel">آقایان</div><div class="statvalue">۱۴</div><div class="statfoot">۱۹٫۴٪ از شرکت</div></div>
    <div class="stat" style="--accent:var(--amber)"><div class="statlabel">دارای دکتری</div><div class="statvalue">۴</div><div class="statfoot">رکورد تحصیلی نمونه</div></div>
  </section>
  <div class="distribution">
    <div class="dist" style="--accent:var(--purple)"><i class="dot"></i><b>۱۴ نفر</b> · ۲۰ تا ۲۴ سال</div>
    <div class="dist" style="--accent:var(--cyan)"><i class="dot"></i><b>۳۶ نفر</b> · ۲۵ تا ۳۰ سال</div>
    <div class="dist" style="--accent:var(--pink)"><i class="dot"></i><b>۲۲ نفر</b> · ۳۱ سال به بالا</div>
    <div class="dist" style="--accent:var(--green)"><i class="dot"></i><b>۱۲ دپارتمان</b> · متصل به ۸ تیم Agency</div>
  </div>
  <section class="panel">
    <div class="filters">
      <input id="search" class="input search" type="search" placeholder="جست‌وجو بر اساس نام، شماره پرسنلی، سمت یا دپارتمان…" aria-label="جست‌وجو">
      <select id="department" class="select" aria-label="دپارتمان"><option value="">همه دپارتمان‌ها</option>{''.join(f'<option>{html.escape(d)}</option>' for d in departments)}</select>
      <select id="gender" class="select" aria-label="جنسیت"><option value="">همه جنسیت‌ها</option><option value="زن">خانم‌ها</option><option value="مرد">آقایان</option></select>
      <select id="age" class="select" aria-label="بازه سنی"><option value="">همه سنین</option><option value="۲۰ تا ۲۴ سال">۲۰ تا ۲۴ سال</option><option value="۲۵ تا ۳۰ سال">۲۵ تا ۳۰ سال</option><option value="۳۱ سال به بالا">۳۱ سال به بالا</option></select>
    </div>
    <div class="resultbar"><span>نتایج: <b id="resultCount">۷۲</b> نفر</span><span>برای مشاهدهٔ جزئیات، پروندهٔ هر فرد را باز کنید.</span></div>
    <div id="cards" class="cards"></div>
  </section>
  <footer class="footer"><span>© ۲۰۲۶ کمپانی هوش مصنوعی بابک · HR demo data</span><span>پرونده‌ها در مسیر <a href="employees/BAC-0001/index.html">employees/BAC-xxxx</a> قرار دارند.</span></footer>
</main>
<script>
const employees = {embedded};
const cards = document.getElementById('cards');
const search = document.getElementById('search');
const department = document.getElementById('department');
const gender = document.getElementById('gender');
const age = document.getElementById('age');
const count = document.getElementById('resultCount');
const faDigits = value => String(value).replace(/\\d/g, d => '۰۱۲۳۴۵۶۷۸۹'[d]);
const esc = value => String(value ?? '').replace(/[&<>"']/g, c => ({{'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}}[c]));
function render() {{
  const q = search.value.trim().toLowerCase();
  const list = employees.filter(e => {{
    const haystack = [e.full_name,e.employee_id,e.role,e.department,e.agency_team].join(' ').toLowerCase();
    return (!q || haystack.includes(q)) && (!department.value || e.department === department.value) && (!gender.value || e.gender === gender.value) && (!age.value || e.age_bucket === age.value);
  }});
  count.textContent = faDigits(list.length);
  cards.innerHTML = list.length ? list.map(e => `
    <article class="card">
      <div class="cardtop"><img class="avatar" src="employees/${{encodeURIComponent(e.employee_id)}}/photo.svg" alt="تصویر نمونه ${{esc(e.full_name)}}"><div style="min-width:0"><div class="cardname" title="${{esc(e.full_name)}}">${{esc(e.full_name)}}</div><div class="cardrole" title="${{esc(e.role)}}">${{esc(e.role)}}</div><div class="id">${{esc(e.employee_id)}}</div></div></div>
      <div class="tags"><span class="tag ${{e.gender === 'زن' ? 'gender-w' : 'gender-m'}}">${{e.gender === 'زن' ? 'خانم' : 'آقا'}}</span><span class="tag">${{faDigits(e.age)}} سال</span><span class="tag">${{esc(e.agency_team)}}</span></div>
      <div class="detail"><div><span>دپارتمان</span><b title="${{esc(e.department)}}">${{esc(e.department)}}</b></div><div><span>استخدام</span><b>${{esc(e.hire_date)}}</b></div><div><span>پایه حقوق</span><b class="salary">${{faDigits(e.base_salary_toman.toLocaleString('en-US'))}} تومان</b></div><div><span>تأهل</span><b>${{esc(e.family_info.marital_status)}}</b></div></div>
      <a class="cardlink" href="employees/${{encodeURIComponent(e.employee_id)}}/index.html">باز کردن پرونده ←</a>
    </article>`).join('') : '<div class="empty">رکوردی با این فیلترها پیدا نشد. عبارت جست‌وجو یا فیلترها را تغییر دهید.</div>';
}}
[search,department,gender,age].forEach(el => el.addEventListener('input', render));
render();
</script>
</body></html>
'''
(ROOT / "index.html").write_text(html_doc, encoding="utf-8")

# A plain Markdown list is useful for HR review and remains readable without JavaScript.
list_lines = [
    "# فهرست شرکتی ۷۲ پرسنل — دادهٔ نمایشی",
    "",
    "> همهٔ رکوردها ساختگی‌اند؛ کد ملی‌ها معتبر نیستند و جزئیات هر نفر در پوشهٔ اختصاصی او قرار دارد.",
    "",
    "| ردیف | شماره پرسنلی | نام و نام خانوادگی | جنسیت | سن | دپارتمان | سمت | استخدام | پایه حقوق (تومان) | تأهل | پرونده |",
    "|---:|---|---|---|---:|---|---|---|---:|---|---|",
]
for index, e in enumerate(employees, 1):
    list_lines.append(
        f"| {index} | {e['employee_id']} | {e['full_name']} | {e['gender']} | {e['age']} | {e['department']} | {e['role']} | {e['hire_date']} | {e['base_salary_toman']:,} | {e['family_info']['marital_status']} | [باز کردن](../employees/{e['employee_id']}/index.html) |"
    )
list_lines += [
    "",
    "## توزیع داده",
    "",
    f"- کل: **{counts['total']}** نفر",
    f"- خانم: **{counts['female']}** نفر؛ آقا: **{counts['male']}** نفر",
    f"- ۲۰ تا ۲۴ سال: **{counts['age_20_24']}** نفر؛ ۲۵ تا ۳۰ سال: **{counts['age_25_30']}** نفر؛ ۳۱ سال به بالا: **{counts['age_31_plus']}** نفر",
    f"- دارای دکتری: **{counts['doctorates']}** نفر",
]
(ROOT / "data" / "employees-list.md").write_text("\n".join(list_lines) + "\n", encoding="utf-8")
print(f"built {ROOT / 'index.html'} and {ROOT / 'data/employees-list.md'} with {len(employees)} records")
