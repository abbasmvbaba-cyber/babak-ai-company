#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Generate a fully synthetic HR demo dataset for Babak AI Company.

The generated files intentionally use non-valid demo national-code placeholders and
vector avatars. Replace them only inside a private, access-controlled HR system.
"""
from __future__ import annotations

import csv
import html
import json
import shutil
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EMPLOYEES_DIR = ROOT / "employees"
DATA_DIR = ROOT / "data"
CURRENT_GREGORIAN = date(2026, 9, 3)
CURRENT_JALALI = "1405/06/12"

# All names in this file are synthetic demo records. They are not intended to
# identify real people.
FEMALE_GIVEN = [
    "آوا", "آناهیتا", "آتوسا", "افسانه", "الهام", "الینا", "الناز", "بهاره",
    "پرنیا", "پریسا", "پگاه", "ترانه", "ثنا", "جمیله", "حنانه", "درسا",
    "دریا", "دنیا", "رها", "روژان", "سارا", "سمیرا", "سپیده", "سحر",
    "سمانه", "شبنم", "شیوا", "صبا", "طناز", "عاطفه", "غزل", "فاطمه",
    "فرزانه", "فرنوش", "کتایون", "کیانا", "مریم", "مهسا", "مهشید", "مژگان",
    "نازنین", "نرگس", "نگار", "نیایش", "نیکی", "هانیه", "هلیا", "یاسمن",
    "یلدا", "لیلا", "لادن", "مونا", "مهتاب", "نوشین", "ویدا", "یگانه",
    "راضیه", "آیدا",
]
MALE_GIVEN = [
    "آرمان", "امیر", "امیرحسین", "بهنام", "پویا", "پیمان", "حامد", "حسین",
    "سامان", "شایان", "علی", "فرهاد", "کیارش", "نوید",
]
FAMILY_NAMES = [
    "احمدی", "رضایی", "محمدی", "حسینی", "کریمی", "مرادی", "موسوی", "کاظمی",
    "اکبری", "جعفری", "حیدری", "نادری", "صادقی", "رستمی", "شریفی", "رحیمی",
    "قاسمی", "میرزایی", "فرهادی", "طاهری", "رستگار", "نوری", "یوسفی", "قربانی",
    "عباسی", "باقری", "نیک‌نام", "شمس", "مهرابی", "آقایی", "سلیمانی", "کمالی",
    "دادخواه", "زارعی", "صابری", "توکلی", "معینی", "بیات", "کاوه", "خلیلی",
    "صفری", "خرم", "پاکزاد", "نوروزی", "حبیبی", "بنی‌هاشمی", "جهانگیری", "اسماعیلی",
    "راد", "رفیعی", "دانش", "فراهانی", "گلکار", "نیک‌روش", "عابدی", "فرهمند",
    "یزدانی", "هاشمی", "بهشتی", "فدایی", "توسلی", "موحد", "افشاری", "مرعشی",
    "کیانی", "تهرانی", "امانی", "حسام‌پور", "ساعی", "ملک‌زاده", "سروش", "مقدم",
]
FATHER_NAMES = [
    "رضا", "حسن", "محمد", "محمود", "علی", "کاظم", "حسین", "مجید", "داود", "جواد",
    "مسعود", "بهرام", "فرامرز", "یوسف", "اکبر", "حبیب", "ناصر", "مرتضی", "احمد", "سعید",
    "باقر", "صمد", "رحمان", "اسماعیل", "ابراهیم", "منصور", "مهدی", "فرهاد", "بهنام", "پرویز",
]
BIRTH_CITIES = [
    "تهران", "مشهد", "اصفهان", "شیراز", "تبریز", "رشت", "اهواز", "کرمان", "یزد", "قم",
    "کرج", "ساری", "همدان", "سنندج", "ارومیه", "بندرعباس",
]
SPOUSE_MALE = [
    "میلاد", "رضا", "فرشاد", "مهدی", "مجتبی", "سعید", "علی‌رضا", "وحید", "شهاب", "یونس",
    "کاوه", "نوید", "حمید", "رامین", "امید", "اشکان", "داریوش", "احسان",
]
SPOUSE_FEMALE = [
    "مریم", "سارا", "نگار", "الهه", "نیلوفر", "شکوفه", "پریسا", "نسترن", "بهاره", "رها",
    "مهسا", "ترانه", "شبنم", "نازنین", "آیدا", "شیما", "سپیده", "الهام",
]

DEPARTMENTS = [
    {
        "name": "مدیریت عامل", "agency_team": "Direction", "field": "مدیریت کسب‌وکار",
        "roles": [
            ("مدیرعامل", "executive"), ("مدیر دفتر مدیرعامل", "director"), ("دستیار اجرایی", "coordinator"),
        ],
    },
    {
        "name": "استراتژی", "agency_team": "Strategy", "field": "مدیریت استراتژیک",
        "roles": [
            ("مدیر استراتژی", "director"), ("مشاور ارشد استراتژی", "senior"),
            ("تحلیلگر استراتژی", "specialist"), ("پژوهشگر بازار", "researcher"),
        ],
    },
    {
        "name": "بازاریابی", "agency_team": "Marketing", "field": "بازاریابی و ارتباطات",
        "roles": [
            ("مدیر بازاریابی", "director"), ("سرپرست SEO", "lead"), ("کارشناس SEO", "specialist"),
            ("مدیر شبکه‌های اجتماعی", "lead"), ("کارشناس شبکه‌های اجتماعی", "specialist"),
            ("کارشناس تبلیغات عملکردی", "specialist"), ("مدیر کمپین", "lead"),
            ("کپی‌رایتر", "specialist"), ("کارشناس ایمیل مارکتینگ", "specialist"),
            ("کارشناس روابط عمومی", "specialist"), ("کارشناس اینفلوئنسر مارکتینگ", "specialist"),
            ("تحلیلگر بازاریابی", "analyst"),
        ],
    },
    {
        "name": "فروش", "agency_team": "Sales", "field": "مدیریت بازرگانی",
        "roles": [
            ("مدیر فروش", "director"), ("سرپرست فروش", "lead"), ("کارشناس فروش سازمانی", "specialist"),
            ("کارشناس فروش سازمانی", "specialist"), ("کارشناس فروش", "specialist"),
            ("کارشناس فروش", "specialist"), ("کارشناس توسعه کسب‌وکار", "specialist"),
            ("کارشناس توسعه کسب‌وکار", "specialist"), ("کارشناس موفقیت مشتری", "specialist"),
            ("کارشناس موفقیت مشتری", "specialist"),
        ],
    },
    {
        "name": "تحلیل و هوش تجاری", "agency_team": "Intelligence", "field": "علوم داده و هوش تجاری",
        "roles": [
            ("مدیر هوش تجاری", "director"), ("دانشمند داده", "senior"), ("مهندس داده", "senior"),
            ("تحلیلگر داده", "analyst"), ("تحلیلگر هوش رقابتی", "analyst"),
            ("پژوهشگر هوش بازار", "researcher"), ("مهندس یادگیری ماشین", "senior"),
        ],
    },
    {
        "name": "منابع انسانی", "agency_team": "Managing", "field": "مدیریت منابع انسانی",
        "roles": [
            ("مدیر منابع انسانی", "director"), ("کارشناس جذب و استخدام", "specialist"),
            ("کارشناس آموزش و توسعه", "specialist"), ("کارشناس جبران خدمات", "specialist"),
            ("کارشناس منابع انسانی", "specialist"), ("دستیار منابع انسانی", "coordinator"),
        ],
    },
    {
        "name": "مالی", "agency_team": "Managing", "field": "حسابداری و مالی",
        "roles": [
            ("مدیر مالی", "director"), ("حسابدار ارشد", "senior"), ("حسابدار", "specialist"),
            ("کارشناس حقوق و دستمزد", "specialist"), ("کارشناس مالی", "specialist"),
        ],
    },
    {
        "name": "توسعه محصول", "agency_team": "Research", "field": "مهندسی کامپیوتر و محصول",
        "roles": [
            ("مدیر محصول", "director"), ("مالک محصول", "senior"), ("مدیر پروژه", "senior"),
            ("توسعه‌دهنده ارشد", "senior"), ("توسعه‌دهنده Front-end", "specialist"),
            ("توسعه‌دهنده Back-end", "specialist"), ("مهندس QA", "specialist"),
            ("مهندس DevOps و زیرساخت", "specialist"),
        ],
    },
    {
        "name": "طراحی", "agency_team": "Content", "field": "طراحی تجربه کاربر",
        "roles": [
            ("مدیر طراحی", "director"), ("طراح ارشد UI/UX", "senior"), ("طراح UI/UX", "specialist"),
            ("گرافیست", "specialist"), ("طراح حرکت و ویدیو", "specialist"),
        ],
    },
    {
        "name": "فناوری اطلاعات", "agency_team": "Research", "field": "فناوری اطلاعات",
        "roles": [
            ("مدیر فناوری اطلاعات", "director"), ("کارشناس شبکه", "specialist"),
            ("کارشناس پشتیبانی IT", "specialist"), ("کارشناس امنیت اطلاعات", "specialist"),
        ],
    },
    {
        "name": "عملیات", "agency_team": "Managing", "field": "مدیریت عملیات",
        "roles": [
            ("مدیر عملیات", "director"), ("کارشناس عملیات", "specialist"),
            ("مسئول اداری", "specialist"), ("مسئول تدارکات", "specialist"),
            ("کارشناس کنترل کیفیت", "specialist"),
        ],
    },
    {
        "name": "آموزش و محتوا", "agency_team": "Content", "field": "علوم تربیتی و تولید محتوا",
        "roles": [
            ("مدیر آموزش و محتوا", "director"), ("مدرس سازمانی", "specialist"),
            ("نویسنده و تهیه‌کننده محتوای آموزشی", "specialist"),
        ],
    },
]

# 14 male positions distributed through the organization; all other records are female.
MALE_POSITIONS = {2, 5, 10, 16, 23, 28, 33, 39, 44, 50, 54, 57, 62, 66}

# Exactly 22 leadership/senior records are placed in the 31+ age bucket.
# A few senior specialists remain in the 25–30 bucket to keep the requested distribution exact.
AGE_31_PLUS_POSITIONS = {
    0, 1, 3, 4, 7, 8, 10, 13, 19, 20, 29, 30, 36, 42, 43, 47, 48, 49, 55, 56, 60, 64,
}
SENIOR_AGES = [31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 34, 36, 38, 42]
YOUNG_AGES = [20, 21, 22, 23, 24, 20, 21, 22, 23, 24, 20, 21, 22, 24]
MID_AGES = [25, 26, 27, 28, 29, 30] * 6

# Four synthetic doctoral records, selected for plausible senior analytical/leadership roles.
DOCTORATE_POSITIONS = {30, 32, 47, 57}

PALETTE = [
    ("#071b31", "#19d3c5", "#ffcc8a"), ("#1e1034", "#a879ff", "#f4c1a1"),
    ("#10261c", "#55e6a5", "#d8a77b"), ("#2a1421", "#ff6b9d", "#e8b48e"),
    ("#171d36", "#6cb8ff", "#c98e6f"), ("#28200e", "#ffd166", "#bc805f"),
]


def g2j(gy: int, gm: int, gd: int) -> tuple[int, int, int]:
    """Gregorian to Jalali conversion, adequate for these demo dates."""
    gdm = [0, 31, 59, 90, 120, 151, 181, 212, 243, 273, 304, 334]
    if gy > 1600:
        jy = 979
        gy -= 1600
    else:
        jy = 0
        gy -= 621
    gy2 = gy + 1 if gm > 2 else gy
    days = 365 * gy + (gy2 + 3) // 4 - (gy2 + 99) // 100 + (gy2 + 399) // 400 + gd + gdm[gm - 1]
    if gm > 2 and ((gy % 4 == 0 and gy % 100 != 0) or gy % 400 == 0):
        days += 1
    days -= 80
    jy += 33 * (days // 12053)
    days %= 12053
    jy += 4 * (days // 1461)
    days %= 1461
    if days > 365:
        jy += (days - 1) // 365
        days = (days - 1) % 365
    if days < 186:
        jm = 1 + days // 31
        jd = 1 + days % 31
    else:
        jm = 7 + (days - 186) // 30
        jd = 1 + (days - 186) % 30
    return jy, jm, jd


def jalali_date(year: int, month: int, day: int) -> str:
    return f"{year:04d}/{month:02d}/{day:02d}"


def age_birth_date(age: int, index: int) -> tuple[date, str, int]:
    # Months are kept before September so the age is exact on 1405/06/12.
    month = [1, 2, 3, 4, 5, 6, 7, 8][index % 8]
    day = [3, 11, 19, 27, 7, 15, 23, 9][index % 8]
    birth = date(CURRENT_GREGORIAN.year - age, month, day)
    jy, jm, jd = g2j(birth.year, birth.month, birth.day)
    return birth, jalali_date(jy, jm, jd), jy


def is_age_exact(birth: date, age: int) -> bool:
    years = CURRENT_GREGORIAN.year - birth.year - ((CURRENT_GREGORIAN.month, CURRENT_GREGORIAN.day) < (birth.month, birth.day))
    return years == age


def salary_for(title: str, level: str, number: int) -> int:
    if title == "مدیرعامل":
        base = 180_000_000
    elif level == "director":
        base = 95_000_000
    elif level in {"lead", "senior"}:
        base = 70_000_000
    elif "دانشمند" in title or "مهندس یادگیری" in title:
        base = 68_000_000
    elif "توسعه‌دهنده" in title:
        base = 58_000_000
    elif "مهندس" in title:
        base = 55_000_000
    elif "پژوهشگر" in title:
        base = 52_000_000
    elif "تحلیلگر" in title:
        base = 48_000_000
    elif "طراح" in title or "گرافیست" in title:
        base = 45_000_000
    elif "حسابدار" in title or "مالی" in title:
        base = 44_000_000
    elif "دستیار" in title or "هماهنگ" in title:
        base = 30_000_000
    elif "مدرس" in title or "نویسنده" in title:
        base = 42_000_000
    else:
        base = 38_000_000
    adjustment = ((number * 3) % 7) * 1_000_000
    return base + adjustment


def education_records(birth_jyear: int, age: int, field: str, number: int, doctorate: bool) -> list[dict]:
    diploma_fields = ["ریاضی و فیزیک", "علوم تجربی", "ادبیات و علوم انسانی", "فنی و حرفه‌ای"]
    diploma_field = diploma_fields[number % len(diploma_fields)]
    diploma_start = birth_jyear + 15
    diploma_issue = birth_jyear + 18
    bachelor_start = birth_jyear + 18
    bachelor_issue = birth_jyear + 22
    bachelor_done = age >= 23
    if not bachelor_done:
        bachelor_status = "در حال تحصیل"
        bachelor_issue_text = "در حال تحصیل"
    else:
        bachelor_status = "اخذ شده"
        bachelor_issue_text = jalali_date(bachelor_issue, 6, 20)

    records = [
        {
            "level": "دیپلم", "field": diploma_field, "institution": "دبیرستان نمونه ایرانیان",
            "start_date": jalali_date(diploma_start, 7, 1),
            "issue_date": jalali_date(diploma_issue, 3, 15), "status": "اخذ شده",
        },
        {
            "level": "کارشناسی", "field": field, "institution": "دانشگاه نمونه ایرانیان",
            "start_date": jalali_date(bachelor_start, 7, 1),
            "issue_date": bachelor_issue_text, "status": bachelor_status,
        },
    ]

    master_possible = age >= 27 and ((number + age) % 3 != 1)
    if master_possible:
        master_start = birth_jyear + 22
        master_issue = birth_jyear + 24
        master_done = age >= 26
        records.append({
            "level": "کارشناسی ارشد", "field": field, "institution": "دانشگاه نمونه ایرانیان",
            "start_date": jalali_date(master_start, 7, 1),
            "issue_date": jalali_date(master_issue, 6, 20) if master_done else "در حال تحصیل",
            "status": "اخذ شده" if master_done else "در حال تحصیل",
        })
    else:
        records.append({
            "level": "کارشناسی ارشد", "field": "—", "institution": "—", "start_date": "—",
            "issue_date": "ندارد", "status": "ندارد",
        })

    if doctorate:
        doctorate_start = birth_jyear + 24
        doctorate_issue = birth_jyear + 28
        records.append({
            "level": "دکتری", "field": field, "institution": "دانشگاه نمونه ایرانیان",
            "start_date": jalali_date(doctorate_start, 7, 1),
            "issue_date": jalali_date(doctorate_issue, 4, 20), "status": "اخذ شده",
        })
    else:
        records.append({
            "level": "دکتری", "field": "—", "institution": "—", "start_date": "—",
            "issue_date": "ندارد", "status": "ندارد",
        })
    return records


def family_info(age: int, number: int, gender: str) -> dict:
    if age < 25:
        married = False
    elif age <= 27:
        married = number % 2 == 0
    else:
        married = number % 5 != 0
    if not married:
        return {"marital_status": "مجرد", "spouse_name": "ندارد", "children_count": 0}
    spouse_pool = SPOUSE_MALE if gender == "زن" else SPOUSE_FEMALE
    spouse = spouse_pool[(number + age) % len(spouse_pool)]
    children = 0 if age <= 27 else (number + age) % 3
    return {"marital_status": "متأهل", "spouse_name": spouse, "children_count": children}


def hire_date(birth_jyear: int, age: int, number: int) -> str:
    earliest = birth_jyear + 18
    desired_year = 1400 + ((number * 5) % 6)
    year = min(1405, max(earliest, desired_year))
    if year == 1405:
        month = 1 + ((number * 2) % 6)
        day = 1 + ((number * 3) % 12)
    else:
        month = 1 + ((number * 3) % 12)
        day = 1 + ((number * 7) % 27)
    return jalali_date(year, month, day)


def avatar_svg(employee: dict, number: int) -> str:
    bg, accent, skin = PALETTE[number % len(PALETTE)]
    hair = "#1c1324" if number % 3 else "#2b1b14"
    shirt = accent
    gender = employee["gender"]
    first = html.escape(employee["first_name"])
    full = html.escape(employee["full_name"])
    if gender == "زن":
        hair_shape = f'<path d="M145 232 Q145 105 256 105 Q367 105 367 232 L367 365 Q332 404 256 410 Q180 404 145 365Z" fill="{hair}"/>'
        side_hair = f'<path d="M144 247 Q118 322 155 396 Q184 421 203 386 L185 250Z M368 247 Q394 322 357 396 Q328 421 309 386 L327 250Z" fill="{hair}" opacity=".98"/>'
    else:
        hair_shape = f'<path d="M153 208 Q157 107 256 104 Q355 107 359 208 Q324 166 256 166 Q188 166 153 208Z" fill="{hair}"/>'
        side_hair = ""
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="512" height="512" viewBox="0 0 512 512" role="img" aria-label="تصویر نمونه {full}">
  <title>تصویر نمونه غیرواقعی — {full}</title>
  <rect width="512" height="512" rx="48" fill="{bg}"/>
  <circle cx="256" cy="206" r="144" fill="{accent}" opacity=".13"/>
  {hair_shape}{side_hair}
  <ellipse cx="256" cy="225" rx="93" ry="112" fill="{skin}"/>
  <path d="M188 219 Q207 204 226 219" stroke="#3a2530" stroke-width="9" fill="none" stroke-linecap="round"/>
  <path d="M286 219 Q305 204 324 219" stroke="#3a2530" stroke-width="9" fill="none" stroke-linecap="round"/>
  <circle cx="211" cy="229" r="7" fill="#241c2a"/><circle cx="301" cy="229" r="7" fill="#241c2a"/>
  <path d="M244 239 Q238 267 256 270 Q274 267 268 239" fill="none" stroke="#a46f5c" stroke-width="5"/>
  <path d="M215 296 Q256 322 297 296" stroke="#7f3f55" stroke-width="8" fill="none" stroke-linecap="round"/>
  <path d="M124 512 Q132 377 256 364 Q380 377 388 512Z" fill="{shirt}"/>
  <path d="M202 374 Q256 419 310 374" fill="none" stroke="#ffffff" stroke-opacity=".26" stroke-width="8"/>
  <rect x="24" y="24" width="112" height="38" rx="19" fill="#000" opacity=".3"/>
  <text x="80" y="50" fill="#fff" font-size="18" font-family="Tahoma,Arial" text-anchor="middle">تصویر نمونه</text>
  <text x="256" y="464" fill="#fff" font-size="22" font-family="Tahoma,Arial" text-anchor="middle">{first} · BAC-{number:04d}</text>
</svg>\n'''


def md_table(rows: list[dict]) -> str:
    lines = [
        "| مقطع | رشته | مؤسسه | تاریخ شروع | تاریخ اخذ | وضعیت |",
        "|---|---|---|---|---|---|",
    ]
    for row in rows:
        lines.append("| {level} | {field} | {institution} | {start_date} | {issue_date} | {status} |".format(**row))
    return "\n".join(lines)


def doc_header(employee: dict, title: str) -> str:
    return f"""---\nemployee_id: {employee['employee_id']}\nsynthetic_demo: true\n---\n\n# {title}\n\n> این سند دادهٔ نمایشی و غیرواقعی برای نمونه‌سازی سامانهٔ منابع انسانی «کمپانی هوش مصنوعی بابک» است و ارزش حقوقی ندارد.\n\n"""


