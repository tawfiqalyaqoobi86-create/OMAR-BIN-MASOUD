import streamlit as st
import pandas as pd
import datetime
import json
import time

# إعداد الصفحة
st.set_page_config(page_title="لوحة مدرسة عمر بن مسعود الحية", layout="wide", initial_sidebar_state="collapsed")

# تحميل البيانات وتجهيزها
try:
    with open('weekly_data.json', 'r', encoding='utf-8') as f:
        raw_data = json.load(f)
        all_data = {k.strip(): v for k, v in raw_data.items()}
except:
    all_data = {}

# خريطة تحويل أسماء الصفوف
CLASS_MAP = {
    "5/1": "الخامس أول", "5/2": "الخامس ثاني", "5/3": "الخامس ثالث", "5/4": "الخامس رابع",
    "6/1": "السادس أول", "6/2": "السادس ثاني", "6/3": "السادس ثالث", "6/4": "السادس رابع",
    "7/1": "السابع أول", "7/2": "السابع ثاني", "7/3": "السابع ثالث",
    "8/1": "الثامن أول", "8/2": "الثامن ثاني", "8/3": "الثامن ثالث",
    "9/1": "التاسع أول", "9/2": "التاسع ثاني", "9/3": "التاسع ثالث",
    "10/1": "العاشر أول", "10/2": "العاشر ثاني", "10/3": "العاشر ثالث",
    "11/1": "الحادي عشر اول", "11/2": "الحادي عشر ثاني", "11/3": "الحادي عشر ثالث", "11/4": "الحادي عشر رابع",
    "12/1": "الثاني عشر أول", "12/2": "الثاني عشر ثاني", "12/3": "الثاني عشر ثالث", "12/4": "الثاني عشر رابع"
}

# جدول التوقيت الدراسي
SCHEDULE_TIMES = [
    {"name": "الأولى", "start": "07:25", "end": "08:05"},
    {"name": "الثانية", "start": "08:10", "end": "08:50"},
    {"name": "الثالثة", "start": "08:55", "end": "09:35"},
    {"name": "الرابعة", "start": "09:40", "end": "10:20"},
    {"name": "الخامسة", "start": "10:45", "end": "11:25"},
    {"name": "السادسة", "start": "11:30", "end": "12:10"},
    {"name": "السابعة", "start": "12:15", "end": "12:55"},
    {"name": "الثامنة", "start": "13:00", "end": "13:40"},
]

