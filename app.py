import streamlit as st
import sqlite3
import hashlib
import json
import datetime
import urllib.request
import urllib.error
import os
import base64
import io
import warnings
import uuid
from html import escape
from PIL import Image, ImageOps, UnidentifiedImageError

# ---------------------------------------------------------
# إعدادات المنصة الأساسية
# ---------------------------------------------------------
st.set_page_config(
    page_title="بوابة مكافحة العدوى | Infection Control Portal",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---------------------------------------------------------
# التصميم المؤسسي الفاخر (Enterprise Healthcare UI & Animations)
# ---------------------------------------------------------
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Tajawal:wght@400;500;700;800;900&display=swap');
    
    html, body, [class*="css"], .stMarkdown, .stText, .stButton, .stTextInput, .stTextArea, .stSelectbox, .stNumberInput {
        font-family: 'Tajawal', sans-serif !important;
        direction: rtl;
        text-align: right;
    }
    
    /* إخفاء قوائم Streamlit الافتراضية لمظهر مؤسسي خالص */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* خلفية طبية راقية بلمسة هندسية ناعمة */
    .stApp {
        background-color: #f4f7fb;
        background-image: 
            radial-gradient(at 10% 10%, rgba(14, 165, 233, 0.07) 0px, transparent 50%),
            radial-gradient(at 90% 80%, rgba(13, 148, 136, 0.07) 0px, transparent 50%);
    }
    
    /* حركات انسيابية (Animations) */
    @keyframes fadeInUp {
        from { opacity: 0; transform: translateY(15px); }
        to { opacity: 1; transform: translateY(0); }
    }
    @keyframes pulseGlow {
        0% { box-shadow: 0 0 0 0 rgba(16, 185, 129, 0.4); }
        70% { box-shadow: 0 0 0 10px rgba(16, 185, 129, 0); }
        100% { box-shadow: 0 0 0 0 rgba(16, 185, 129, 0); }
    }
    @keyframes floatSlow {
        0%, 100% { transform: translateY(0px); }
        50% { transform: translateY(-6px); }
    }

    /* الشريط الجانبي الاحترافي */
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #091326 0%, #0f2942 60%, #0a3641 100%) !important;
        border-left: 1px solid rgba(255, 255, 255, 0.08);
        box-shadow: -8px 0 30px rgba(9, 19, 38, 0.12);
    }
    section[data-testid="stSidebar"] * {
        color: #f8fafc !important;
    }

    /* تاريخ واضح بدلاً من النص الأبيض فوق خلفية فاتحة */
    .portal-date {
        background: #f0fdfa;
        border: 1px solid #99f6e4;
        border-radius: 14px;
        padding: 14px 16px;
        margin-bottom: 12px;
    }
    .portal-date .date-label,
    section[data-testid="stSidebar"] .portal-date .date-label {
        color: #115e59 !important;
        font-size: 13px;
        font-weight: 700;
    }
    .portal-date .date-value,
    section[data-testid="stSidebar"] .portal-date .date-value {
        color: #0f172a !important;
        -webkit-text-fill-color: #0f172a !important;
        font-size: 21px;
        font-weight: 800;
        margin-top: 4px;
        direction: ltr;
        text-align: right;
        font-variant-numeric: tabular-nums;
    }
    [data-testid="stDateInput"] input {
        color: #0f172a !important;
        -webkit-text-fill-color: #0f172a !important;
        background-color: #ffffff !important;
        direction: ltr;
        font-weight: 700;
        color-scheme: light;
    }
    section[data-testid="stSidebar"] [data-testid="stFileUploaderDropzone"],
    section[data-testid="stSidebar"] [data-testid="stFileUploaderDropzone"] * {
        color: #0f172a !important;
    }
    section[data-testid="stSidebar"] [data-testid="stFileUploaderDropzone"] {
        background: #f8fafc !important;
        border: 1px dashed #94a3b8;
        border-radius: 14px;
    }
    section[data-testid="stSidebar"] [data-testid="stFileUploaderDropzone"] button {
        color: #0f172a !important;
        background: #ffffff !important;
    }
    section[data-testid="stSidebar"] [data-testid="stAlertContainer"] * {
        color: #0f172a !important;
    }
    
    /* بطاقة البروفايل في القائمة الجانبية */
    .sidebar-profile {
        background: rgba(255, 255, 255, 0.06);
        backdrop-filter: blur(12px);
        border: 1px solid rgba(255, 255, 255, 0.12);
        border-radius: 20px;
        padding: 22px 16px;
        text-align: center;
        margin-bottom: 18px;
        animation: fadeInUp 0.5s ease-out;
    }
    .sidebar-avatar {
        width: 82px;
        height: 82px;
        border-radius: 50%;
        margin: 0 auto 12px auto;
        padding: 4px;
        background: linear-gradient(135deg, #10b981, #0ea5e9);
        box-shadow: 0 8px 20px rgba(14, 165, 233, 0.3);
    }
    .sidebar-avatar img {
        width: 100%;
        height: 100%;
        border-radius: 50%;
        object-fit: cover;
        border: 2px solid #091326;
    }

    /* هوية بصرية أصلية لمكافحة العدوى */
    .exec-banner {
        position: relative;
        border-radius: 24px;
        overflow: hidden;
        margin-bottom: 28px;
        background: radial-gradient(ellipse at 8% 50%, rgba(45, 212, 191, 0.20), transparent 52%),
                    linear-gradient(115deg, #071e2b 0%, #084c50 55%, #0f766e 100%);
        padding: 36px 40px;
        color: white;
        box-shadow: 0 18px 40px rgba(9, 19, 38, 0.16);
        border: 1px solid rgba(255, 255, 255, 0.18);
        animation: fadeInUp 0.6s ease-out;
    }
    .exec-banner::before {
        content: "";
        position: absolute;
        inset: 0;
        opacity: 0.12;
        background-image: radial-gradient(#99f6e4 1px, transparent 1px);
        background-size: 24px 24px;
        pointer-events: none;
    }
    .banner-content { position: relative; z-index: 1; }
    .ic-banner-art {
        position: absolute;
        left: 1%;
        top: 50%;
        transform: translateY(-50%);
        width: min(42%, 360px);
        opacity: 0.24;
        pointer-events: none;
    }
    .ic-banner-art svg { display: block; width: 100%; height: auto; }
    .brand-line {
        color: #ccfbf1;
        font-size: 14px;
        font-weight: 800;
        margin-bottom: 14px;
        letter-spacing: 0.2px;
    }
    .brand-line span { color: #5eead4; padding: 0 10px; }
    .exec-banner h1 {
        color: #ffffff !important;
        font-weight: 900 !important;
        font-size: 31px !important;
        margin: 8px 0 10px 0 !important;
        letter-spacing: -0.3px;
    }
    .exec-banner p {
        color: #e2e8f0 !important;
        font-size: 16px !important;
        margin: 0 !important;
        max-width: 720px;
        line-height: 1.6;
    }
    .live-indicator {
        display: inline-flex;
        align-items: center;
        gap: 8px;
        background: rgba(16, 185, 129, 0.2);
        border: 1px solid rgba(16, 185, 129, 0.5);
        color: #ecfdf5;
        padding: 5px 15px;
        border-radius: 999px;
        font-size: 13px;
        font-weight: 700;
        backdrop-filter: blur(6px);
    }
    .live-dot {
        width: 9px;
        height: 9px;
        background-color: #10b981;
        border-radius: 50%;
        display: inline-block;
        animation: pulseGlow 2s infinite;
    }

    /* بوابة تسجيل الدخول الاحترافية */
    .login-wrapper {
        background: #ffffff;
        border-radius: 26px;
        overflow: hidden;
        box-shadow: 0 25px 60px rgba(15, 23, 42, 0.11);
        border: 1px solid #e2e8f0;
        margin-top: 10px;
        animation: fadeInUp 0.7s ease-out;
    }
    .login-visual-header {
        background: radial-gradient(circle at 15% 30%, rgba(45, 212, 191, 0.22), transparent 55%),
                    linear-gradient(135deg, #071e2b 0%, #0f766e 100%);
        padding: 42px 30px;
        text-align: center;
        color: white;
        position: relative;
    }
    .login-visual-header h2 {
        color: #ffffff !important;
        font-weight: 900 !important;
        font-size: 27px !important;
        margin: 12px 0 6px 0 !important;
    }
    .login-visual-header p {
        color: #ccfbf1 !important;
        font-size: 15px !important;
        margin: 0 !important;
    }

    /* بطاقات المؤشرات التفاعلية */
    .kpi-card {
        background: #ffffff;
        border-radius: 20px;
        padding: 24px 22px;
        border: 1px solid #e2e8f0;
        box-shadow: 0 8px 24px rgba(15, 23, 42, 0.04);
        position: relative;
        overflow: hidden;
        transition: all 0.3s cubic-bezier(0.16, 1, 0.3, 1);
        animation: fadeInUp 0.6s ease-out;
        margin-bottom: 16px;
    }
    .kpi-card:hover {
        transform: translateY(-6px);
        box-shadow: 0 18px 35px rgba(2, 132, 199, 0.11);
        border-color: #bae6fd;
    }
    .kpi-accent {
        position: absolute;
        top: 0;
        right: 0;
        width: 7px;
        height: 100%;
    }
    .kpi-icon-box {
        width: 50px;
        height: 50px;
        border-radius: 14px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 23px;
        float: left;
    }
    .kpi-title {
        color: #64748b;
        font-size: 14px;
        font-weight: 700;
        margin-bottom: 6px;
    }
    .kpi-value {
        color: #0f172a;
        font-size: 32px;
        font-weight: 900;
        line-height: 1.1;
        margin-bottom: 8px;
    }
    .kpi-sub {
        font-size: 12px;
        font-weight: 700;
        padding: 3px 10px;
        border-radius: 99px;
        display: inline-block;
    }

    /* بطاقات الفريق المصورة */
    .member-card {
        background: #ffffff;
        border-radius: 20px;
        padding: 22px;
        border: 1px solid #e2e8f0;
        box-shadow: 0 6px 20px rgba(15, 23, 42, 0.035);
        margin-bottom: 18px;
        transition: all 0.3s ease;
        position: relative;
        overflow: hidden;
    }
    .member-card:hover {
        transform: translateY(-4px);
        box-shadow: 0 14px 30px rgba(15, 23, 42, 0.09);
        border-color: #99f6e4;
    }
    .member-photo {
        width: 64px;
        height: 64px;
        border-radius: 16px;
        object-fit: cover;
        margin-left: 16px;
        border: 2px solid #e2e8f0;
        box-shadow: 0 4px 12px rgba(0,0,0,0.08);
    }
    
    /* شارات الحالة */
    .status-pill-done {
        background: #ecfdf5;
        color: #047857;
        border: 1px solid #a7f3d0;
        padding: 5px 14px;
        border-radius: 99px;
        font-weight: 800;
        font-size: 12.5px;
        display: inline-flex;
        align-items: center;
        gap: 5px;
    }
    .status-pill-wait {
        background: #fffbeb;
        color: #b45309;
        border: 1px solid #fde68a;
        padding: 5px 14px;
        border-radius: 99px;
        font-weight: 800;
        font-size: 12.5px;
        display: inline-flex;
        align-items: center;
        gap: 5px;
    }

    /* بطاقات الأقسام المصورة في الصفحة الرئيسية */
    .unit-gallery-card {
        border-radius: 18px;
        overflow: hidden;
        position: relative;
        height: 150px;
        box-shadow: 0 8px 20px rgba(15, 23, 42, 0.08);
        margin-bottom: 16px;
        transition: all 0.35s ease;
        border: 1px solid rgba(255,255,255,0.2);
    }
    .unit-gallery-card:hover {
        transform: scale(1.02);
        box-shadow: 0 14px 28px rgba(15, 23, 42, 0.16);
    }
    .unit-overlay {
        position: absolute;
        inset: 0;
        background: linear-gradient(0deg, rgba(9, 19, 38, 0.9) 0%, rgba(9, 19, 38, 0.25) 100%);
        display: flex;
        flex-direction: column;
        justify-content: flex-end;
        padding: 16px;
        color: white;
    }
    .unit-overlay h5 {
        color: #ffffff !important;
        margin: 0 !important;
        font-size: 16px !important;
        font-weight: 800 !important;
    }
    .unit-overlay span {
        color: #99f6e4 !important;
        font-size: 12px !important;
        font-weight: 600;
    }

    /* الأزرار والتبويبات */
    .stButton>button {
        background: linear-gradient(135deg, #0f766e 0%, #0284c7 100%) !important;
        color: white !important;
        font-family: 'Tajawal', sans-serif !important;
        font-weight: 800 !important;
        font-size: 16px !important;
        border-radius: 14px !important;
        border: none !important;
        padding: 11px 26px !important;
        box-shadow: 0 8px 20px rgba(2, 132, 199, 0.22) !important;
        transition: all 0.25s ease !important;
    }
    .stButton>button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 12px 26px rgba(2, 132, 199, 0.34) !important;
    }
    button[data-baseweb="tab"] {
        font-family: 'Tajawal', sans-serif !important;
        font-weight: 800 !important;
        font-size: 15.5px !important;
        padding: 12px 22px !important;
    }
    @media (max-width: 640px) {
        .exec-banner { padding: 24px 20px; }
        .exec-banner h1 { font-size: 25px !important; }
        .member-card > div { flex-wrap: wrap; gap: 12px; }
        .ic-banner-art { width: 65%; opacity: 0.12; }
        .brand-line { font-size: 12px; }
    }
</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# قاعدة البيانات وتجهيز الحسابات والصلاحيات المزدوجة للدكتور الوليد
# ---------------------------------------------------------
DB_FILE = "infection_control_enterprise.db"

DEFAULT_REPORT_QUESTIONS = [
    {"id": "accomplishments", "label": "أبرز الإنجازات والأعمال المنفذة خلال الأسبوع",
     "placeholder": "سجّل الأعمال المنجزة والجولات الميدانية والمتابعات والبرامج التدريبية...", "required": True, "active": True},
    {"id": "challenges", "label": "التحديات، المعوقات، أو الملاحظات الحرجة المرصودة",
     "placeholder": "اذكر الملاحظات أو المعوقات التي تتطلب المتابعة...", "required": False, "active": True},
    {"id": "next_week_plan", "label": "خطة العمل والأولويات للأسبوع القادم",
     "placeholder": "ما أبرز المهام والأقسام المستهدفة في الأسبوع القادم؟", "required": False, "active": True},
]

# رسم أصلي داخل الملف؛ لا يعتمد على صور مستشفيات أو شعارات خارجية.
INFECTION_CONTROL_ART = '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 400 400" fill="none" aria-hidden="true">
<circle cx="200" cy="200" r="176" stroke="#5eead4" stroke-width="1" stroke-dasharray="5 10"/>
<circle cx="200" cy="200" r="145" stroke="#99f6e4" stroke-width="1"/>
<path d="M200 87 285 123V195C285 250 246 289 200 315 154 289 115 250 115 195V123Z" fill="#14b8a6" fill-opacity=".2" stroke="#99f6e4" stroke-width="6"/>
<path d="m157 195 29 29 59-63" stroke="#ecfdf5" stroke-width="13" stroke-linecap="round" stroke-linejoin="round"/>
<g stroke="#5eead4" stroke-width="3"><path d="M53 200h57M290 200h57M200 25v52M200 323v52M76 76l40 40M284 284l40 40M76 324l40-40M284 116l40-40"/>
<circle cx="53" cy="200" r="14" fill="#084c50"/><circle cx="347" cy="200" r="14" fill="#084c50"/>
<circle cx="200" cy="31" r="12" fill="#084c50"/><circle cx="200" cy="369" r="12" fill="#084c50"/>
<circle cx="76" cy="76" r="9" fill="#99f6e4"/><circle cx="324" cy="324" r="9" fill="#99f6e4"/>
<circle cx="76" cy="324" r="9" fill="#99f6e4"/><circle cx="324" cy="76" r="9" fill="#99f6e4"/></g></svg>'''

def hash_password(password: str) -> str:
    salt = "ic_salt_2026_mac"
    return hashlib.sha256((password + salt).encode('utf-8')).hexdigest()

def get_db_connection():
    conn = sqlite3.connect(DB_FILE, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn

# قائمة الأعضاء الستة (د. الوليد الرقيبة يمتلك صلاحية head_employee أي رئيس قسم + عضو يرفع تقارير)
TEAM_MEMBERS_SEED = [
    (
        'A', '1234', 'د. الوليد الرقيبة', 'head_employee',
        'رئيس قسم مكافحة العدوى | الإشراف العام وترصد الميكروبات',
        '#0f766e',
        'https://images.unsplash.com/photo-1622253692010-333f2da6031d?auto=format&fit=crop&w=400&q=80'
    ),
    (
        'Abdullrahman', '1234', 'د. عبدالرحمن', 'employee',
        'وحدة ترصد العدوى المكتسبة (HAI Surveillance)',
        '#0284c7',
        'https://images.unsplash.com/photo-1537368910025-700350fe46c7?auto=format&fit=crop&w=400&q=80'
    ),
    (
        'Ahmed', '1234', 'د. أحمد إمام', 'employee',
        'وحدة التدقيق والجولات الميدانية (IC Audits)',
        '#2563eb',
        'https://images.unsplash.com/photo-1612349317150-e413f6a5b16d?auto=format&fit=crop&w=400&q=80'
    ),
    (
        'Shekah', '1234', 'أ. شيخه البريدي', 'employee',
        'وحدة نظافة الأيدي والتدريب (Hand Hygiene & Training)',
        '#7c3aed',
        'https://images.unsplash.com/photo-1594824476967-48c8b964273f?auto=format&fit=crop&w=400&q=80'
    ),
    (
        'Suliman', '1234', 'أ. سليمان الجارالله', 'employee',
        'وحدة التعقيم المركزي وصحة البيئة (CSSD & Env. Health)',
        '#d97706',
        'https://images.unsplash.com/photo-1582750433449-648ed127bb54?auto=format&fit=crop&w=400&q=80'
    ),
    (
        'Abdullah', '1234', 'د. عبدالله', 'employee',
        'عيادة صحة العاملين والتطعيمات (Occupational Health)',
        '#059669',
        'https://images.unsplash.com/photo-1559839734-2b71ea197ec2?auto=format&fit=crop&w=400&q=80'
    ),
]

def init_db():
    conn = get_db_connection()
    conn.execute("BEGIN IMMEDIATE")
    c = conn.cursor()
    
    c.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password_hash TEXT NOT NULL,
        full_name TEXT NOT NULL,
        role TEXT NOT NULL,
        section TEXT NOT NULL,
        badge_color TEXT DEFAULT '#0f766e',
        photo_url TEXT DEFAULT ''
    )
    """)
    
    c.execute("""
    CREATE TABLE IF NOT EXISTS weekly_reports (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        week_num INTEGER NOT NULL,
        year INTEGER NOT NULL,
        date_submitted TEXT NOT NULL,
        accomplishments TEXT NOT NULL,
        challenges TEXT NOT NULL,
        next_week_plan TEXT NOT NULL,
        audits_count INTEGER DEFAULT 0,
        compliance_rate REAL DEFAULT NULL,
        critical_alerts TEXT DEFAULT '',
        FOREIGN KEY (user_id) REFERENCES users (id)
    )
    """)

    # ترقية إضافية فقط؛ لا تُحذف الحسابات أو التقارير أو نسب الإصدار السابق.
    existing_columns = {row['name'] for row in c.execute("PRAGMA table_info(weekly_reports)")}
    for column, definition in {
        "form_snapshot": "TEXT NOT NULL DEFAULT ''",
        "answers_json": "TEXT NOT NULL DEFAULT '{}'",
        "compliance_checks_total": "INTEGER DEFAULT NULL",
        "compliance_checks_passed": "INTEGER DEFAULT NULL",
        "compliance_evidence": "TEXT NOT NULL DEFAULT ''",
        "compliance_reviewed_at": "TEXT DEFAULT NULL",
        "compliance_reviewed_by": "INTEGER DEFAULT NULL",
    }.items():
        if column not in existing_columns:
            c.execute(f"ALTER TABLE weekly_reports ADD COLUMN {column} {definition}")
    c.execute("""
        CREATE TABLE IF NOT EXISTS portal_settings (
            setting_key TEXT PRIMARY KEY,
            value TEXT NOT NULL,
            revision INTEGER NOT NULL DEFAULT 1,
            updated_at TEXT,
            updated_by INTEGER
        )
    """)
    c.execute("INSERT OR IGNORE INTO portal_settings (setting_key, value) VALUES (?, ?)",
              ("report_questions", json.dumps(DEFAULT_REPORT_QUESTIONS, ensure_ascii=False)))
    
    c.execute("SELECT COUNT(*) FROM users")
    if c.fetchone()[0] == 0:
        # حساب إداري إضافي للطوارئ
        c.execute("""
        INSERT INTO users (username, password_hash, full_name, role, section, badge_color, photo_url)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            'admin', hash_password('1234'), 'د. الوليد الرقيبة (إدارة النظام)', 'head_employee',
            'رئيس قسم مكافحة العدوى', '#0f172a',
            'https://images.unsplash.com/photo-1622253692010-333f2da6031d?auto=format&fit=crop&w=400&q=80'
        ))
        
        for username, pwd, name, role, sec, color, photo in TEAM_MEMBERS_SEED:
            c.execute("""
            INSERT INTO users (username, password_hash, full_name, role, section, badge_color, photo_url)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (username, hash_password(pwd), name, role, sec, color, photo))
            
    conn.commit()
    conn.close()

init_db()

# ---------------------------------------------------------
# التاريخ المحلي وصور الأعضاء (تُحفظ الصورة داخل قاعدة البيانات الحالية)
# ---------------------------------------------------------
PORTAL_TIMEZONE = datetime.timezone(datetime.timedelta(hours=3))
MAX_PHOTO_BYTES = 5 * 1024 * 1024
MAX_PHOTO_PIXELS = 20_000_000
DEFAULT_PHOTO = TEAM_MEMBERS_SEED[0][-1]

def portal_now():
    return datetime.datetime.now(PORTAL_TIMEZONE)

def reporting_period_text(week_num, year):
    try:
        start = datetime.date.fromisocalendar(int(year), int(week_num), 1)
    except (TypeError, ValueError):
        # بعض السجلات القديمة قد تتضمن أسبوع 53 في سنة لا تحتويه.
        return f"الأسبوع {week_num} / {year}"
    end = start + datetime.timedelta(days=6)
    return f"{start:%d/%m/%Y} — {end:%d/%m/%Y}"

def prepare_profile_photo(raw_bytes):
    """التحقق من محتوى الصورة، تصحيح اتجاهها، وضغطها دون بياناتها الوصفية."""
    if not raw_bytes or len(raw_bytes) > MAX_PHOTO_BYTES:
        raise ValueError("اختر صورة لا يتجاوز حجمها 5 ميجابايت.")
    try:
        with warnings.catch_warnings():
            warnings.simplefilter("error", Image.DecompressionBombWarning)
            with Image.open(io.BytesIO(raw_bytes)) as source:
                if source.format not in {"JPEG", "PNG", "WEBP"}:
                    raise ValueError("الصيغ المدعومة: JPG وPNG وWEBP فقط.")
                if source.width * source.height > MAX_PHOTO_PIXELS:
                    raise ValueError("أبعاد الصورة كبيرة جداً. اختر نسخة أصغر من 20 ميجابكسل.")
                source.verify()
            with Image.open(io.BytesIO(raw_bytes)) as source:
                image = ImageOps.exif_transpose(source).convert("RGBA")
                image.thumbnail((512, 512), Image.Resampling.LANCZOS)
                background = Image.new("RGB", image.size, "white")
                background.paste(image, mask=image.getchannel("A"))
                output = io.BytesIO()
                background.save(output, format="JPEG", quality=88, optimize=True)
        return "data:image/jpeg;base64," + base64.b64encode(output.getvalue()).decode("ascii")
    except (UnidentifiedImageError, OSError, SyntaxError,
            Image.DecompressionBombError, Image.DecompressionBombWarning) as exc:
        raise ValueError("تعذر قراءة الصورة. اختر صورة سليمة بصيغة JPG أو PNG أو WEBP.") from exc

def save_my_profile_photo(photo_url):
    """تحديث صورة صاحب الجلسة فقط دون تغيير بيانات الحساب أو التقارير."""
    if not st.session_state.get("authenticated") or not st.session_state.get("user"):
        raise PermissionError("يرجى تسجيل الدخول أولاً.")
    user_id = st.session_state.user['id']
    conn = get_db_connection()
    try:
        with conn:
            result = conn.execute("UPDATE users SET photo_url = ? WHERE id = ?", (photo_url, user_id))
            if result.rowcount != 1:
                raise ValueError("لم يتم العثور على الحساب.")
    finally:
        conn.close()
    st.session_state.user['photo_url'] = photo_url

def render_profile_photo_settings(current_user):
    message = st.session_state.pop("profile_photo_message", None)
    revision = st.session_state.get("profile_photo_revision", 0)
    with st.expander("🖼️ تغيير صورتي", expanded=bool(message)):
        if message:
            st.success(message)
        st.caption("اختر صورة من جهازك بصيغة JPG أو PNG أو WEBP، بحد أقصى 5 ميجابايت.")
        uploaded = st.file_uploader(
            "الصورة الشخصية الجديدة",
            type=["jpg", "jpeg", "png", "webp"],
            key=f"profile_photo_{current_user['id']}_{revision}"
        )
        prepared = None
        if uploaded is not None:
            try:
                if uploaded.size > MAX_PHOTO_BYTES:
                    raise ValueError("حجم الصورة أكبر من 5 ميجابايت. اختر صورة أصغر.")
                prepared = prepare_profile_photo(uploaded.getvalue())
                preview = base64.b64decode(prepared.split(",", 1)[1])
                st.image(preview, caption="معاينة الصورة قبل الحفظ", width=140)
            except ValueError as exc:
                st.error(str(exc))
        if st.button("💾 حفظ صورتي", key="save_my_photo", disabled=prepared is None, use_container_width=True):
            try:
                save_my_profile_photo(prepared)
            except (sqlite3.Error, ValueError):
                st.error("تعذر حفظ الصورة الآن. يرجى المحاولة مرة أخرى.")
            else:
                st.session_state.profile_photo_revision = revision + 1
                st.session_state.profile_photo_message = "تم تحديث صورتك بنجاح ✅"
                st.rerun()
        if (current_user.get('photo_url') or '').startswith("data:image/"):
            if st.button("↩️ استعادة الصورة الافتراضية", key="reset_my_photo", use_container_width=True):
                default_photo = next(
                    (member[-1] for member in TEAM_MEMBERS_SEED if member[0].lower() == current_user['username'].lower()),
                    DEFAULT_PHOTO
                )
                try:
                    save_my_profile_photo(default_photo)
                except (sqlite3.Error, ValueError):
                    st.error("تعذر استعادة الصورة الآن. يرجى المحاولة مرة أخرى.")
                else:
                    st.session_state.profile_photo_revision = revision + 1
                    st.session_state.profile_photo_message = "تمت استعادة الصورة الافتراضية ✅"
                    st.rerun()

# ---------------------------------------------------------
# إعدادات الأسئلة، حفظ الإجابات، واحتساب المؤشرات من بيانات الرصد
# ---------------------------------------------------------
def require_admin(conn):
    if not st.session_state.get('authenticated') or not st.session_state.get('user'):
        raise PermissionError("يرجى تسجيل الدخول أولاً.")
    user_id = st.session_state.user['id']
    row = conn.execute("SELECT role FROM users WHERE id = ?", (user_id,)).fetchone()
    if row is None or row['role'] not in {'admin', 'head_employee'}:
        raise PermissionError("تعديل هذه الإعدادات متاح لرئيس القسم فقط.")
    return user_id

def load_question_settings():
    conn = get_db_connection()
    try:
        row = conn.execute("SELECT value, revision FROM portal_settings WHERE setting_key = 'report_questions'").fetchone()
        return json.loads(row['value']), row['revision']
    finally:
        conn.close()

def save_question_settings(questions, expected_revision):
    if not 1 <= len(questions) <= 25:
        raise ValueError("يمكن أن يحتوي النموذج على سؤال واحد إلى 25 سؤالاً.")
    if not any(q['active'] for q in questions):
        raise ValueError("يجب إبقاء سؤال واحد على الأقل ظاهراً للأعضاء.")
    ids = set()
    for q in questions:
        if not q['label'].strip() or len(q['label']) > 200:
            raise ValueError("أدخل عنواناً لكل سؤال لا يتجاوز 200 حرف.")
        if q['id'] in ids or not q['id'].replace('_', '').isalnum():
            raise ValueError("معرّفات الأسئلة غير صالحة أو مكررة.")
        ids.add(q['id'])
    conn = get_db_connection()
    try:
        with conn:
            admin_id = require_admin(conn)
            result = conn.execute("""
                UPDATE portal_settings SET value = ?, revision = revision + 1, updated_at = ?, updated_by = ?
                WHERE setting_key = 'report_questions' AND revision = ?
            """, (json.dumps(questions, ensure_ascii=False), portal_now().isoformat(), admin_id, expected_revision))
            if result.rowcount != 1:
                raise ValueError("تغيّرت إعدادات النموذج من جلسة أخرى. حدّث الصفحة ثم أعد التعديل.")
    finally:
        conn.close()

def report_answers_and_questions(report):
    report = dict(report)
    answers = {q['id']: report.get(q['id']) or '' for q in DEFAULT_REPORT_QUESTIONS}
    try:
        stored = json.loads(report.get('answers_json') or '{}')
        if isinstance(stored, dict):
            answers.update({k: v for k, v in stored.items() if isinstance(v, str)})
    except (ValueError, TypeError):
        pass
    try:
        questions = json.loads(report.get('form_snapshot') or 'null')
        if not isinstance(questions, list) or not questions:
            questions = DEFAULT_REPORT_QUESTIONS
    except (ValueError, TypeError):
        questions = DEFAULT_REPORT_QUESTIONS
    return answers, questions

def render_saved_answers(report):
    answers, questions = report_answers_and_questions(report)
    for index, q in enumerate(questions, 1):
        st.markdown(f"**{index}. {q['label']}**")
        st.write(answers.get(q['id'], '').strip() or 'لم تُسجّل إجابة لهذه الخانة.')

def save_weekly_report(questions, new_answers, audits_count):
    if not st.session_state.get('authenticated') or not st.session_state.get('user'):
        raise PermissionError("يرجى تسجيل الدخول أولاً.")
    active_questions = [q for q in questions if q['active']]
    for q in active_questions:
        if q['required'] and not new_answers.get(q['id'], '').strip():
            raise ValueError(f"يرجى الإجابة عن السؤال المطلوب: {q['label']}")
    if not isinstance(audits_count, int) or not 0 <= audits_count <= 250:
        raise ValueError("عدد الجولات غير صالح.")
    year, week, _ = portal_now().date().isocalendar()
    user_id = st.session_state.user['id']
    conn = get_db_connection()
    try:
        # منع إنشاء تقريرين لنفس العضو والفترة عند الإرسال من جلستين متزامنتين.
        conn.execute("BEGIN IMMEDIATE")
        with conn:
            old = conn.execute("""SELECT * FROM weekly_reports WHERE user_id = ? AND week_num = ? AND year = ?
                                  ORDER BY date_submitted DESC, id DESC LIMIT 1""", (user_id, week, year)).fetchone()
            answers, old_questions = report_answers_and_questions(old) if old else ({}, [])
            answers.update({q['id']: new_answers.get(q['id'], '').strip() for q in active_questions})
            active_ids = {q['id'] for q in active_questions}
            snapshot = active_questions + [q for q in old_questions if q['id'] not in active_ids and answers.get(q['id'], '').strip()]
            values = (answers.get('accomplishments', ''), answers.get('challenges', ''), answers.get('next_week_plan', ''),
                      audits_count, portal_now().strftime('%Y-%m-%d %H:%M'),
                      json.dumps(snapshot, ensure_ascii=False), json.dumps(answers, ensure_ascii=False))
            if old:
                conn.execute("""UPDATE weekly_reports SET accomplishments = ?, challenges = ?, next_week_plan = ?,
                                audits_count = ?, date_submitted = ?, form_snapshot = ?, answers_json = ? WHERE id = ?""",
                             (*values, old['id']))
            else:
                conn.execute("""INSERT INTO weekly_reports (accomplishments, challenges, next_week_plan, audits_count,
                                date_submitted, form_snapshot, answers_json, user_id, week_num, year, compliance_rate)
                                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, NULL)""", (*values, user_id, week, year))
    finally:
        conn.close()

def load_team_members():
    conn = get_db_connection()
    try:
        return [dict(row) for row in conn.execute("SELECT * FROM users WHERE LOWER(username) != 'admin' ORDER BY id")]
    finally:
        conn.close()

def load_period_reports(week, year):
    conn = get_db_connection()
    try:
        return [dict(row) for row in conn.execute("""
            SELECT r.*, u.full_name, u.section, u.username, u.badge_color, u.photo_url
            FROM weekly_reports r JOIN users u ON r.user_id = u.id
            WHERE r.week_num = ? AND r.year = ? AND LOWER(u.username) != 'admin'
              AND r.id = (SELECT newer.id FROM weekly_reports newer
                          WHERE newer.user_id = r.user_id AND newer.week_num = r.week_num AND newer.year = r.year
                          ORDER BY newer.date_submitted DESC, newer.id DESC LIMIT 1)
            ORDER BY u.id
        """, (week, year))]
    finally:
        conn.close()

def has_verified_measurement(report):
    total = report.get('compliance_checks_total')
    passed = report.get('compliance_checks_passed')
    return (isinstance(total, int) and isinstance(passed, int) and total > 0 and 0 <= passed <= total
            and bool(report.get('compliance_reviewed_at')) and report.get('compliance_reviewed_by') is not None
            and bool((report.get('compliance_evidence') or '').strip()))

def compliance_metrics(reports):
    verified = [r for r in reports if has_verified_measurement(r)]
    total = sum(r['compliance_checks_total'] for r in verified)
    passed = sum(r['compliance_checks_passed'] for r in verified)
    return {'total': total, 'passed': passed, 'reports_measured': len(verified),
            'rate': (100 * passed / total) if total else None}

def save_compliance_measurement(report_id, total, passed, evidence):
    if not isinstance(total, int) or not isinstance(passed, int) or total <= 0 or not 0 <= passed <= total:
        raise ValueError("أدخل إجمالي فرص رصد أكبر من صفر، وعدداً مطابقاً لا يتجاوز الإجمالي.")
    if not evidence.strip():
        raise ValueError("أدخل مرجع بيانات الرصد حتى يكون القياس موثقاً.")
    conn = get_db_connection()
    try:
        with conn:
            admin_id = require_admin(conn)
            result = conn.execute("""UPDATE weekly_reports SET compliance_checks_total = ?, compliance_checks_passed = ?,
                compliance_evidence = ?, compliance_reviewed_at = ?, compliance_reviewed_by = ?, compliance_rate = ? WHERE id = ?""",
                (total, passed, evidence.strip(), portal_now().isoformat(timespec='minutes'), admin_id, 100 * passed / total, report_id))
            if result.rowcount != 1:
                raise ValueError("لم يتم العثور على التقرير.")
    finally:
        conn.close()

def clear_compliance_measurement(report_id):
    conn = get_db_connection()
    try:
        with conn:
            require_admin(conn)
            conn.execute("""UPDATE weekly_reports SET compliance_checks_total = NULL, compliance_checks_passed = NULL,
                compliance_evidence = '', compliance_reviewed_at = NULL, compliance_reviewed_by = NULL,
                compliance_rate = NULL WHERE id = ?""", (report_id,))
    finally:
        conn.close()

def render_question_settings():
    st.subheader("🛠️ إعدادات أسئلة التقرير الأسبوعي")
    st.caption("عدّل عنوان السؤال والنص المساعد، وحدّد هل الإجابة مطلوبة وهل يظهر السؤال للأعضاء. تحتفظ التقارير المحفوظة بنص أسئلتها وإجاباتها.")
    questions, revision = load_question_settings()
    with st.form('weekly_questions_settings'):
        edited = []
        for index, q in enumerate(questions, 1):
            st.markdown(f"**السؤال {index}**")
            label = st.text_input('عنوان السؤال', value=q['label'], max_chars=200, key=f"question_label_{q['id']}_{revision}")
            placeholder = st.text_input('النص المساعد داخل الخانة', value=q.get('placeholder', ''), max_chars=600, key=f"question_help_{q['id']}_{revision}")
            c1, c2 = st.columns(2)
            with c1:
                active = st.checkbox('يظهر للأعضاء', value=q['active'], key=f"question_active_{q['id']}_{revision}")
            with c2:
                required = st.checkbox('الإجابة مطلوبة', value=q['required'], key=f"question_required_{q['id']}_{revision}")
            edited.append({'id': q['id'], 'label': label.strip(), 'placeholder': placeholder.strip(), 'active': active, 'required': required})
            st.divider()
        if st.form_submit_button('💾 حفظ إعدادات الأسئلة', use_container_width=True):
            try:
                save_question_settings(edited, revision)
            except (ValueError, PermissionError) as exc:
                st.error(str(exc))
            else:
                st.session_state.portal_notice = 'تم تحديث أسئلة التقرير للأعضاء بنجاح ✅'
                st.rerun()
    if len(questions) < 25:
        with st.expander('➕ إضافة سؤال جديد'):
            with st.form(f'add_report_question_{revision}', clear_on_submit=True):
                label = st.text_input('عنوان السؤال الجديد', max_chars=200)
                placeholder = st.text_input('النص المساعد للسؤال الجديد', max_chars=600)
                required = st.checkbox('إجابة السؤال الجديد مطلوبة')
                if st.form_submit_button('➕ إضافة السؤال'):
                    new_question = {'id': 'custom_' + uuid.uuid4().hex, 'label': label.strip(), 'placeholder': placeholder.strip(), 'required': required, 'active': True}
                    try:
                        save_question_settings(questions + [new_question], revision)
                    except (ValueError, PermissionError) as exc:
                        st.error(str(exc))
                    else:
                        st.session_state.portal_notice = 'تمت إضافة السؤال الجديد ✅'
                        st.rerun()

# ---------------------------------------------------------
# التقرير التنفيذي: نفس البيانات والحساب المستخدمين في لوحة القيادة
# ---------------------------------------------------------
def build_executive_summary(reports_list, week_num, year):
    total_reports = len(reports_list)
    if total_reports == 0:
        return "لا توجد تقارير مرفوعة لهذا الأسبوع حتى الآن."
    total_members = len(load_team_members())
    total_audits = sum(r['audits_count'] for r in reports_list)
    measurement = compliance_metrics(reports_list)
    rate_text = f"{measurement['rate']:.1f}%" if measurement['rate'] is not None else 'لا توجد بيانات رصد موثقة'
    completion_text = f"{100 * total_reports / total_members:.0f}%" if total_members else 'لا يوجد أعضاء'
    sections_summary = []
    for r in reports_list:
        answers, questions = report_answers_and_questions(r)
        details = '\n'.join(f"- **{q['label']}:** {answers.get(q['id'], '').strip() or 'لم تُسجّل إجابة.'}" for q in questions)
        personal_rate = (f"{100 * r['compliance_checks_passed'] / r['compliance_checks_total']:.1f}% "
                         f"({r['compliance_checks_passed']} / {r['compliance_checks_total']})"
                         if has_verified_measurement(r) else 'لا توجد بيانات رصد موثقة')
        sections_summary.append(f"### {r['full_name']} — {r['section']}\n"
                                f"الجولات: {r['audits_count']} | الالتزام المرصود: {personal_rate}\n\n{details}")
    return f"""### 🏥 التقرير التنفيذي الموحد لقسم مكافحة العدوى — الفترة {reporting_period_text(week_num, year)}
**تجمع القصيم الصحي | شركة الصحة القابضة**
**ملخص مجمّع من التقارير المحفوظة — للمراجعة والاعتماد من رئيس القسم**

---

#### 📊 أولاً: المؤشرات القياسية العامة للقسم (Department KPIs)
- **اكتمال التقارير الأسبوعية:** `{total_reports}` من أصل `{total_members}` أعضاء ({completion_text})
- **إجمالي الجولات الميدانية والتدقيقات:** `{total_audits}` جولة تفقدية
- **نسبة الالتزام في فرص الرصد الموثقة:** {rate_text}
- **فرص الرصد المطابقة / الإجمالي:** `{measurement['passed']} / {measurement['total']}`
- **تغطية القياس:** `{measurement['reports_measured']}` من أصل `{total_reports}` تقارير مستلمة

---

#### 📋 ثانياً: إجابات الأعضاء حسب أسئلة كل تقرير
{chr(10).join(sections_summary)}

---

#### 📐 منهجية المؤشر
نسبة الالتزام = مجموع فرص الرصد المطابقة ÷ مجموع فرص الرصد القابلة للتقييم × 100.
تُستبعد النسب الافتراضية القديمة والتقارير التي لا تحتوي على أعداد رصد موثقة.
المؤشر يصف العينات المدخلة فقط؛ لا يُعد قياساً شاملاً لجميع الممارسات أو نسبة للعدوى المكتسبة.
"""

# ---------------------------------------------------------
# إدارة الجلسة وتسجيل الدخول الآمن
# ---------------------------------------------------------
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False
if 'user' not in st.session_state:
    st.session_state.user = None

def login(username, password):
    conn = get_db_connection()
    c = conn.cursor()
    pwd_hash = hash_password(password.strip())
    c.execute("SELECT * FROM users WHERE LOWER(username) = LOWER(?)", (username.strip(),))
    user = c.fetchone()
    conn.close()
    if user:
        if user['password_hash'] == pwd_hash:
            st.session_state.authenticated = True
            st.session_state.user = dict(user)
            return True
    return False

def logout():
    st.session_state.clear()
    st.rerun()

# ---------------------------------------------------------
# دالة عرض واجهة الموظف (نموذج التقرير الأسبوعي بدون مؤشر نسبة الالتزام)
# ---------------------------------------------------------
def render_employee_portal(target_user):
    today = portal_now().date()
    current_year, current_week, _ = today.isocalendar()
    questions, question_revision = load_question_settings()
    
    # معرض مصور لأقسام مكافحة العدوى يضفي فخامة بصرية للمنصة
    g1, g2, g3 = st.columns(3)
    with g1:
        st.markdown("""
        <div class="unit-gallery-card" style="background: url('https://images.unsplash.com/photo-1584515979956-d9f6e5d09982?auto=format&fit=crop&w=700&q=80') center/cover;">
            <div class="unit-overlay">
                <span>الرصد الوقائي</span>
                <h5>الترصد الوبائي والجولات الميدانية</h5>
            </div>
        </div>
        """, unsafe_allow_html=True)
    with g2:
        st.markdown("""
        <div class="unit-gallery-card" style="background: url('https://images.unsplash.com/photo-1579684385127-1ef15d508118?auto=format&fit=crop&w=700&q=80') center/cover;">
            <div class="unit-overlay">
                <span>الجودة والسلامة</span>
                <h5>كفاءة التعقيم المركزي وسلامة البيئة</h5>
            </div>
        </div>
        """, unsafe_allow_html=True)
    with g3:
        st.markdown("""
        <div class="unit-gallery-card" style="background: url('https://images.unsplash.com/photo-1576091160550-2173dba999ef?auto=format&fit=crop&w=700&q=80') center/cover;">
            <div class="unit-overlay">
                <span>التعليم الطبي المستمر</span>
                <h5>الممارسات الوقائية وصحة العاملين</h5>
            </div>
        </div>
        """, unsafe_allow_html=True)

    tab_submit, tab_history = st.tabs(["📝 رفع التقرير الأسبوعي", "📂 أرشيف تقاريري السابقة"])
    
    with tab_submit:
        conn = get_db_connection()
        c = conn.cursor()
        c.execute("SELECT * FROM weekly_reports WHERE user_id = ? AND week_num = ? AND year = ? ORDER BY date_submitted DESC, id DESC LIMIT 1",
                  (target_user['id'], current_week, current_year))
        existing_report = c.fetchone()
        conn.close()
        
        if existing_report:
            st.success(f"✅ تم استلام تقريرك للفترة {reporting_period_text(current_week, current_year)} بتاريخ {existing_report['date_submitted']}. يمكنك تعديل وتحديث التقرير:")
            
        saved_answers, _ = report_answers_and_questions(existing_report) if existing_report else ({}, [])
        with st.form(f"emp_report_form_{target_user['id']}_{current_year}_{current_week}_{question_revision}"):
            st.markdown("#### 📅 الفترة الزمنية والنشاط الميداني")
            # تُحسب الفترة تلقائياً؛ لا حاجة لإدخال رقم الأسبوع أو السنة يدوياً.
            c_w1, c_w2 = st.columns(2)
            with c_w1:
                st.markdown(f"""
                <div class="portal-date">
                    <div class="date-label">📅 تاريخ التقرير</div>
                    <div class="date-value">{today:%d/%m/%Y}</div>
                </div>
                """, unsafe_allow_html=True)
                st.caption(f"الفترة الأسبوعية: {reporting_period_text(current_week, current_year)} — تُحدد تلقائياً.")
            with c_w2:
                audits_count = st.number_input(
                    "🔍 عدد الجولات الميدانية / التدقيقات المنفذة",
                    min_value=0, max_value=250,
                    value=existing_report['audits_count'] if existing_report else 0
                )
                
            st.markdown("#### 📋 تفاصيل التقرير الأسبوعي")
            new_answers = {}
            for index, q in enumerate((q for q in questions if q['active']), 1):
                required_hint = ' *' if q['required'] else ''
                new_answers[q['id']] = st.text_area(
                    f"{index}. {q['label']}{required_hint}",
                    value=saved_answers.get(q['id'], ''), placeholder=q.get('placeholder', ''),
                    height=135 if index == 1 else 110,
                    key=f"answer_{target_user['id']}_{current_year}_{current_week}_{q['id']}_{question_revision}"
                )
            st.caption('* إجابة مطلوبة')
            
            save_report_btn = st.form_submit_button("🚀 اعتماد ورفع التقرير الأسبوعي", use_container_width=True)
            if save_report_btn:
                try:
                    save_weekly_report(questions, new_answers, audits_count)
                except (ValueError, PermissionError) as exc:
                    st.error(str(exc))
                else:
                    st.balloons()
                    st.success("🎉 تم رفع واعتماد تقريرك الأسبوعي بنجاح!")
                    st.rerun()

    with tab_history:
        st.subheader("📚 أرشيف تقاريرك الأسبوعية السابقة")
        conn = get_db_connection()
        c = conn.cursor()
        c.execute("SELECT * FROM weekly_reports WHERE user_id = ? ORDER BY year DESC, week_num DESC", (target_user['id'],))
        my_reports = c.fetchall()
        conn.close()
        
        if not my_reports:
            st.info("لا توجد تقارير سابقة مسجلة في أرشيفك حتى الآن.")
        else:
            for rep in my_reports:
                with st.expander(f"📅 تقرير الفترة {reporting_period_text(rep['week_num'], rep['year'])} — تاريخ الرفع: {rep['date_submitted']}"):
                    st.markdown(f"**🔍 عدد الجولات الميدانية المنفذة:** `{rep['audits_count']}` جولات")
                    render_saved_answers(rep)

# ---------------------------------------------------------
# دالة عرض لوحة تحكم رئيس القسم / الأدمن (مع تقييم نسبة الالتزام خاص بالأدمن فقط)
# ---------------------------------------------------------
def render_admin_portal():
    today = portal_now().date()
    current_year, current_week, _ = today.isocalendar()
    
    if st.session_state.get('portal_notice'):
        st.success(st.session_state.pop('portal_notice'))
    tab_dash, tab_details, tab_ai, tab_team, tab_questions = st.tabs([
        "📊 لوحة القيادة والمؤشرات",
        "📑 تقارير الأعضاء وتقييم الالتزام",
        "📋 التقرير التنفيذي الموحد",
        "⚙️ إدارة أعضاء القسم",
        "🛠️ إعدادات أسئلة التقرير"
    ])
    
    with tab_dash:
        employees = load_team_members()
        submitted_reports = load_period_reports(current_week, current_year)
        
        submitted_user_ids = {r['user_id'] for r in submitted_reports}
        total_emp = len(employees)
        done_count = len(submitted_reports)
        pending_count = total_emp - done_count
        total_aud = sum(r['audits_count'] for r in submitted_reports)
        measurement = compliance_metrics(submitted_reports)
        compliance_text = f"{measurement['rate']:.1f}%" if measurement['rate'] is not None else 'لا توجد بيانات'
        
        # البطاقات القياسية الأربع
        k1, k2, k3, k4 = st.columns(4)
        with k1:
            st.markdown(f"""
            <div class="kpi-card">
                <div class="kpi-accent" style="background: #10b981;"></div>
                <div class="kpi-icon-box" style="background: #ecfdf5; color: #059669;">✅</div>
                <div class="kpi-title">التقارير المكتملة</div>
                <div class="kpi-value"><bdi dir="ltr">{done_count} / {total_emp}</bdi></div>
                <span class="kpi-sub" style="background: #ecfdf5; color: #047857;">نسبة التسليم {(done_count/total_emp*100) if total_emp else 0:.0f}%</span>
            </div>
            """, unsafe_allow_html=True)
        with k2:
            st.markdown(f"""
            <div class="kpi-card">
                <div class="kpi-accent" style="background: #f59e0b;"></div>
                <div class="kpi-icon-box" style="background: #fffbeb; color: #d97706;">⏳</div>
                <div class="kpi-title">بانتظار الرفع</div>
                <div class="kpi-value">{pending_count}</div>
                <span class="kpi-sub" style="background: #fffbeb; color: #b45309;">أعضاء قيد الإعداد</span>
            </div>
            """, unsafe_allow_html=True)
        with k3:
            st.markdown(f"""
            <div class="kpi-card">
                <div class="kpi-accent" style="background: #0ea5e9;"></div>
                <div class="kpi-icon-box" style="background: #f0f9ff; color: #0284c7;">🔍</div>
                <div class="kpi-title">إجمالي الجولات الميدانية</div>
                <div class="kpi-value">{total_aud}</div>
                <span class="kpi-sub" style="background: #f0f9ff; color: #0369a1;">جولة تدقيق هذا الأسبوع</span>
            </div>
            """, unsafe_allow_html=True)
        with k4:
            st.markdown(f"""
            <div class="kpi-card">
                <div class="kpi-accent" style="background: #8b5cf6;"></div>
                <div class="kpi-icon-box" style="background: #f5f3ff; color: #6d28d9;">📈</div>
                <div class="kpi-title">الالتزام في فرص الرصد الموثقة</div>
                <div class="kpi-value" style="font-size: {'32px' if measurement['rate'] is not None else '23px'};">{compliance_text}</div>
                <span class="kpi-sub" style="background: #f5f3ff; color: #5b21b6;">تم قياس {measurement['reports_measured']} من {done_count} تقارير</span>
            </div>
            """, unsafe_allow_html=True)
            
        st.caption(f"طريقة الحساب: فرص الرصد المطابقة ÷ إجمالي الفرص القابلة للتقييم × 100. الفرص المطابقة: {measurement['passed']} | الإجمالي: {measurement['total']}. التقارير غير المقاسة لا تدخل في النسبة.")
        st.markdown(f"### 👨‍⚕️ متابعة حالة تسليم أعضاء قسم مكافحة العدوى ({total_emp})")
        
        col_g1, col_g2 = st.columns(2)
        for idx, emp in enumerate(employees):
            is_done = emp['id'] in submitted_user_ids
            rep_obj = next((r for r in submitted_reports if r['user_id'] == emp['id']), None)
            status_badge = '<span class="status-pill-done">● تم التسليم</span>' if is_done else '<span class="status-pill-wait">● بانتظار الرفع</span>'
            sub_info = f"تاريخ الإرسال: {rep_obj['date_submitted']} | الجولات: {rep_obj['audits_count']}" if rep_obj else "لم يتم إرسال تقرير الأسبوع الحالي بعد"
            photo = emp.get('photo_url') or 'https://images.unsplash.com/photo-1622253692010-333f2da6031d?auto=format&fit=crop&w=400&q=80'
            
            card_html = f"""
            <div class="member-card">
                <div style="display: flex; align-items: center; justify-content: space-between;">
                    <div style="display: flex; align-items: center;">
                        <img src="{escape(photo, quote=True)}" class="member-photo" alt="الصورة الشخصية"/>
                        <div>
                            <h4 style="margin: 0; font-size: 18px; font-weight: 800; color: #0f172a;">{escape(emp['full_name'])}</h4>
                            <p style="margin: 3px 0; font-size: 13px; color: #0f766e; font-weight: 700;">{escape(emp['section'])}</p>
                            <span style="font-size: 12px; color: #64748b;">{sub_info}</span>
                        </div>
                    </div>
                    <div>{status_badge}</div>
                </div>
            </div>
            """
            if idx % 2 == 0:
                with col_g1:
                    st.markdown(card_html, unsafe_allow_html=True)
            else:
                with col_g2:
                    st.markdown(card_html, unsafe_allow_html=True)

    # 2. استعراض التقارير وإدخال أعداد رصد موثقة، دون نسبة افتراضية أو تقديرية.
    with tab_details:
        st.subheader("📑 مراجعة التقارير وتوثيق بيانات الالتزام")
        st.caption("أدخل عدد فرص الرصد المطابقة وإجمالي الفرص القابلة للتقييم من نموذج التدقيق الفعلي. تُحسب النسبة تلقائياً، وتُجمع الفرص لحساب مؤشر القسم.")
        
        selected_date = st.date_input(
            "📅 اختر تاريخاً ضمن الفترة المراد عرض تقاريرها",
            value=today, min_value=datetime.date(2024, 1, 1), max_value=today,
            format="DD/MM/YYYY", key="adm_details_date"
        )
        sel_year, sel_week, _ = selected_date.isocalendar()
        st.caption(f"الفترة المعروضة: {reporting_period_text(sel_week, sel_year)}")
            
        filtered_reports = load_period_reports(sel_week, sel_year)
        
        if not filtered_reports:
            st.info(f"لا توجد تقارير مرفوعة للفترة {reporting_period_text(sel_week, sel_year)} حتى الآن.")
        else:
            for r in filtered_reports:
                with st.expander(f"📄 {r['full_name']} — {r['section']} (تاريخ الرفع: {r['date_submitted']})", expanded=True):
                    c_info1, c_info2 = st.columns([1, 2])
                    with c_info1:
                        st.info(f"🔍 **عدد الجولات الميدانية المنفذة:** `{r['audits_count']}` جولات")
                    with c_info2:
                        if has_verified_measurement(r):
                            st.success(f"الالتزام المرصود: {100 * r['compliance_checks_passed'] / r['compliance_checks_total']:.1f}% — {r['compliance_checks_passed']} من {r['compliance_checks_total']} فرصة")
                            st.caption(f"آخر توثيق: {r['compliance_reviewed_at']} | المرجع: {r['compliance_evidence']}")
                        else:
                            st.info('لم تُدخل بيانات رصد موثقة لهذا التقرير. لا تدخل النسب الافتراضية السابقة في المؤشر.')
                        with st.form(f"admin_comp_form_{r['id']}"):
                            total = st.number_input(
                                'إجمالي فرص الرصد القابلة للتقييم', min_value=0,
                                value=int(r.get('compliance_checks_total') or 0), step=1, key=f"checks_total_{r['id']}"
                            )
                            passed = st.number_input(
                                'فرص الرصد المطابقة للمعايير', min_value=0,
                                value=int(r.get('compliance_checks_passed') or 0), step=1, key=f"checks_passed_{r['id']}"
                            )
                            evidence = st.text_input('مرجع بيانات الرصد', value=r.get('compliance_evidence') or '',
                                placeholder='مثال: نموذج تدقيق نظافة الأيدي بتاريخ 02/11/2026', max_chars=500, key=f"checks_source_{r['id']}")
                            if st.form_submit_button("💾 حفظ بيانات الرصد وحساب الالتزام"):
                                try:
                                    save_compliance_measurement(r['id'], total, passed, evidence)
                                except (ValueError, PermissionError) as exc:
                                    st.error(str(exc))
                                else:
                                    st.session_state.portal_notice = 'تم حفظ بيانات الرصد وتحديث المؤشر ✅'
                                    st.rerun()
                        if has_verified_measurement(r) and st.button('إلغاء بيانات القياس لهذا التقرير', key=f"clear_measurement_{r['id']}"):
                            clear_compliance_measurement(r['id'])
                            for field in ('checks_total', 'checks_passed', 'checks_source'):
                                st.session_state.pop(f"{field}_{r['id']}", None)
                            st.session_state.portal_notice = 'تم إلغاء القياس؛ التقرير محفوظ ولا يدخل في نسبة الالتزام حتى إدخال قياس جديد.'
                            st.rerun()
                    render_saved_answers(r)

    # 3. التقرير التنفيذي الموحد
    with tab_ai:
        st.subheader("📋 التقرير التنفيذي الموحد لقسم مكافحة العدوى")
        st.write("يجمع النظام تقارير الأعضاء وإجاباتهم، ويستخدم نفس بيانات الرصد والحساب المعروضين في لوحة القيادة.")
        
        summary_date = st.date_input(
            "📅 اختر تاريخاً ضمن الفترة المراد تلخيصها",
            value=today, min_value=datetime.date(2024, 1, 1), max_value=today,
            format="DD/MM/YYYY", key="adm_summary_date"
        )
        ai_year, ai_week, _ = summary_date.isocalendar()
        st.caption(f"فترة التقرير التنفيذي: {reporting_period_text(ai_week, ai_year)}")
            
        target_reports = load_period_reports(ai_week, ai_year)
        st.markdown(f"**التقارير المستلمة الجاهزة للدمج:** `{len(target_reports)}` من أصل `{len(load_team_members())}`")
        
        if st.button("✨ إصدار التقرير التنفيذي الموحد الآن", use_container_width=True):
            if not target_reports:
                st.warning("⚠️ لا توجد تقارير مرفوعة لهذا الأسبوع لإصدار الملخص.")
            else:
                summary_result = build_executive_summary(target_reports, ai_week, ai_year)
                st.success("✅ تم إعداد التقرير التنفيذي الموحد بنجاح!")
                st.markdown("---")
                st.markdown(summary_result)
                st.download_button(
                    label="📥 تحميل التقرير التنفيذي الموحد (ملف رسمي)",
                    data=summary_result,
                    file_name=f"Infection_Control_Executive_Report_W{ai_week}_{ai_year}.md",
                    mime="text/markdown",
                    use_container_width=True
                )

    # 4. إدارة أعضاء الفريق
    with tab_team:
        st.subheader("⚙️ إدارة حسابات وصلاحيات أعضاء قسم مكافحة العدوى")
        conn = get_db_connection()
        c = conn.cursor()
        c.execute("SELECT * FROM users WHERE username != 'admin' ORDER BY id ASC")
        current_employees = [dict(row) for row in c.fetchall()]
        conn.close()
        
        for emp in current_employees:
            with st.expander(f"👤 {emp['full_name']} — اسم المستخدم: ({emp['username']})"):
                with st.form(f"edit_emp_form_{emp['id']}"):
                    col_ed1, col_ed2 = st.columns(2)
                    with col_ed1:
                        new_name = st.text_input("الاسم الكامل", value=emp['full_name'])
                        new_user = st.text_input("اسم المستخدم (Username)", value=emp['username'])
                    with col_ed2:
                        new_sec = st.text_input("الوحدة / المسمى الوظيفي", value=emp['section'])
                        new_pass = st.text_input("تغيير الرقم السري", type="password", placeholder="اتركه فارغاً للإبقاء على الرقم السري الحالي")
                        
                    if st.form_submit_button("💾 حفظ التعديلات", use_container_width=True):
                        conn = get_db_connection()
                        c = conn.cursor()
                        if new_pass.strip():
                            c.execute("""
                            UPDATE users SET full_name = ?, section = ?, username = ?, password_hash = ? WHERE id = ?
                            """, (new_name.strip(), new_sec.strip(), new_user.strip(), hash_password(new_pass.strip()), emp['id']))
                        else:
                            c.execute("""
                            UPDATE users SET full_name = ?, section = ?, username = ? WHERE id = ?
                            """, (new_name.strip(), new_sec.strip(), new_user.strip(), emp['id']))
                        conn.commit()
                        conn.close()
                        st.success(f"✅ تم تحديث بيانات {new_name} بنجاح!")
                        st.rerun()

    with tab_questions:
        render_question_settings()

# ---------------------------------------------------------
# 1. شاشة تسجيل الدخول المحمية (بدون كشف أي حسابات أو أرقام سرية للزوار)
# ---------------------------------------------------------
if not st.session_state.authenticated:
    col_spacer1, col_center, col_spacer2 = st.columns([1, 2.2, 1])
    with col_center:
        st.markdown("""
        <div class="login-wrapper">
            <div class="login-visual-header">
                <div class="brand-line">تجمع القصيم الصحي <span>•</span> شركة الصحة القابضة</div>
                <div class="live-indicator" style="margin-bottom: 10px;">
                    <span class="live-dot"></span> بوابة إلكترونية آمنة ومشفرة
                </div>
                <h2>قسم مكافحة العدوى | Infection Control</h2>
                <p>المنصة الرقمية الموحدة لإدارة التقارير الأسبوعية والمؤشرات الوقائية</p>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        st.write("")
        with st.form("secure_login_form"):
            st.markdown("#### 🔐 تسجيل الدخول لمنسوبي القسم")
            username_input = st.text_input("👤 اسم المستخدم (Username)", placeholder="أدخل اسم المستخدم المعتمد")
            password_input = st.text_input("🔑 الرقم السري (Password)", type="password", placeholder="••••••••")
            submit_login = st.form_submit_button("دخول إلى المنصة", use_container_width=True)
            
            if submit_login:
                if login(username_input, password_input):
                    st.rerun()
                else:
                    st.error("⚠️ بيانات الدخول غير صحيحة. يرجى التأكد من اسم المستخدم والرقم السري أو التواصل مع رئيس القسم.")
                    
        st.markdown("""
        <div style="text-align: center; margin-top: 18px; color: #64748b; font-size: 13px;">
            🔒 جميع البيانات والتقارير محمية ومخصصة لمنسوبي قسم مكافحة العدوى فقط.
        </div>
        """, unsafe_allow_html=True)
    st.stop()

# ---------------------------------------------------------
# 2. الشاشة الداخلية بعد تسجيل الدخول
# ---------------------------------------------------------
# جلب أحدث صورة وبيانات للحساب عند كل تحديث للواجهة.
conn = get_db_connection()
try:
    user_row = conn.execute("SELECT * FROM users WHERE id = ?", (st.session_state.user['id'],)).fetchone()
finally:
    conn.close()
if user_row is None:
    logout()
st.session_state.user = dict(user_row)
current_user = st.session_state.user
today = portal_now().date()
current_year, current_week, _ = today.isocalendar()
is_head_or_admin = current_user['role'] in ['admin', 'head_employee']

# الشريط الجانبي
with st.sidebar:
    photo_src = current_user.get('photo_url') or 'https://images.unsplash.com/photo-1622253692010-333f2da6031d?auto=format&fit=crop&w=400&q=80'
    role_title = "👑 رئيس قسم مكافحة العدوى" if is_head_or_admin else "🛡️ أخصائي مكافحة عدوى"
    
    st.markdown(f"""
    <div class="sidebar-profile">
        <div class="sidebar-avatar">
            <img src="{escape(photo_src, quote=True)}" alt="الصورة الشخصية"/>
        </div>
        <h3 style="margin: 0; font-weight: 900; font-size: 20px;">{escape(current_user['full_name'])}</h3>
        <p style="margin: 4px 0 12px 0; font-size: 13px; opacity: 0.8;">{escape(current_user['section'])}</p>
        <span style="background: rgba(16, 185, 129, 0.22); border: 1px solid #10b981; padding: 5px 14px; border-radius: 99px; font-size: 12px; font-weight: 800;">
            {role_title}
        </span>
    </div>
    """, unsafe_allow_html=True)

    render_profile_photo_settings(current_user)
    
    # إذا كان المستخدم هو د. الوليد الرقيبة (رئيس القسم)، يظهر له مفتاح تبديل سريع + خيار جمع الواجهتين معاً
    selected_view_mode = "both"
    if is_head_or_admin:
        st.markdown("#### 🎛️ وضع العرض لرئيس القسم")
        view_choice = st.radio(
            "اختر طريقة استعراض المنصة:",
            [
                "✨ عرض شامل (لوحة الرئيس + نموذجي الشخصي)",
                "👑 لوحة قيادة رئيس القسم فقط",
                "📝 نموذج رفع التقرير الأسبوعي فقط"
            ],
            index=0
        )
        if "لوحة قيادة" in view_choice:
            selected_view_mode = "admin_only"
        elif "نموذج رفع" in view_choice:
            selected_view_mode = "emp_only"
        else:
            selected_view_mode = "both"
        st.divider()
        
    st.markdown(f"""
    <div class="portal-date">
        <div class="date-label">📅 التاريخ — بتوقيت السعودية</div>
        <div class="date-value">{today:%d/%m/%Y}</div>
    </div>
    """, unsafe_allow_html=True)
    st.divider()
    if st.button("🚪 تسجيل الخروج الآمن", use_container_width=True):
        logout()

# البانر البانورامي المصور
st.markdown(f"""
<div class="exec-banner">
    <div class="ic-banner-art">{INFECTION_CONTROL_ART}</div>
    <div class="banner-content">
    <div class="brand-line">تجمع القصيم الصحي <span>•</span> شركة الصحة القابضة</div>
    <div style="display: flex; align-items: center; justify-content: space-between; flex-wrap: wrap; gap: 20px;">
        <div>
            <div class="live-indicator">
                <span class="live-dot"></span> نظام الرصد والتقارير الأسبوعية — قسم مكافحة العدوى
            </div>
            <h1>مرحباً بك، {escape(current_user['full_name'])}</h1>
            <p>{escape(current_user['section'])} — بوابة رقمية متكاملة لمتابعة الأداء الوقائي، توثيق الجولات الميدانية، وتعزيز سلامة المرضى والعاملين.</p>
        </div>
        <div class="portal-date" style="text-align: center; margin-bottom: 0;">
            <div class="date-label">📅 الفترة التقريرية الحالية</div>
            <div class="date-value">{reporting_period_text(current_week, current_year)}</div>
        </div>
    </div>
    </div>
</div>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# عرض المحتوى حسب صلاحية المستخدم
# ---------------------------------------------------------
if is_head_or_admin:
    if selected_view_mode == "both":
        mode_tab1, mode_tab2 = st.tabs([
            "👑 لوحة قيادة رئيس القسم (متابعة الفريق، نسبة الالتزام، والتلخيص)",
            "📝 بوابتي الشخصية (رفع تقريري الأسبوعي كعضو في القسم)"
        ])
        with mode_tab1:
            render_admin_portal()
        with mode_tab2:
            render_employee_portal(current_user)
    elif selected_view_mode == "admin_only":
        render_admin_portal()
    else:
        render_employee_portal(current_user)
else:
    render_employee_portal(current_user)
