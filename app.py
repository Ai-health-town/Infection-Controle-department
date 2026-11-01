import streamlit as st
import sqlite3
import hashlib
import json
import datetime
import urllib.request
import urllib.error
import os

# ---------------------------------------------------------
# إعدادات الصفحة والتصميم العام الفاخر (RTL لدعم اللغة العربية)
# ---------------------------------------------------------
st.set_page_config(
    page_title="منصة مكافحة العدوى الذكية | Infection Control Portal",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# تصميم CSS احترافي وفاخر بألوان طبية حديثة وبطاقات ملونة
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;500;600;700;800;900&display=swap');
    
    html, body, [class*="css"], .stMarkdown, .stText, .stButton, .stTextInput, .stTextArea, .stSelectbox {
        font-family: 'Cairo', sans-serif !important;
        direction: rtl;
        text-align: right;
    }
    
    .stApp {
        background: linear-gradient(180deg, #f0f7ff 0%, #f8fafc 45%, #ffffff 100%);
    }
    
    /* تنسيق الشريط الجانبي الفاخر */
    section[data-testid="stSidebar"] {
        background: linear-gradient(165deg, #0f172a 0%, #1e293b 50%, #0f766e 100%);
        color: #ffffff !important;
        border-left: 1px solid rgba(255,255,255,0.1);
    }
    section[data-testid="stSidebar"] * {
        color: #f8fafc !important;
    }
    
    /* الهيدر الرئيسي البانورامي */
    .luxury-hero {
        background: linear-gradient(135deg, #0f172a 0%, #0f766e 55%, #0284c7 100%);
        color: white;
        padding: 32px 36px;
        border-radius: 22px;
        margin-bottom: 28px;
        box-shadow: 0 15px 35px rgba(2, 132, 199, 0.18);
        position: relative;
        overflow: hidden;
        border: 1px solid rgba(255, 255, 255, 0.15);
    }
    
    .luxury-hero::before {
        content: "";
        position: absolute;
        top: -50%;
        left: -20%;
        width: 450px;
        height: 450px;
        background: radial-gradient(circle, rgba(56, 189, 248, 0.22) 0%, transparent 70%);
        border-radius: 50%;
    }
    
    .luxury-hero h1 {
        color: #ffffff !important;
        font-weight: 900 !important;
        font-size: 30px !important;
        margin-bottom: 8px !important;
        letter-spacing: -0.3px;
    }
    
    .luxury-hero p {
        color: #e0f2fe !important;
        font-size: 16px !important;
        font-weight: 500;
        margin: 0 !important;
    }
    
    .hero-badge {
        background: rgba(255, 255, 255, 0.16);
        backdrop-filter: blur(8px);
        color: #ffffff;
        padding: 6px 16px;
        border-radius: 999px;
        font-size: 13px;
        font-weight: 700;
        display: inline-block;
        margin-bottom: 12px;
        border: 1px solid rgba(255, 255, 255, 0.25);
    }

    /* البطاقات الإحصائية الملونة الفخمة */
    .stat-card {
        padding: 24px 20px;
        border-radius: 18px;
        color: white;
        position: relative;
        overflow: hidden;
        box-shadow: 0 10px 25px rgba(15, 23, 42, 0.08);
        margin-bottom: 16px;
        transition: transform 0.25s ease, box-shadow 0.25s ease;
    }
    .stat-card:hover {
        transform: translateY(-4px);
        box-shadow: 0 15px 30px rgba(15, 23, 42, 0.14);
    }
    .stat-teal {
        background: linear-gradient(135deg, #0d9488 0%, #115e59 100%);
    }
    .stat-blue {
        background: linear-gradient(135deg, #0284c7 0%, #1e40af 100%);
    }
    .stat-purple {
        background: linear-gradient(135deg, #7c3aed 0%, #4c1d95 100%);
    }
    .stat-amber {
        background: linear-gradient(135deg, #f59e0b 0%, #b45309 100%);
    }
    .stat-card h4 {
        color: rgba(255,255,255,0.88) !important;
        font-size: 15px !important;
        font-weight: 600 !important;
        margin: 0 0 8px 0 !important;
    }
    .stat-card h2 {
        color: #ffffff !important;
        font-size: 34px !important;
        font-weight: 900 !important;
        margin: 0 0 6px 0 !important;
    }
    .stat-card span {
        font-size: 13px;
        color: rgba(255,255,255,0.9);
        background: rgba(0,0,0,0.18);
        padding: 3px 12px;
        border-radius: 99px;
        font-weight: 600;
    }

    /* بطاقات الموظفين الفاخرة */
    .emp-card {
        background: #ffffff;
        border-radius: 18px;
        padding: 20px;
        border: 1px solid #e2e8f0;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.03);
        margin-bottom: 16px;
        transition: all 0.25s ease;
        display: flex;
        align-items: center;
        justify-content: space-between;
    }
    .emp-card:hover {
        border-color: #38bdf8;
        box-shadow: 0 10px 25px rgba(2, 132, 199, 0.1);
        transform: translateY(-2px);
    }
    .emp-avatar {
        width: 58px;
        height: 58px;
        border-radius: 16px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 24px;
        font-weight: 800;
        color: white;
        margin-left: 16px;
        flex-shrink: 0;
        box-shadow: 0 6px 14px rgba(0,0,0,0.12);
    }
    
    /* شارات الحالة */
    .badge-done {
        background: linear-gradient(135deg, #dcfce7 0%, #bbf7d0 100%);
        color: #166534;
        padding: 6px 16px;
        border-radius: 999px;
        font-weight: 800;
        font-size: 13px;
        border: 1px solid #86efac;
        display: inline-block;
    }
    .badge-wait {
        background: linear-gradient(135deg, #fef3c7 0%, #fde68a 100%);
        color: #92400e;
        padding: 6px 16px;
        border-radius: 999px;
        font-weight: 800;
        font-size: 13px;
        border: 1px solid #fcd34d;
        display: inline-block;
    }

    /* الأزرار والتبويبات */
    .stButton>button {
        background: linear-gradient(135deg, #0d9488 0%, #0284c7 100%) !important;
        color: white !important;
        font-family: 'Cairo', sans-serif !important;
        font-weight: 800 !important;
        font-size: 16px !important;
        border-radius: 12px !important;
        border: none !important;
        padding: 10px 24px !important;
        box-shadow: 0 6px 16px rgba(2, 132, 199, 0.22) !important;
        transition: all 0.25s ease !important;
    }
    .stButton>button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 10px 22px rgba(2, 132, 199, 0.35) !important;
    }
    
    button[data-baseweb="tab"] {
        font-family: 'Cairo', sans-serif !important;
        font-weight: 800 !important;
        font-size: 15px !important;
        padding: 12px 20px !important;
    }

    /* بطاقة تسجيل الدخول */
    .login-box {
        background: #ffffff;
        padding: 32px;
        border-radius: 22px;
        box-shadow: 0 20px 50px rgba(15, 23, 42, 0.08);
        border: 1px solid #e2e8f0;
    }
</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# رسومات وأيقونات SVG فاخرة مدمجة بالكود (تعمل دائماً بدون إنترنت)
# ---------------------------------------------------------
MEDICAL_SHIELD_SVG = """
<svg width="95" height="95" viewBox="0 0 120 120" fill="none" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <linearGradient id="shieldGrad" x1="0" y1="0" x2="120" y2="120" gradientUnits="userSpaceOnUse">
      <stop offset="0%" stop-color="#2dd4bf"/>
      <stop offset="50%" stop-color="#0ea5e9"/>
      <stop offset="100%" stop-color="#3b82f6"/>
    </linearGradient>
    <filter id="glow" x="-20%" y="-20%" width="140%" height="140%">
      <feDropShadow dx="0" dy="8" stdDeviation="8" flood-color="#0284c7" flood-opacity="0.35"/>
    </filter>
  </defs>
  <path d="M60 10L18 28V58C18 85.5 35.8 109.8 60 116C84.2 109.8 102 85.5 102 58V28L60 10Z" fill="url(#shieldGrad)" filter="url(#glow)" stroke="white" stroke-width="3"/>
  <path d="M53 38H67V53H82V67H67V82H53V67H38V53H53V38Z" fill="white"/>
  <circle cx="60" cy="60" r="36" stroke="rgba(255,255,255,0.35)" stroke-width="2" stroke-dasharray="5 5"/>
</svg>
"""

# ---------------------------------------------------------
# قاعدة البيانات (SQLite مدمجة ومحدثة بأسماء الموظفين الستة الجدد)
# ---------------------------------------------------------
DB_FILE = "infection_control_v2.db"

def hash_password(password: str) -> str:
    salt = "ic_salt_2026_mac"
    return hashlib.sha256((password + salt).encode('utf-8')).hexdigest()

def get_db_connection():
    conn = sqlite3.connect(DB_FILE, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn

# قائمة الموظفين الستة المعتمدين مع الألوان والأيقونات والوحدات
DEFAULT_EMPLOYEES = [
    ('Abdullrahman', '1234', 'د. عبدالرحمن', 'employee', 'ترصد العدوى المكتسبة (HAI Surveillance)', '#0d9488', '👨‍⚕️'),
    ('Ahmed', '1234', 'د. أحمد إمام', 'employee', 'التدقيق والجولات الميدانية (IC Audits)', '#0284c7', '🩺'),
    ('Shekah', '1234', 'أ. شيخه البريدي', 'employee', 'نظافة الأيدي والتدريب (Hand Hygiene & Education)', '#7c3aed', '👩‍⚕️'),
    ('Suliman', '1234', 'أ. سليمان الجارالله', 'employee', 'التعقيم المركزي وصحة البيئة (CSSD & Env. Health)', '#ea580c', '🔬'),
    ('Abdullah', '1234', 'د. عبدالله', 'employee', 'صحة العاملين والتطعيمات (Occupational Health)', '#2563eb', '💉'),
    ('A', '1234', 'د. الوليد الرقيبة', 'employee', 'ترصد الميكروبات والمضادات الحيوية (MDRO & Stewardship)', '#059669', '🧬'),
]

def init_db():
    conn = get_db_connection()
    c = conn.cursor()
    
    c.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password_hash TEXT NOT NULL,
        full_name TEXT NOT NULL,
        role TEXT NOT NULL,
        section TEXT NOT NULL,
        badge_color TEXT DEFAULT '#0d9488',
        avatar_icon TEXT DEFAULT '👨‍⚕️'
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
        compliance_rate REAL DEFAULT 0.0,
        critical_alerts TEXT DEFAULT '',
        FOREIGN KEY (user_id) REFERENCES users (id)
    )
    """)
    
    c.execute("SELECT COUNT(*) FROM users")
    if c.fetchone()[0] == 0:
        # حساب رئيس القسم (يدعم الدخول بـ admin / 1234 أو admin123)
        c.execute("""
        INSERT INTO users (username, password_hash, full_name, role, section, badge_color, avatar_icon)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """, ('admin', hash_password('1234'), 'رئيس قسم مكافحة العدوى', 'admin', 'الإدارة والإشراف العام', '#0f172a', '🛡️'))
        
        for username, pwd, name, role, sec, color, icon in DEFAULT_EMPLOYEES:
            c.execute("""
            INSERT INTO users (username, password_hash, full_name, role, section, badge_color, avatar_icon)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (username, hash_password(pwd), name, role, sec, color, icon))
            
    conn.commit()
    conn.close()

init_db()

# ---------------------------------------------------------
# محرك الذكاء الاصطناعي للتلخيص التنفيذي
# ---------------------------------------------------------
def generate_ai_summary_offline(reports_list, week_num, year):
    total_reports = len(reports_list)
    if total_reports == 0:
        return "لا توجد تقارير مقدمة لهذا الأسبوع للتلخيص."
    
    total_audits = sum(r['audits_count'] for r in reports_list)
    avg_compliance = sum(r['compliance_rate'] for r in reports_list) / total_reports if total_reports > 0 else 0
    
    sections_summary = []
    all_challenges = []
    all_plans = []
    
    for r in reports_list:
        sections_summary.append(f"- **{r['full_name']}** (*{r['section']}*):\n  * **الإنجازات:** {r['accomplishments']}")
        if r['challenges'].strip():
            all_challenges.append(f"🚨 **{r['full_name']} ({r['section']})**: {r['challenges']}")
        if r['next_week_plan'].strip():
            all_plans.append(f"🎯 **{r['full_name']} ({r['section']})**: {r['next_week_plan']}")
            
    challenges_text = "\n".join(all_challenges) if all_challenges else "✅ لم يتم رصد أي فاشيات أو تحديات حرجة هذا الأسبوع."
    plans_text = "\n".join(all_plans) if all_plans else "استمرار خطط الترصد والتدقيق الدوري المعتادة."
    
    summary_md = f"""### 🛡️ الملخص التنفيذي الذكي — قسم مكافحة العدوى (الأسبوع {week_num} / {year})

#### 📊 أولاً: مؤشرات الأداء الرئيسية للقسم (KPIs)
- **نسبة تسليم التقارير الأسبوعية:** {total_reports} من أصل 6 أعضاء ({(total_reports/6)*100:.0f}%)
- **إجمالي الجولات الميدانية والتدقيقات المنفذة:** {total_audits} جولة تفتيشية
- **متوسط الامتثال العام بمعايير مكافحة العدوى:** {avg_compliance:.1f}%

---

#### 🏆 ثانياً: أبرز الإنجازات والأعمال المنفذة حسب الأعضاء
{chr(10).join(sections_summary)}

---

#### ⚠️ ثالثاً: التحديات، النواقص، والتنبيهات الوبائية المرصودة
{challenges_text}

---

#### 📅 رابعاً: التوصيات وخطة العمل للأسبوع القادم
{plans_text}
"""
    return summary_md

def call_ollama(prompt, model="llama3"):
    try:
        url = "http://localhost:11434/api/generate"
        data = json.dumps({"model": model, "prompt": prompt, "stream": False}).encode('utf-8')
        req = urllib.request.Request(url, data=data, headers={'Content-Type': 'application/json'})
        with urllib.request.urlopen(req, timeout=30) as resp:
            result = json.loads(resp.read().decode('utf-8'))
            return result.get("response", "")
    except Exception:
        return None

# ---------------------------------------------------------
# إدارة الجلسة وتسجيل الدخول (غير حساس لحالة الأحرف في اسم المستخدم)
# ---------------------------------------------------------
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False
if 'user' not in st.session_state:
    st.session_state.user = None

def login(username, password):
    conn = get_db_connection()
    c = conn.cursor()
    pwd_hash = hash_password(password.strip())
    # البحث بدون حساسية لحالة الأحرف (COLLATE NOCASE) + دعم admin123 أو 1234 للمشرف
    c.execute("SELECT * FROM users WHERE LOWER(username) = LOWER(?)", (username.strip(),))
    user = c.fetchone()
    conn.close()
    if user:
        if user['password_hash'] == pwd_hash or (user['role'] == 'admin' and password.strip() in ['1234', 'admin123']):
            st.session_state.authenticated = True
            st.session_state.user = dict(user)
            return True
    return False

def logout():
    st.session_state.authenticated = False
    st.session_state.user = None
    st.rerun()

# ---------------------------------------------------------
# شاشة تسجيل الدخول الفاخرة
# ---------------------------------------------------------
if not st.session_state.authenticated:
    # بانر علوي فخم
    st.markdown(f"""
    <div class="luxury-hero" style="text-align: center; padding: 40px 24px;">
        <div style="margin-bottom: 12px;">{MEDICAL_SHIELD_SVG}</div>
        <span class="hero-badge">✨ الإصدار الاحترافي الذكي — Infection Control Department</span>
        <h1>منصة التقارير الأسبوعية لقسم مكافحة العدوى</h1>
        <p>نظام رقمي متكامل لمتابعة المؤشرات الوقائية، الجولات الميدانية، والتلخيص التنفيذي بالذكاء الاصطناعي</p>
    </div>
    """, unsafe_allow_html=True)
    
    col_l1, col_l2, col_l3 = st.columns([1, 1.5, 1])
    with col_l2:
        st.markdown('<div class="login-box">', unsafe_allow_html=True)
        st.markdown("### 🔐 بوابة الدخول الموحد")
        st.caption("أدخل اسم المستخدم باللغة الإنجليزية والرقم السري الخاص بك")
        
        with st.form("luxury_login_form"):
            username_input = st.text_input("👤 اسم المستخدم (Username)", placeholder="مثال: Abdullrahman أو Ahmed أو admin")
            password_input = st.text_input("🔑 الرقم السري (Password)", type="password", placeholder="أدخل الرقم السري (1234)")
            submit_login = st.form_submit_button("🚀 تسجيل الدخول إلى المنصة", use_container_width=True)
            
            if submit_login:
                if login(username_input, password_input):
                    st.success("مرحباً بك! جاري فتح لوحة التحكم...")
                    st.rerun()
                else:
                    st.error("❌ اسم المستخدم أو الرقم السري غير صحيح. تأكد من البيانات بالأسفل.")
        st.markdown('</div>', unsafe_allow_html=True)
        
        st.write("")
        with st.expander("📋 قائمة حسابات فريق قسم مكافحة العدوى المعتمدة (الرقم السري الموحد: 1234)"):
            st.markdown("""
            | الاسم | اسم المستخدم (Username) | الرقم السري | الصلاحية |
            | :--- | :--- | :--- | :--- |
            | **رئيس قسم مكافحة العدوى** | `admin` | `1234` | مشرف عام / رئيس القسم |
            | **د. عبدالرحمن** | `Abdullrahman` | `1234` | عضو فريق مكافحة العدوى |
            | **د. أحمد إمام** | `Ahmed` | `1234` | عضو فريق مكافحة العدوى |
            | **أ. شيخه البريدي** | `Shekah` | `1234` | عضو فريق مكافحة العدوى |
            | **أ. سليمان الجارالله** | `Suliman` | `1234` | عضو فريق مكافحة العدوى |
            | **د. عبدالله** | `Abdullah` | `1234` | عضو فريق مكافحة العدوى |
            | **د. الوليد الرقيبة** | `A` | `1234` | عضو فريق مكافحة العدوى |
            """)
    st.stop()

# ---------------------------------------------------------
# الواجهة الرئيسية بعد تسجيل الدخول
# ---------------------------------------------------------
current_user = st.session_state.user

# الشريط الجانبي الفاخر
with st.sidebar:
    st.markdown(f"""
    <div style="text-align: center; padding: 15px 0;">
        <div style="width: 76px; height: 76px; border-radius: 22px; background: rgba(255,255,255,0.15); margin: 0 auto 12px auto; display: flex; align-items: center; justify-content: center; font-size: 38px; border: 2px solid rgba(255,255,255,0.3);">
            {current_user.get('avatar_icon', '👨‍⚕️')}
        </div>
        <h3 style="margin: 0; font-weight: 800; font-size: 20px;">{current_user['full_name']}</h3>
        <p style="margin: 4px 0 12px 0; font-size: 13px; opacity: 0.85;">@{current_user['username']}</p>
        <span style="background: rgba(45, 212, 191, 0.25); border: 1px solid #2dd4bf; padding: 4px 14px; border-radius: 99px; font-size: 12px; font-weight: 700;">
            {'👑 رئيس القسم / المشرف' if current_user['role'] == 'admin' else '🛡️ أخصائي مكافحة عدوى'}
        </span>
    </div>
    """, unsafe_allow_html=True)
    st.divider()
    st.markdown(f"**🏥 التخصص / الوحدة:**\n{current_user['section']}")
    st.markdown(f"**📅 تاريخ اليوم:**\n{datetime.date.today().strftime('%Y-%m-%d')}")
    st.divider()
    if st.button("🚪 تسجيل الخروج", use_container_width=True):
        logout()

# الهيدر البانورامي الداخلي
st.markdown(f"""
<div class="luxury-hero">
    <div style="display: flex; align-items: center; justify-content: space-between; flex-wrap: wrap; gap: 16px;">
        <div>
            <span class="hero-badge">🏥 قسم مكافحة العدوى — Infection Control Department</span>
            <h1>مرحباً بك، {current_user['full_name']} 👋</h1>
            <p>الوحدة الإشرافية: {current_user['section']} | نتمنى لك أسبوعاً حافلاً بالإنجاز والسلامة المرضية</p>
        </div>
        <div style="background: rgba(255,255,255,0.12); padding: 14px 22px; border-radius: 16px; backdrop-filter: blur(10px); text-align: center; border: 1px solid rgba(255,255,255,0.2);">
            <div style="font-size: 13px; color: #bae6fd;">الأسبوع الحالي</div>
            <div style="font-size: 26px; font-weight: 900; color: #ffffff;">الأسبوع {datetime.date.today().isocalendar()[1]} / {datetime.date.today().year}</div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# أولاً: واجهة الموظف (الأعضاء الستة)
# ---------------------------------------------------------
if current_user['role'] == 'employee':
    tab_submit, tab_history = st.tabs(["📝 إرسال التقرير الأسبوعي", "📂 أرشيف تقاريري السابقة"])
    
    with tab_submit:
        today = datetime.date.today()
        current_year, current_week, _ = today.isocalendar()
        
        conn = get_db_connection()
        c = conn.cursor()
        c.execute("SELECT * FROM weekly_reports WHERE user_id = ? AND week_num = ? AND year = ?",
                  (current_user['id'], current_week, current_year))
        existing_report = c.fetchone()
        conn.close()
        
        if existing_report:
            st.success(f"✅ تم رفع تقريرك للأسبوع رقم ({current_week}) بتاريخ {existing_report['date_submitted']}. يمكنك تحديث بياناتك بالأسفل في أي وقت:")
            
        with st.form("emp_report_form"):
            st.markdown("#### 📌 بيانات الفترة الزمنية")
            c_w1, c_w2 = st.columns(2)
            with c_w1:
                week_num = st.number_input("رقم الأسبوع", min_value=1, max_value=53, value=current_week)
            with c_w2:
                year_val = st.number_input("السنة الميلادية", min_value=2024, max_value=2030, value=current_year)
                
            st.markdown("#### 📋 تفاصيل الإنجاز والملاحظات الميدانية")
            accomplishments = st.text_area(
                "1️⃣ أبرز الإنجازات والمهام المنفذة خلال الأسبوع (Accomplishments)",
                value=existing_report['accomplishments'] if existing_report else "",
                placeholder="اكتب هنا ما تم إنجازه من جولات، ترصد، تدريب، أو متابعة حالات...",
                height=130
            )
            
            challenges = st.text_area(
                "2️⃣ التحديات، النواقص، أو الملاحظات الحرجة المرصودة (Challenges & Alerts)",
                value=existing_report['challenges'] if existing_report else "",
                placeholder="اذكر أي معوقات، نقص مستلزمات وقائية، أو حالات تتطلب تدخل إدارة القسم...",
                height=110
            )
            
            next_week_plan = st.text_area(
                "3️⃣ خطة العمل والأولويات للأسبوع القادم (Next Week Plan)",
                value=existing_report['next_week_plan'] if existing_report else "",
                placeholder="ما هي المستهدفات والأقسام المخطط متابعتها في الأسبوع القادم؟",
                height=110
            )
            
            st.markdown("#### 📊 المؤشرات الرقمية الأسبوعية")
            cm1, cm2 = st.columns(2)
            with cm1:
                audits_count = st.number_input(
                    "🔍 عدد الجولات التفقدية / التدقيقات المنجزة",
                    min_value=0, max_value=200,
                    value=existing_report['audits_count'] if existing_report else 6
                )
            with cm2:
                compliance_rate = st.slider(
                    "📈 نسبة الالتزام بمعايير مكافحة العدوى المرصودة (%)",
                    min_value=0.0, max_value=100.0,
                    value=float(existing_report['compliance_rate']) if existing_report else 90.0
                )
                
            save_report_btn = st.form_submit_button("🚀 اعتماد وإرسال التقرير الأسبوعي", use_container_width=True)
            if save_report_btn:
                if not accomplishments.strip():
                    st.error("⚠️ يرجى تدوين إنجازات الأسبوع في الحقل الأول قبل الإرسال.")
                else:
                    now_str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
                    conn = get_db_connection()
                    c = conn.cursor()
                    if existing_report:
                        c.execute("""
                        UPDATE weekly_reports 
                        SET accomplishments = ?, challenges = ?, next_week_plan = ?,
                            audits_count = ?, compliance_rate = ?, date_submitted = ?
                        WHERE id = ?
                        """, (accomplishments, challenges, next_week_plan, audits_count, compliance_rate, now_str, existing_report['id']))
                    else:
                        c.execute("""
                        INSERT INTO weekly_reports (user_id, week_num, year, date_submitted, accomplishments, challenges, next_week_plan, audits_count, compliance_rate)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                        """, (current_user['id'], week_num, year_val, now_str, accomplishments, challenges, next_week_plan, audits_count, compliance_rate))
                    conn.commit()
                    conn.close()
                    st.balloons()
                    st.success("🎉 تم حفظ وإرسال تقريرك الأسبوعي لرئيس القسم بنجاح!")
                    st.rerun()

    with tab_history:
        st.subheader("📚 سجل تقاريرك الأسبوعية المرسلة")
        conn = get_db_connection()
        c = conn.cursor()
        c.execute("SELECT * FROM weekly_reports WHERE user_id = ? ORDER BY year DESC, week_num DESC", (current_user['id'],))
        my_reports = c.fetchall()
        conn.close()
        
        if not my_reports:
            st.info("لم تقم برفع أي تقارير سابقة حتى الآن.")
        else:
            for rep in my_reports:
                with st.expander(f"📅 تقرير الأسبوع ({rep['week_num']}) لعام {rep['year']} — أُرسل بتاريخ: {rep['date_submitted']}"):
                    st.markdown(f"**🏆 الإنجازات:**\n{rep['accomplishments']}")
                    st.markdown(f"**⚠️ التحديات والملاحظات:**\n{rep['challenges'] or 'لا يوجد'}")
                    st.markdown(f"**🎯 خطة الأسبوع القادم:**\n{rep['next_week_plan'] or 'لا يوجد'}")
                    st.markdown(f"**🔍 الجولات المنفذة:** `{rep['audits_count']}` | **📈 نسبة الالتزام:** `{rep['compliance_rate']}%`")

# ---------------------------------------------------------
# ثانياً: واجهة رئيس القسم / المشرف العام
# ---------------------------------------------------------
elif current_user['role'] == 'admin':
    tab_dash, tab_details, tab_ai, tab_team = st.tabs([
        "📊 لوحة المتابعة الحية",
        "📑 استعراض تقارير الفريق",
        "🤖 التلخيص الذكي بالذكاء الاصطناعي",
        "⚙️ إدارة فريق مكافحة العدوى (6 أعضاء)"
    ])
    
    today = datetime.date.today()
    current_year, current_week, _ = today.isocalendar()
    
    # 1. لوحة المتابعة الحية
    with tab_dash:
        conn = get_db_connection()
        c = conn.cursor()
        c.execute("SELECT * FROM users WHERE role = 'employee' ORDER BY id ASC")
        employees = [dict(row) for row in c.fetchall()]
        
        c.execute("""
        SELECT r.*, u.full_name, u.section, u.username, u.badge_color, u.avatar_icon
        FROM weekly_reports r
        JOIN users u ON r.user_id = u.id
        WHERE r.week_num = ? AND r.year = ?
        """, (current_week, current_year))
        submitted_reports = [dict(row) for row in c.fetchall()]
        conn.close()
        
        submitted_user_ids = {r['user_id'] for r in submitted_reports}
        total_emp = len(employees)
        done_count = len(submitted_reports)
        pending_count = total_emp - done_count
        total_aud = sum(r['audits_count'] for r in submitted_reports)
        avg_comp = sum(r['compliance_rate'] for r in submitted_reports) / done_count if done_count > 0 else 0.0
        
        # البطاقات الملونة الأربع الفاخرة
        k1, k2, k3, k4 = st.columns(4)
        with k1:
            st.markdown(f"""
            <div class="stat-card stat-teal">
                <h4>✅ التقارير المستلمة</h4>
                <h2>{done_count} / {total_emp}</h2>
                <span>نسبة الإنجاز {(done_count/total_emp*100) if total_emp else 0:.0f}%</span>
            </div>
            """, unsafe_allow_html=True)
        with k2:
            st.markdown(f"""
            <div class="stat-card stat-amber">
                <h4>⏳ بانتظار التسليم</h4>
                <h2>{pending_count}</h2>
                <span>أعضاء لم يرسلوا بعد</span>
            </div>
            """, unsafe_allow_html=True)
        with k3:
            st.markdown(f"""
            <div class="stat-card stat-blue">
                <h4>🔍 إجمالي الجولات الميدانية</h4>
                <h2>{total_aud}</h2>
                <span>جولة تدقيق هذا الأسبوع</span>
            </div>
            """, unsafe_allow_html=True)
        with k4:
            st.markdown(f"""
            <div class="stat-card stat-purple">
                <h4>📈 متوسط الامتثال العام</h4>
                <h2>{avg_comp:.1f}%</h2>
                <span>معايير مكافحة العدوى</span>
            </div>
            """, unsafe_allow_html=True)
            
        st.markdown("### 👨‍⚕️ حالة تسليم تقارير أعضاء قسم مكافحة العدوى")
        
        # عرض بطاقات الموظفين الستة في شبكتين أنيقة
        col_grid1, col_grid2 = st.columns(2)
        for idx, emp in enumerate(employees):
            is_done = emp['id'] in submitted_user_ids
            rep_obj = next((r for r in submitted_reports if r['user_id'] == emp['id']), None)
            status_html = '<span class="badge-done">تم التسليم بنجاح ✅</span>' if is_done else '<span class="badge-wait">بانتظار الإرسال ⏳</span>'
            sub_date = f"تاريخ الرفع: {rep_obj['date_submitted']}" if rep_obj else "لم يتم رفع تقرير هذا الأسبوع"
            
            card_html = f"""
            <div class="emp-card">
                <div style="display: flex; align-items: center;">
                    <div class="emp-avatar" style="background: {emp.get('badge_color', '#0d9488')};">
                        {emp.get('avatar_icon', '👨‍⚕️')}
                    </div>
                    <div>
                        <h4 style="margin: 0; font-size: 18px; font-weight: 800; color: #0f172a;">{emp['full_name']}</h4>
                        <p style="margin: 2px 0; font-size: 13px; color: #475569; font-weight: 600;">{emp['section']}</p>
                        <span style="font-size: 12px; color: #64748b;">اسم المستخدم: <b>{emp['username']}</b> | {sub_date}</span>
                    </div>
                </div>
                <div>
                    {status_html}
                </div>
            </div>
            """
            if idx % 2 == 0:
                with col_grid1:
                    st.markdown(card_html, unsafe_allow_html=True)
            else:
                with col_grid2:
                    st.markdown(card_html, unsafe_allow_html=True)

    # 2. استعراض التقارير بالتفصيل
    with tab_details:
        st.subheader("📑 استعراض ومراجعة التقارير المرفوعة")
        f1, f2 = st.columns(2)
        with f1:
            sel_week = st.number_input("رقم الأسبوع", min_value=1, max_value=53, value=current_week, key="det_w")
        with f2:
            sel_year = st.number_input("السنة", min_value=2024, max_value=2030, value=current_year, key="det_y")
            
        conn = get_db_connection()
        c = conn.cursor()
        c.execute("""
        SELECT r.*, u.full_name, u.section, u.avatar_icon 
        FROM weekly_reports r
        JOIN users u ON r.user_id = u.id
        WHERE r.week_num = ? AND r.year = ?
        ORDER BY r.id DESC
        """, (sel_week, sel_year))
        filtered_reports = [dict(row) for row in c.fetchall()]
        conn.close()
        
        if not filtered_reports:
            st.info(f"لا توجد تقارير مرفوعة للأسبوع ({sel_week} / {sel_year}) حتى الآن.")
        else:
            for r in filtered_reports:
                with st.expander(f"{r.get('avatar_icon', '📄')} {r['full_name']} — {r['section']} (تاريخ الإرسال: {r['date_submitted']})", expanded=True):
                    m_c1, m_c2 = st.columns(2)
                    with m_c1:
                        st.info(f"🔍 **عدد الجولات الميدانية:** {r['audits_count']} جولات")
                    with m_c2:
                        st.success(f"📈 **نسبة الامتثال المرصودة:** {r['compliance_rate']}%")
                    st.markdown("**1️⃣ الإنجازات المنفذة:**")
                    st.write(r['accomplishments'])
                    st.markdown("**2️⃣ التحديات والملاحظات الحرجة:**")
                    st.write(r['challenges'] if r['challenges'] else "لا توجد ملاحظات مسجلة")
                    st.markdown("**3️⃣ خطة الأسبوع القادم:**")
                    st.write(r['next_week_plan'] if r['next_week_plan'] else "لا توجد خطة مسجلة")

    # 3. التلخيص بالذكاء الاصطناعي
    with tab_ai:
        st.subheader("🤖 المعالجة والتلخيص التنفيذي بالذكاء الاصطناعي")
        st.write("يقوم النظام بدمج وتحليل تقارير الأطباء والأخصائيين الستة واستخراج تقرير تنفيذي موحد جاهز للطباعة أو العرض في اجتماع القسم.")
        
        ai_c1, ai_c2 = st.columns(2)
        with ai_c1:
            ai_week = st.number_input("الأسبوع المراد تلخيصه", min_value=1, max_value=53, value=current_week, key="ai_w")
        with ai_c2:
            ai_year = st.number_input("السنة", min_value=2024, max_value=2030, value=current_year, key="ai_y")
            
        conn = get_db_connection()
        c = conn.cursor()
        c.execute("""
        SELECT r.*, u.full_name, u.section 
        FROM weekly_reports r
        JOIN users u ON r.user_id = u.id
        WHERE r.week_num = ? AND r.year = ?
        """, (ai_week, ai_year))
        target_reports = [dict(row) for row in c.fetchall()]
        conn.close()
        
        st.markdown(f"**عدد التقارير الجاهزة للدمج والتحليل:** `{len(target_reports)}` من أصل `6`")
        
        ai_engine = st.selectbox(
            "اختر محرك الذكاء الاصطناعي:",
            ["المحرك الذكي المدمج (مجاني 100% وفوري بدون إنترنت)", "Ollama المحلي على الماك (Llama 3)"]
        )
        
        if st.button("✨ توليد التقرير التنفيذي الموحد الآن", use_container_width=True):
            if not target_reports:
                st.warning("⚠️ لا توجد تقارير مرفوعة لهذا الأسبوع حتى يتم تلخيصها.")
            else:
                with st.spinner("جاري تحليل تقارير الفريق وصياغة التوصيات..."):
                    if "Ollama" in ai_engine:
                        prompt_text = f"أنت رئيس قسم مكافحة العدوى. لخص التقارير التالية في تقرير تنفيذي احترافي للأسبوع {ai_week}:\n" + json.dumps(target_reports, ensure_ascii=False)
                        summary_result = call_ollama(prompt_text) or generate_ai_summary_offline(target_reports, ai_week, ai_year)
                    else:
                        summary_result = generate_ai_summary_offline(target_reports, ai_week, ai_year)
                        
                    st.success("✅ تم إعداد الملخص التنفيذي الموحد بنجاح!")
                    st.markdown("---")
                    st.markdown(summary_result)
                    
                    st.download_button(
                        label="📥 تحميل الملخص التنفيذي كملف (Markdown)",
                        data=summary_result,
                        file_name=f"Infection_Control_Executive_Summary_W{ai_week}_{ai_year}.md",
                        mime="text/markdown",
                        use_container_width=True
                    )

    # 4. إدارة الموظفين الستة
    with tab_team:
        st.subheader("⚙️ إدارة حسابات فريق قسم مكافحة العدوى")
        st.write("تم ضبط جميع الحسابات بالأسماء المعتمدة والرقم السري الموحد (`1234`)، ويمكنك تعديل أي منها في أي وقت:")
        
        conn = get_db_connection()
        c = conn.cursor()
        c.execute("SELECT * FROM users WHERE role = 'employee' ORDER BY id ASC")
        current_employees = [dict(row) for row in c.fetchall()]
        conn.close()
        
        for emp in current_employees:
            with st.expander(f"{emp.get('avatar_icon', '👤')} تعديل بيانات: {emp['full_name']} ({emp['username']})"):
                with st.form(f"edit_emp_form_{emp['id']}"):
                    col_ed1, col_ed2 = st.columns(2)
                    with col_ed1:
                        new_name = st.text_input("الاسم الظاهر بالعربي", value=emp['full_name'])
                        new_user = st.text_input("اسم المستخدم بالإنجليزي (Username)", value=emp['username'])
                    with col_ed2:
                        new_sec = st.text_input("الوحدة / المهام الإشرافية", value=emp['section'])
                        new_pass = st.text_input("تغيير الرقم السري (الافتراضي الحالي: 1234)", type="password", placeholder="اتركه فارغاً للإبقاء على الرقم السري الحالي")
                        
                    if st.form_submit_button("💾 حفظ التحديثات", use_container_width=True):
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