def profile_md(employee: dict) -> str:
    family = employee["family_info"]
    return f"""---
employee_id: {employee['employee_id']}
full_name: {employee['full_name']}
department: {employee['department']}
role: {employee['role']
}
gender: {employee['gender']}
age_bucket: {employee['age_bucket']}
synthetic_demo: true
---

# پرونده پرسنلی {employee['full_name']}

> **دادهٔ کاملاً ساختگی / غیرقابل استفاده رسمی** — این پرونده برای تست رابط و گردش‌کار HR ساخته شده است. کد ملی، عکس و مدارک واقعی نیستند.

## اطلاعات شناسایی

| فیلد | مقدار |
|---|---|
| نام و نام خانوادگی | {employee['full_name']} |
| جنسیت | {employee['gender']} |
| تاریخ تولد | {employee['birth_date_jalali']} |
| سن در تاریخ {CURRENT_JALALI} | {employee['age']} سال |
| نام پدر | {employee['father_name']} |
| کد ملی نمایشی | {employee['national_code']} |
| محل تولد | {employee['birth_place']} |
| تابعیت | ایرانی |

## اطلاعات شغلی

| فیلد | مقدار |
|---|---|
| شماره پرسنلی | {employee['employee_id']} |
| دپارتمان | {employee['department']} |
| تیم Agency-in-a-BOX | {employee['agency_team']} |
| سمت | {employee['role']} |
| تاریخ استخدام | {employee['hire_date']} |
| سابقه تقریبی در شرکت | {employee['years_with_company']} سال |
| نوع همکاری | تمام‌وقت — دادهٔ نمونه |
| وضعیت | فعال — نمونه |
| ایمیل سازمانی نمونه | {employee['work_email']} |
| داخلی نمونه | {employee['extension']} |
| سرپرست مستقیم | {employee['supervisor']} |
| پایه حقوق ماهانه | {employee['base_salary_display']} |
| واحد پول | تومان |

## سوابق تحصیلی

{md_table(employee['education'])}

## وضعیت خانوادگی

| فیلد | مقدار |
|---|---|
| وضعیت تأهل | {family['marital_status']} |
| نام همسر | {family['spouse_name']} |
| تعداد فرزندان | {family['children_count']} |

## اسناد موجود در این پوشه

- [تصویر پروفایل نمونه](photo.svg)
- [خلاصه استخدام و حکم داخلی نمونه](documents/employment-record.md)
- [سوابق تحصیلی نمونه](documents/education-record.md)
- [خلاصه جبران خدمات نمونه](documents/compensation-record.md)
- [فرم وضعیت خانوادگی نمونه](documents/family-record.md)
- [چک‌لیست مدارک مورد نیاز](documents/document-checklist.md)

## یادداشت HR

این پرونده تا زمان جایگزینی داده‌های واقعی در سامانهٔ خصوصی، صرفاً برای تست است. مدارک هویتی، قرارداد نهایی، بیمه و گواهی‌های رسمی عمداً به صورت «بارگذاری نشده» نگه داشته شده‌اند.
"""