# CSS
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700&display=swap');
    html, body, [data-testid="stAppViewContainer"] {
        font-family: 'Cairo', sans-serif;
        direction: rtl;
        background: radial-gradient(circle, #1a4da1 0%, #0b1a32 100%) !important;
        color: white;
    }
    #MainMenu, footer, header {visibility: hidden;}
    .grade-group-box { border: 2px solid #b8d000; margin-bottom: 15px; background-color: rgba(0,0,0,0.2); border-radius: 5px; overflow: hidden; }
    .grade-header { background-color: #b8d000; color: black; text-align: center; font-weight: bold; padding: 5px; font-size: 1.1rem; }
    .class-row-table { width: 100%; border-collapse: collapse; background-color: white; table-layout: fixed; }
    .class-row-table td { border: 1px solid #1a4da1; padding: 10px 5px; font-weight: bold; text-align: center; height: 55px; vertical-align: middle; }
    .class-label-cell { background-color: #1a4da1; color: white !important; width: 35%; font-size: 1rem; }
    .teacher-name-cell { background-color: white; color: #1a4da1 !important; width: 65%; font-size: 0.95rem; }
    .ticker-footer { position: fixed; bottom: 0; left: 0; width: 100%; background-color: #1a4da1; border-top: 2px solid white; padding: 8px; z-index: 999; overflow: hidden; white-space: nowrap; }
    .ticker-text { display: inline-block; padding-left: 100%; animation: marquee 30s linear infinite; font-weight: bold; font-size: 1.2rem; }
    @keyframes marquee { 0% { transform: translateX(0); } 100% { transform: translateX(-100%); } }
    .stTabs [data-baseweb="tab-list"] { background-color: #0b1a32; border: 2px solid white; padding: 5px; }
    .stTabs [data-baseweb="tab"] { color: white !important; font-weight: bold; }
    .stTabs [aria-selected="true"] { background-color: #1a4da1 !important; }
    </style>
    """, unsafe_allow_html=True)

# الرأس مع جلب وقت المتصفح عبر JS لضمان المزامنة
st.components.v1.html(f"""
    <div style="display: flex; justify-content: space-between; align-items: center; background-color: #0b1a32; padding: 10px 15px; border: 2px solid white; color: white; font-family: 'Cairo', sans-serif; direction: rtl;">
        <div style="background-color: #1a4da1; border: 2px solid white; padding: 5px 25px; font-size: 1.5rem; font-weight: bold;" id="live-day">...</div>
        <div style="display: flex; justify-content: space-between; align-items: center; flex-grow: 1; margin: 0 20px;">
            <div style="font-size: 1.1rem;">3 رمضان 1447</div>
            <div style="font-size: 2.8rem; font-weight: bold;" id="live-clock">00:00:00</div>
            <div style="font-size: 1.1rem;" id="live-date">...</div>
        </div>
    </div>
    <script>
        function update() {{
            const now = new Date();
            const days = ["الأحد", "الإثنين", "الثلاثاء", "الأربعاء", "الخميس", "الجمعة", "السبت"];
            document.getElementById('live-day').innerText = days[now.getDay()];
            document.getElementById('live-clock').innerText = now.toLocaleTimeString('en-GB');
            document.getElementById('live-date').innerText = now.getDate() + "-" + (now.getMonth()+1) + "-" + now.getFullYear();
        }}
        setInterval(update, 1000); update();
    </script>
    """, height=100)

# حساب الحصة الحالية (بايثون يحتاج وقت دقيق)
timezone_offset = datetime.timezone(datetime.timedelta(hours=4))
now_local = datetime.datetime.now(timezone_offset)
current_time_str = now_local.strftime("%H:%M")

auto_session = None
for s in SCHEDULE_TIMES:
    if s["start"] <= current_time_str < s["end"]:
        auto_session = s["name"]
        break

days_ar_map = {0: "الإثنين", 1: "الثلاثاء", 2: "الأربعاء", 3: "الخميس", 6: "الأحد"}
current_day = days_ar_map.get(now_local.weekday(), "الأحد")

tab1, tab2, tab3 = st.tabs(["اللوحة العامة", "جداول الفصول الحالية", "المناوبة"])

with tab1:
    col1, col2, col3 = st.columns([1, 1.2, 1])
    with col1:
        st.markdown('<div style="background-color:#1a4da1; padding:5px; text-align:center; font-weight:bold; border:2px solid white;">برنامج اليوم الدراسي</div>', unsafe_allow_html=True)
        st.markdown('<table style="width:100%; text-align:center; border:1px solid white; border-collapse:collapse; font-size:0.8rem;"><tr><th>الحصة</th><th>من</th><th>إلى</th></tr><tr><td>الأولى</td><td>07:25</td><td>08:05</td></tr><tr><td>الثانية</td><td>08:10</td><td>08:50</td></tr><tr><td>الثالثة</td><td>08:55</td><td>09:35</td></tr><tr><td>الرابعة</td><td>09:40</td><td>10:20</td></tr><tr><td>الخامسة</td><td>10:45</td><td>11:25</td></tr><tr><td>السادسة</td><td>11:30</td><td>12:10</td></tr><tr><td>السابعة</td><td>12:15</td><td>12:55</td></tr><tr><td>الثامنة</td><td>13:00</td><td>13:40</td></tr></table>', unsafe_allow_html=True)
    with col2:
        st.markdown(f'<div style="border:3px solid white; background-color:#1a4da1; padding:15px; text-align:center; border-radius:10px;"><h3>الحصة الحالية</h3><h1 style="font-size:3rem;">{auto_session if auto_session else "فترة استراحة"}</h1></div>', unsafe_allow_html=True)
        st.markdown('<div style="text-align:center; margin-top:20px; font-weight:bold;">هيثم الغافري | توفيق اليعقوبي</div>', unsafe_allow_html=True)
    with col3:
        st.info("رؤية المدرسة : نحو مدرسةٍ رائدةٍ بأداءٍ متميزٍ")
        if st.button("الجدول العام للمعلمين", use_container_width=True):
            st.image("جدول.png")

with tab2:
    # إضافة خيار يدوي في حال فشل التوقيت التلقائي
    chosen_session = st.selectbox("اختر الحصة يدوياً إذا لم تظهر تلقائياً", ["تلقائي"] + [s["name"] for s in SCHEDULE_TIMES])
    active_session = auto_session if chosen_session == "تلقائي" else chosen_session
    
    st.markdown(f'<h2 style="text-align:center; color:#b8d000;">حصص {current_day} - {active_session if active_session else "فترة استراحة"}</h2>', unsafe_allow_html=True)
    
    # محاولة جلب اليوم بأكثر من صيغة (بهمزة وبدون)
    day_data = all_data.get(current_day) or all_data.get(current_day.replace("إ", "ا"))
    
    if day_data:
        grades = ["الخامس", "السادس", "السابع", "الثامن", "التاسع", "العاشر", "الحادي عشر", "الثاني عشر"]
        grid_cols = st.columns(4)
        for idx, g_name in enumerate(grades):
            with grid_cols[idx % 4]:
                st.markdown(f'<div class="grade-group-box"><div class="grade-header">الصف {g_name}</div>', unsafe_allow_html=True)
                for row in day_data:
                    c_code = row.get("الصف", "")
                    # منطق تحديد الصف (مثلاً 5/1 يتبع الخامس)
                    is_match = False
                    if g_name == "الخامس" and "5/" in c_code: is_match = True
                    elif g_name == "السادس" and "6/" in c_code: is_match = True
                    elif g_name == "السابع" and "7/" in c_code: is_match = True
                    elif g_name == "الثامن" and "8/" in c_code: is_match = True
                    elif g_name == "التاسع" and "9/" in c_code: is_match = True
                    elif g_name == "العاشر" and "10/" in c_code: is_match = True
                    elif g_name == "الحادي عشر" and "11/" in c_code: is_match = True
                    elif g_name == "الثاني عشر" and "12/" in c_code: is_match = True
                    
                    if is_match:
                        display_name = CLASS_MAP.get(c_code, c_code)
                        teacher = row.get(active_session, "") if active_session else ""
                        st.markdown(f"""
                            <table class="class-row-table">
                                <tr>
                                    <td class="class-label-cell">{display_name}</td>
                                    <td class="teacher-name-cell">{teacher}</td>
                                </tr>
                            </table>
                        """, unsafe_allow_html=True)
                st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.error(f"لم يتم العثور على بيانات ليوم {current_day} في ملف JSON")

st.markdown('<div class="ticker-footer"><div class="ticker-text">مدرسة عمر بن مسعود للتعليم الأساسي ترحب بكم ... نتمنى لطلابنا يوماً دراسياً موفقاً</div></div>', unsafe_allow_html=True)

# تحديث تلقائي كل دقيقة
time.sleep(60)
st.rerun()
