import streamlit as st
import pandas as pd
import datetime
import json
import time

# إعداد الصفحة
st.set_page_config(page_title="لوحة مدرسة عمر بن مسعود الحية", layout="wide", initial_sidebar_state="collapsed")

# تحميل البيانات
try:
    with open('weekly_data.json', 'r', encoding='utf-8') as f:
        all_data = json.load(f)
except:
    all_data = {}

# جدول التوقيت الدراسي (تنسيق 24 ساعة للمقارنة الدقيقة)
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

# CSS مخصص لإصلاح كافة عيوب التنسيق
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700&family=Tajawal:wght@400;700&display=swap');
    
    html, body, [data-testid="stAppViewContainer"], [data-testid="stHeader"] {
        font-family: 'Cairo', 'Tajawal', sans-serif;
        direction: rtl;
        text-align: right;
        background: radial-gradient(circle, #1a4da1 0%, #0b1a32 100%) !important;
        color: white !important;
    }

    #MainMenu, footer, header {visibility: hidden;}

    /* بطاقة الفصل المدمجة */
    .class-card {
        display: flex;
        flex-direction: row-reverse; /* لجعل رقم الصف على اليمين */
        border: 2px solid white;
        margin-bottom: 10px;
        background-color: white;
        height: 60px;
        align-items: center;
        overflow: hidden;
    }

    .class-label {
        background-color: #1a4da1;
        color: white;
        width: 35%;
        height: 100%;
        display: flex;
        align-items: center;
        justify-content: center;
        font-weight: bold;
        font-size: 1.1rem;
    }

    .teacher-name {
        color: #1a4da1 !important;
        width: 65%;
        height: 100%;
        display: flex;
        align-items: center;
        justify-content: center;
        font-weight: bold;
        font-size: 1rem;
        background-color: white;
        text-align: center;
        padding: 0 5px;
    }

    /* شريط التبويبات */
    .stTabs [data-baseweb="tab-list"] {
        background-color: #0b1a32;
        border: 2px solid white;
        padding: 5px;
    }
    .stTabs [data-baseweb="tab"] { color: white !important; font-weight: bold; }
    .stTabs [aria-selected="true"] { background-color: #1a4da1 !important; }

    /* التذييل المتحرك المصلح */
    .ticker-container {
        position: fixed;
        bottom: 0;
        left: 0;
        width: 100%;
        background-color: #1a4da1;
        border-top: 2px solid white;
        padding: 10px 0;
        z-index: 9999;
        overflow: hidden;
    }

    .ticker-wrap {
        width: 100%;
        overflow: hidden;
        white-space: nowrap;
    }

    .ticker-move {
        display: inline-block;
        padding-right: 100%;
        animation: ticker 30s linear infinite;
        color: white;
        font-weight: bold;
        font-size: 1.2rem;
    }

    @keyframes ticker {
        0% { transform: translateX(-100%); }
        100% { transform: translateX(100%); }
    }
    </style>
    """, unsafe_allow_html=True)

# الرأس التفاعلي
st.components.v1.html("""
    <div style="display: flex; justify-content: space-between; align-items: center; background-color: #0b1a32; padding: 10px 15px; border: 2px solid white; color: white; font-family: 'Cairo', sans-serif; direction: rtl;">
        <div style="background-color: #1a4da1; border: 2px solid white; padding: 5px 25px; font-size: 1.5rem; font-weight: bold;" id="day-txt">...</div>
        <div style="display: flex; justify-content: space-between; align-items: center; flex-grow: 1; margin: 0 20px;">
            <div style="font-size: 1.1rem;">3 رمضان 1447</div>
            <div style="font-size: 2.8rem; font-weight: bold;" id="clock-txt">00:00:00</div>
            <div style="font-size: 1.1rem;" id="date-txt">...</div>
        </div>
    </div>
    <script>
        function update() {
            const now = new Date();
            const days = ["الأحد", "الإثنين", "الثلاثاء", "الأربعاء", "الخميس", "الجمعة", "السبت"];
            document.getElementById('day-txt').innerText = days[now.getDay()];
            document.getElementById('clock-txt').innerText = now.toLocaleTimeString('en-GB');
            document.getElementById('date-txt').innerText = now.getDate() + "-" + (now.getMonth()+1) + "-" + now.getFullYear();
        }
        setInterval(update, 1000); update();
    </script>
    """, height=100)

# حساب الحصة واليوم في بايثون
now = datetime.datetime.now()
current_time = now.strftime("%H:%M")
current_session = None
for s in SCHEDULE_TIMES:
    if s["start"] <= current_time < s["end"]:
        current_session = s["name"]
        break

days_ar = {0: "الإثنين", 1: "الثلاثاء", 2: "الأربعاء", 3: "الخميس", 6: "الأحد"}
current_day = days_ar.get(now.weekday(), "الأحد")

tab1, tab2, tab3 = st.tabs(["اللوحة العامة", "جداول الفصول الحالية", "المناوبة"])

with tab1:
    col1, col2, col3 = st.columns([1, 1.2, 1])
    with col1:
        st.markdown('<div style="background-color:#1a4da1; padding:5px; text-align:center; font-weight:bold; border:2px solid white;">برنامج اليوم الدراسي</div>', unsafe_allow_html=True)
        st.markdown("""
            <table style="width:100%; border-collapse:collapse; color:white; border:1px solid white; text-align:center; font-size:0.8rem;">
                <tr style="background-color:#1a4da1;"><th>الحصة</th><th>من</th><th>إلى</th></tr>
                <tr><td>الأولى</td><td>07:25</td><td>08:05</td></tr>
                <tr><td>الثانية</td><td>08:10</td><td>08:50</td></tr>
                <tr><td>الثالثة</td><td>08:55</td><td>09:35</td></tr>
                <tr><td>الرابعة</td><td>09:40</td><td>10:20</td></tr>
                <tr style="background-color:rgba(255,255,255,0.1);"><td>الفسحة</td><td>10:20</td><td>10:45</td></tr>
                <tr><td>الخامسة</td><td>10:45</td><td>11:25</td></tr>
                <tr><td>السادسة</td><td>11:30</td><td>12:10</td></tr>
                <tr><td>السابعة</td><td>12:15</td><td>12:55</td></tr>
                <tr><td>الثامنة</td><td>13:00</td><td>13:40</td></tr>
            </table>
        """, unsafe_allow_html=True)
    with col2:
        st.components.v1.html(f"""
            <div style="text-align: center; color: white; font-family: 'Cairo', sans-serif; direction: rtl;">
                <div style="border: 3px solid white; background-color: #1a4da1; padding: 10px; border-radius: 8px; margin-bottom: 20px;">
                    <div style="font-size: 1.2rem;">الحصة الحالية</div>
                    <div style="font-size: 2.5rem; font-weight: bold;">{current_session if current_session else "فترة استراحة"}</div>
                </div>
                <div style="position: relative; width: 180px; height: 180px; margin: 0 auto;">
                    <svg viewBox="0 0 100 100" style="transform: rotate(-90deg); width: 100%; height: 100%;">
                        <circle cx="50" cy="50" r="45" fill="none" stroke="rgba(255,255,255,0.2)" stroke-width="8"></circle>
                        <circle cx="50" cy="50" r="45" fill="none" stroke="white" stroke-width="8" stroke-dasharray="283" stroke-dashoffset="100"></circle>
                    </svg>
                    <div style="position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%) rotate(0deg); text-align: center;">
                        <div style="font-size: 3.5rem; font-weight: bold;">12</div>
                        <div style="font-size: 1.1rem;">دقيقة</div>
                    </div>
                </div>
                <div style="margin-top:20px; font-weight:bold;">هيثم الغافري | توفيق اليعقوبي</div>
            </div>
        """, height=380)
    with col3:
        st.markdown('<div style="background-color:rgba(26, 77, 161, 0.3); border:2px solid white; padding:15px; text-align:center;">رؤية المدرسة : نحو مدرسةٍ رائدةٍ بأداءٍ متميزٍ</div>', unsafe_allow_html=True)
        if st.button("الجدول العام للمعلمين", use_container_width=True):
            st.image("جدول.png")

with tab2:
    st.markdown(f'<h3 style="text-align:center; color:#b8d000; margin-bottom:20px;">حصص اليوم: {current_day} | الحصة: {current_session if current_session else "---"}</h3>', unsafe_allow_html=True)
    
    if all_data and current_day in all_data:
        day_rows = all_data[current_day]
        cols = st.columns(4)
        for i, row in enumerate(day_rows):
            with cols[i % 4]:
                # جلب المعلم إذا كنا في وقت حصة
                teacher = row.get(current_session, "") if current_session else ""
                st.markdown(f"""
                    <div class="class-card">
                        <div class="class-label">الصف {row["الصف"]}</div>
                        <div class="teacher-name">{teacher}</div>
                    </div>
                """, unsafe_allow_html=True)
    else:
        st.warning("لا توجد بيانات متاحة لهذا اليوم.")

# تذييل الصفحة المصلح تماماً
st.markdown("""
    <div class="ticker-container">
        <div class="ticker-wrap">
            <div class="ticker-move">
                مدرسة عمر بن مسعود للتعليم الأساسي ترحب بكم ... نتمنى لطلابنا يوماً دراسياً موفقاً ومليئاً بالنجاح والتميز ...
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

# التحديث التلقائي
time.sleep(30)
st.rerun()