def employment_md(employee: dict) -> str:
    return doc_header(employee, "خلاصه استخدام و حکم داخلی نمونه") + f"""## مشخصات حکم

| فیلد | مقدار |
|---|---|
| شماره پرسنلی | {employee['employee_id']} |
| نام | {employee['full_name']} |
| دپارتمان | {employee['department']} |
| سمت | {employee['role']} |
| تاریخ شروع همکاری | {employee['hire_date']} |
| نوع همکاری | تمام‌وقت |
| وضعیت همکاری | فعال — نمونه |
| سرپرست مستقیم | {employee['supervisor']} |
| محل خدمت | دفتر مرکزی بابک AI — دادهٔ نمونه |

### متن داخلی غیرالزام‌آور

همکاری نمونهٔ {employee['full_name']} از تاریخ **{employee['hire_date']}** در سمت **{employee['role']}** و در دپارتمان **{employee['department']}** ثبت شده است. هر قرارداد واقعی باید پس از بررسی HR، امضای طرفین و ثبت در سامانهٔ امن شرکت نگهداری شود.

> این متن قرارداد کار یا حکم استخدامی رسمی نیست.
"""


def education_md(employee: dict) -> str:
    return doc_header(employee, "سوابق تحصیلی نمونه") + f"""## سوابق ثبت‌شده

{md_table(employee['education'])}

> نام مؤسسه‌ها در این دادهٔ نمایشی عمومی و غیرواقعی است. اصل مدارک باید جداگانه و فقط در مخزن خصوصی HR بارگذاری و اعتبارسنجی شود.
"""


def compensation_md(employee: dict) -> str:
    return doc_header(employee, "خلاصه جبران خدمات نمونه") + f"""## اطلاعات حقوقی

| فیلد | مقدار |
|---|---|
| نام | {employee['full_name']} |
| شماره پرسنلی | {employee['employee_id']} |
| سمت | {employee['role']} |
| پایه حقوق ماهانه | {employee['base_salary_display']} تومان |
| دوره پرداخت | ماهانه |
| وضعیت مزایا | نیازمند تکمیل در HR خصوصی |
| کسورات قانونی | محاسبه نشده — دادهٔ نمونه |

این صفحه فقط پایه حقوق نمونه را نشان می‌دهد و جایگزین فیش حقوقی، قرارداد یا محاسبهٔ قانونی بیمه و مالیات نیست.
"""


def family_md(employee: dict) -> str:
    family = employee["family_info"]
    return doc_header(employee, "فرم وضعیت خانوادگی نمونه") + f"""## وضعیت ثبت‌شده

| فیلد | مقدار |
|---|---|
| نام | {employee['full_name']} |
| وضعیت تأهل | {family['marital_status']} |
| نام همسر | {family['spouse_name']} |
| تعداد فرزندان | {family['children_count']} |

اطلاعات تکمیلی افراد تحت تکفل، در صورت نیاز، باید فقط در مخزن HR خصوصی و با دسترسی محدود نگهداری شود.
"""


def checklist_md(employee: dict) -> str:
    return doc_header(employee, "چک‌لیست مدارک پرونده") + f"""## مدارک ایجادشده برای نمونه‌سازی

| مدرک | مسیر / وضعیت | توضیح |
|---|---|---|
| تصویر پروفایل | [photo.svg](../photo.svg) — آماده | آواتار برداری ساختگی، نه عکس شخص واقعی |
| فرم اطلاعات پرسنلی | [profile.md](../profile.md) — آماده | داده‌های ساختگی برای تست |
| خلاصه استخدام | [employment-record.md](employment-record.md) — آماده | پیش‌نویس داخلی غیرالزام‌آور |
| سوابق تحصیلی | [education-record.md](education-record.md) — آماده | رکورد نمایشی، بدون اصل مدرک |
| جبران خدمات | [compensation-record.md](compensation-record.md) — آماده | پایه حقوق نمونه به تومان |
| وضعیت خانوادگی | [family-record.md](family-record.md) — آماده | دادهٔ نمونه |
| کارت ملی / شناسنامه | بارگذاری نشده | برای جلوگیری از ساخت مدرک جعلی و افشای PII |
| اصل مدارک تحصیلی | بارگذاری نشده | نیازمند دریافت و اعتبارسنجی واقعی |
| قرارداد نهایی امضاشده | بارگذاری نشده | این پوشه قرارداد قانونی تولید نمی‌کند |
| مدارک بیمه و مالیات | بارگذاری نشده | باید در سامانهٔ امن HR ثبت شود |

> **قانون نگهداری:** هیچ کد ملی واقعی، تصویر واقعی یا مدرک رسمی را در رپوی عمومی GitHub قرار ندهید.
"""


def profile_html(employee: dict) -> str:
    e = employee
    education_rows = "".join(
        f"<tr><td>{html.escape(r['level'])}</td><td>{html.escape(r['field'])}</td><td>{html.escape(r['institution'])}</td><td>{html.escape(r['start_date'])}</td><td>{html.escape(r['issue_date'])}</td><td>{html.escape(r['status'])}</td></tr>"
        for r in e["education"]
    )
    family = e["family_info"]
    return f'''<!doctype html>
<html lang="fa" dir="rtl">
<head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{html.escape(e['full_name'])} | پرونده HR</title>
<style>
:root{{--bg:#070b16;--panel:#10182a;--line:#24324c;--text:#eaf2ff;--muted:#91a1bf;--cyan:#39e7d4;--purple:#a879ff;--pink:#ff6b9d}}
*{{box-sizing:border-box}} body{{margin:0;background:radial-gradient(circle at 10% 0%,#162443 0,#070b16 38%);color:var(--text);font-family:Tahoma,Arial,sans-serif;line-height:1.8}} a{{color:var(--cyan)}} .wrap{{max-width:1180px;margin:0 auto;padding:24px}} .top{{display:flex;justify-content:space-between;align-items:center;gap:18px;margin-bottom:20px}} .back{{border:1px solid var(--line);padding:8px 14px;border-radius:12px;text-decoration:none}} .badge{{color:var(--cyan);font-size:12px;letter-spacing:.08em}} .hero{{display:grid;grid-template-columns:160px 1fr;gap:24px;align-items:center;background:linear-gradient(135deg,#111d35,#0c1323);border:1px solid var(--line);border-radius:24px;padding:22px;box-shadow:0 0 40px #061426}} .avatar{{width:150px;height:150px;border-radius:22px;border:1px solid #35506c;background:#0b1425}} h1{{margin:3px 0 8px;font-size:30px}} h2{{font-size:18px;margin:0 0 14px;color:var(--cyan)}} .role{{font-size:18px;color:#d9d6ff}} .meta{{display:flex;flex-wrap:wrap;gap:9px;margin-top:14px}} .pill{{padding:5px 10px;border:1px solid #2d4263;border-radius:999px;color:var(--muted);font-size:13px}} .grid{{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:16px;margin-top:16px}} section{{background:rgba(16,24,42,.9);border:1px solid var(--line);border-radius:20px;padding:20px}} section.full{{grid-column:1/-1}} table{{width:100%;border-collapse:collapse;font-size:14px}} th,td{{padding:10px 8px;border-bottom:1px solid #21304a;text-align:right;vertical-align:top}} th{{color:var(--muted);font-weight:normal}} .value{{font-size:20px;color:#fff}} .salary{{color:var(--pink);font-weight:bold}} .links{{display:flex;flex-wrap:wrap;gap:10px}} .links a{{border:1px solid #2c4660;border-radius:12px;padding:7px 12px;text-decoration:none}} .notice{{margin-top:16px;color:#ffd98a;background:#312513;border:1px solid #665027;border-radius:14px;padding:12px 14px;font-size:13px}} @media(max-width:720px){{.hero{{grid-template-columns:1fr;text-align:center}}.avatar{{margin:auto}}.grid{{grid-template-columns:1fr}}.top{{align-items:flex-start;flex-direction:column}}}}
</style>
</head>
<body><main class="wrap">
<div class="top"><div><div class="badge">BABAK AI COMPANY · HR FILE</div><div style="color:var(--muted);font-size:13px">پرونده پرسنلی نمایشی</div></div><a class="back" href="../../index.html">بازگشت به فهرست</a></div>
<div class="hero"><img class="avatar" src="photo.svg" alt="تصویر نمونه {html.escape(e['full_name'])}"><div><h1>{html.escape(e['full_name'])}</h1><div class="role">{html.escape(e['role'])}</div><div class="meta"><span class="pill">{html.escape(e['employee_id'])}</span><span class="pill">{html.escape(e['department'])}</span><span class="pill">{html.escape(e['gender'])}</span><span class="pill">{e['age']} سال</span><span class="pill">{html.escape(e['age_bucket'])}</span></div></div></div>
<div class="grid">
<section><h2>اطلاعات شناسایی</h2><table><tr><th>تاریخ تولد</th><td>{e['birth_date_jalali']}</td></tr><tr><th>نام پدر</th><td>{html.escape(e['father_name'])}</td></tr><tr><th>کد ملی نمایشی</th><td>{html.escape(e['national_code'])}</td></tr><tr><th>محل تولد</th><td>{html.escape(e['birth_place'])}</td></tr><tr><th>تابعیت</th><td>ایرانی</td></tr></table></section>
<section><h2>اطلاعات استخدام</h2><table><tr><th>تاریخ استخدام</th><td>{e['hire_date']}</td></tr><tr><th>سابقه تقریبی</th><td>{e['years_with_company']} سال</td></tr><tr><th>سرپرست مستقیم</th><td>{html.escape(e['supervisor'])}</td></tr><tr><th>ایمیل نمونه</th><td>{html.escape(e['work_email'])}</td></tr><tr><th>پایه حقوق</th><td class="salary">{e['base_salary_display']} تومان</td></tr></table></section>
<section class="full"><h2>سوابق تحصیلی</h2><table><thead><tr><th>مقطع</th><th>رشته</th><th>مؤسسه</th><th>شروع</th><th>اخذ</th><th>وضعیت</th></tr></thead><tbody>{education_rows}</tbody></table></section>
<section><h2>وضعیت خانوادگی</h2><table><tr><th>وضعیت تأهل</th><td>{family['marital_status']}</td></tr><tr><th>نام همسر</th><td>{html.escape(family['spouse_name'])}</td></tr><tr><th>تعداد فرزندان</th><td>{family['children_count']}</td></tr></table></section>
<section><h2>اسناد پرونده</h2><div class="links"><a href="profile.md">پرونده متنی</a><a href="profile.json">JSON</a><a href="documents/employment-record.md">استخدام</a><a href="documents/education-record.md">تحصیلات</a><a href="documents/compensation-record.md">حقوق</a><a href="documents/family-record.md">خانواده</a><a href="documents/document-checklist.md">چک‌لیست</a></div></section>
</div><div class="notice">این رکورد، تصویر و کد ملی کاملاً ساختگی و غیرقابل استفاده رسمی هستند. دادهٔ واقعی HR باید در مخزن خصوصی و دسترسی‌محدود نگهداری شود.</div>
</main></body></html>'''


def build_employees() -> list[dict]:
    roles = []
    for dept in DEPARTMENTS:
        for title, level in dept["roles"]:
            roles.append({"department": dept["name"], "agency_team": dept["agency_team"], "field": dept["field"], "role": title, "level": level})
    assert len(roles) == 72, len(roles)
    assert len(FEMALE_GIVEN) == 58, len(FEMALE_GIVEN)
    assert len(MALE_GIVEN) == 14, len(MALE_GIVEN)
    assert len(MALE_POSITIONS) == 14
    employees = []
    female_i = male_i = 0
    senior_i = young_i = mid_i = 0
    # First pass creates the records.
    for index, role in enumerate(roles):
        number = index + 1
        gender = "مرد" if index in MALE_POSITIONS else "زن"
        if gender == "زن":
            first = FEMALE_GIVEN[female_i]
            female_i += 1
        else:
            first = MALE_GIVEN[male_i]
            male_i += 1
        family_name = FAMILY_NAMES[index]
        full_name = f"{first} {family_name}"
        if index in AGE_31_PLUS_POSITIONS:
            age = SENIOR_AGES[senior_i]
            senior_i += 1
        elif young_i < len(YOUNG_AGES):
            age = YOUNG_AGES[young_i]
            young_i += 1
        else:
            age = MID_AGES[mid_i]
            mid_i += 1
        birth, birth_jalali, birth_jyear = age_birth_date(age, index)
        assert is_age_exact(birth, age), (number, birth, age)
        employee_id = f"BAC-{number:04d}"
        education = education_records(birth_jyear, age, role["field"], number, index in DOCTORATE_POSITIONS)
        family = family_info(age, number, gender)
        record = {
            "employee_id": employee_id,
            "full_name": full_name,
            "first_name": first,
            "family": family_name,
            "gender": gender,
            "age": age,
            "age_bucket": "۲۰ تا ۲۴ سال" if age < 25 else ("۲۵ تا ۳۰ سال" if age <= 30 else "۳۱ سال به بالا"),
            "birth_date_gregorian": birth.isoformat(),
            "birth_date_jalali": birth_jalali,
            "father_name": FATHER_NAMES[index % len(FATHER_NAMES)],
            "national_code": f"IR-DEMO-{number:06d}",
            "birth_place": BIRTH_CITIES[index % len(BIRTH_CITIES)],
            "department": role["department"],
            "agency_team": role["agency_team"],
            "role": role["role"],
            "level": role["level"],
            "hire_date": hire_date(birth_jyear, age, number),
            "base_salary_toman": salary_for(role["role"], role["level"], number),
            "education": education,
            "family_info": family,
            "work_email": f"employee{number:03d}@babak-ai.company",
            "extension": f"1{number:03d}",
            "status": "فعال — نمونه",
            "employment_type": "تمام‌وقت",
            "synthetic_demo": True,
            "avatar_file": "photo.svg",
            "doctorate": index in DOCTORATE_POSITIONS,
        }
        record["base_salary_display"] = f"{record['base_salary_toman']:,}".translate(str.maketrans("0123456789", "۰۱۲۳۴۵۶۷۸۹"))
        record["years_with_company"] = max(0, 1405 - int(record["hire_date"].split("/")[0]))
        employees.append(record)
    # Second pass attaches the department head as a supervisor.
    heads = {}
    for employee in employees:
        if employee["level"] in {"executive", "director"} and employee["department"] not in heads:
            heads[employee["department"]] = employee["full_name"]
    for employee in employees:
        employee["supervisor"] = "هیئت‌مدیره — دادهٔ نمونه" if employee["level"] == "executive" else heads.get(employee["department"], "مدیر واحد — نمونه")
    assert len(employees) == 72
    assert sum(e["gender"] == "زن" for e in employees) == 58
    assert sum(e["gender"] == "مرد" for e in employees) == 14
    assert sum(e["age"] < 25 for e in employees) == 14
    assert sum(25 <= e["age"] <= 30 for e in employees) == 36
    assert sum(e["age"] > 30 for e in employees) == 22
    assert sum(e["doctorate"] for e in employees) == 4
    return employees


def write_files(employees: list[dict]) -> None:
    if EMPLOYEES_DIR.exists():
        shutil.rmtree(EMPLOYEES_DIR)
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    for employee in employees:
        folder = EMPLOYEES_DIR / employee["employee_id"]
        docs = folder / "documents"
        docs.mkdir(parents=True, exist_ok=True)
        (folder / "photo.svg").write_text(avatar_svg(employee, int(employee["employee_id"].split("-")[-1])), encoding="utf-8")
        (folder / "profile.md").write_text(profile_md(employee), encoding="utf-8")
        (folder / "profile.json").write_text(json.dumps(employee, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        (folder / "index.html").write_text(profile_html(employee), encoding="utf-8")
        (docs / "employment-record.md").write_text(employment_md(employee), encoding="utf-8")
        (docs / "education-record.md").write_text(education_md(employee), encoding="utf-8")
        (docs / "compensation-record.md").write_text(compensation_md(employee), encoding="utf-8")
        (docs / "family-record.md").write_text(family_md(employee), encoding="utf-8")
        (docs / "document-checklist.md").write_text(checklist_md(employee), encoding="utf-8")

    # Machine-readable company list for the dashboard and future Supabase import.
    (DATA_DIR / "employees.json").write_text(json.dumps({
        "company": "کمپانی هوش مصنوعی بابک",
        "generated_at": CURRENT_JALALI,
        "synthetic_demo": True,
        "privacy_note": "تمام رکوردها ساختگی هستند؛ national_codeها معتبر نیستند.",
        "counts": {
            "total": len(employees),
            "female": sum(e["gender"] == "زن" for e in employees),
            "male": sum(e["gender"] == "مرد" for e in employees),
            "age_20_24": sum(e["age"] < 25 for e in employees),
            "age_25_30": sum(25 <= e["age"] <= 30 for e in employees),
            "age_31_plus": sum(e["age"] > 30 for e in employees),
            "doctorates": sum(e["doctorate"] for e in employees),
        },
        "employees": employees,
    }, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    fieldnames = [
        "employee_id", "full_name", "gender", "age", "age_bucket", "birth_date_jalali", "father_name",
        "national_code", "birth_place", "department", "agency_team", "role", "hire_date",
        "base_salary_toman", "marital_status", "spouse_name", "children_count", "work_email", "extension",
        "supervisor", "synthetic_demo",
    ]
    with (DATA_DIR / "employees.csv").open("w", newline="", encoding="utf-8-sig") as fh:
        writer = csv.DictWriter(fh, fieldnames=fieldnames)
        writer.writeheader()
        for e in employees:
            row = {key: e.get(key, "") for key in fieldnames}
            row["marital_status"] = e["family_info"]["marital_status"]
            row["spouse_name"] = e["family_info"]["spouse_name"]
            row["children_count"] = e["family_info"]["children_count"]
            writer.writerow(row)


def main() -> None:
    employees = build_employees()
    write_files(employees)
    print(json.dumps({
        "total": len(employees),
        "female": sum(e["gender"] == "زن" for e in employees),
        "male": sum(e["gender"] == "مرد" for e in employees),
        "age_20_24": sum(e["age"] < 25 for e in employees),
        "age_25_30": sum(25 <= e["age"] <= 30 for e in employees),
        "age_31_plus": sum(e["age"] > 30 for e in employees),
        "doctorates": sum(e["doctorate"] for e in employees),
    }, ensure_ascii=False))


if __name__ == "__main__":
    main()
