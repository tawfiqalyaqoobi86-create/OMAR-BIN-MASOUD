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

# جدول التوقيت الدراسي الرسمي (يتحكم في ظهور واختفاء الأسماء)
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

# ضبط المنطقة الزمنية (سلطنة عمان)
timezone_offset = datetime.timezone(datetime.timedelta(hours=4))

# CSS مخصص للوضوح العالي والألوان الأصلية
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

    /* تنسيق جداول الفصول الحية - تحديث الألوان */
    .live-grade-table {
        width: 100%;
        background-color: white;
        border-collapse: collapse;
        margin-bottom: 5px;
        table-layout: fixed;
    }

    .live-grade-table td {
        border: 2px solid #1a4da1;
        padding: 12px 5px;
        font-weight: bold;
        text-align: center;
        height: 50px;
    }

    .class-name-cell {
        background-color: #1a4da1;
        color: white !important;
        width: 35%;
        font-size: 1.1rem;
    }

    .teacher-live-cell {
        background-color: white;
        color: #1a4da1 !important; /* اللون الأزرق الأصلي */
        font-size: 1rem;
        word-wrap: break-word;
    }

    /* التذييل المتحرك */
    .ticker-footer {
        background-color: #1a4da1;
        border: 1px solid white;
        padding: 8px;
        position: fixed;
        bottom: 5px;
        left: 10px;
        right: 10px;
        overflow: hidden;
    }

    .ticker-text {
        display: inline-block;
        padding-left: 100%;
        animation: marquee 30s linear infinite;
        color: white;
        font-weight: bold;
    }

    @keyframes marquee {
        0% { transform: translateX(0); }
        100% { transform: translateX(-100%); }
    }
    </style>
    """, unsafe_allow_html=True)

# الساعة العلوية
st.components.v1.html("""
    <div style="display: flex; justify-content: space-between; align-items: center; background-color: #0b1a32; padding: 10px 15px; border: 2px solid white; color: white; font-family: 'Cairo', sans-serif; direction: rtl;">
        <div style="background-color: #1a4da1; border: 2px solid white; padding: 5px 25px; font-size: 1.5rem; font-weight: bold;" id="day-box"></div>
        <div style="display: flex; justify-content: space-between; align-items: center; flex-grow: 1; margin: 0 20px;">
            <div style="font-size: 1.1rem;">3 رمضان 1447</div>
            <div style="font-size: 2.8rem; font-weight: bold; text-shadow: 0 0 10px white;" id="clock-box">00:00:00</div>
            <div style="font-size: 1.1rem;" id="date-box"></div>
        </div>
    </div>
    <script>
        function tick() {
            const now = new Date();
            const days = ["الأحد", "الإثنين", "الثلاثاء", "الأربعاء", "الخميس", "الجمعة", "السبت"];
            document.getElementById('day-box').innerText = days[now.getDay()];
            document.getElementById('clock-box').innerText = now.toLocaleTimeString('en-GB');
            document.getElementById('date-box').innerText = now.getDate() + "-" + (now.getMonth()+1) + "-" + now.getFullYear();
        }
        setInterval(tick, 1000); tick();
    </script>
    """, height=100)

# تحديد الحصة الحالية برمجياً (بناءً على وقت النظام المحلى في عمان)
def get_current_session_key():
    now_local = datetime.datetime.now(timezone_offset)
    current_time = now_local.strftime("%H:%M")
    for s in SCHEDULE_TIMES:
        if s["start"] <= current_time < s["end"]:
            return s["name"]
    return None

current_session = get_current_session_key()
# تحديد اليوم (بايثون يبدأ الإثنين بـ 0)
days_ar_map = {0: "الإثنين", 1: "الثلاثاء", 2: "الأربعاء", 3: "الخميس", 6: "الأحد"}
now_py = datetime.datetime.now(timezone_offset)
current_day = days_ar_map.get(now_py.weekday(), "الأحد")

tab1, tab2, tab3 = st.tabs(["اللوحة العامة", "جداول الفصول الحالية", "المناوبة"])

with tab1:
    col1, col2, col3 = st.columns([1, 1.2, 1])
    with col1:
        st.markdown('<div style="background-color:#1a4da1; padding:8px; text-align:center; font-weight:bold; border:2px solid white;">برنامج اليوم الدراسي</div>', unsafe_allow_html=True)
        st.markdown("""
            <table style="width:100%; border-collapse:collapse; color:white; border:1px solid white; text-align:center; font-size:0.85rem;">
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
        st.components.v1.html("""
            <div style="text-align: center; color: white; font-family: 'Cairo', sans-serif; direction: rtl;">
                <div style="border: 3px solid white; background-color: #1a4da1; padding: 10px; border-radius: 8px; margin-bottom: 20px;">
                    <div style="font-size: 1.2rem;">الحصة الحالية</div>
                    <div style="font-size: 2.5rem; font-weight: bold;" id="sess-name">...</div>
                </div>
                <div style="position: relative; width: 180px; height: 180px; margin: 0 auto;">
                    <svg viewBox="0 0 100 100" style="transform: rotate(-90deg); width: 100%; height: 100%;">
                        <circle cx="50" cy="50" r="45" fill="none" stroke="rgba(255,255,255,0.2)" stroke-width="8"></circle>
                        <circle id="p-circle" cx="50" cy="50" r="45" fill="none" stroke="white" stroke-width="8" stroke-dasharray="283" stroke-dashoffset="283"></circle>
                    </svg>
                    <div style="position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%) rotate(0deg);">
                        <div style="font-size: 3.5rem; font-weight: bold;" id="t-mins">00</div>
                        <div style="font-size: 1.1rem; font-weight: bold;">دقيقة</div>
                    </div>
                </div>
            </div>
            <script>
                const sch = [
                    {n:"الطابور", s:"07:10", e:"07:25"}, {n:"الأولى", s:"07:25", e:"08:05"},
                    {n:"الثانية", s:"08:10", e:"08:50"}, {n:"الثالثة", s:"08:55", e:"09:35"},
                    {n:"الرابعة", s:"09:40", e:"10:20"}, {n:"الفسحة", s:"10:20", e:"10:45"},
                    {n:"الخامسة", s:"10:45", e:"11:25"}, {n:"السادسة", s:"11:30", e:"12:10"},
                    {n:"السابعة", s:"12:15", e:"12:55"}, {n:"الثامنة", s:"13:00", e:"13:40"}
                ];
                function up() {
                    const n = new Date();
                    const c = n.getHours().toString().padStart(2,'0') + ":" + n.getMinutes().toString().padStart(2,'0');
                    let a = sch.find(s => c >= s.s && c < s.e);
                    if(a) {
                        document.getElementById('sess-name').innerText = a.n;
                        const [eh, em] = a.e.split(':').map(Number);
                        const ed = new Date(); ed.setHours(eh, em, 0);
                        document.getElementById('t-mins').innerText = Math.ceil((ed - n)/60000);
                        const [sh, sm] = a.s.split(':').map(Number);
                        const sd = new Date(); sd.setHours(sh, sm, 0);
                        const off = 283 - ((n - sd)/(ed - sd) * 283);
                        document.getElementById('p-circle').style.strokeDashoffset = off;
                    } else {
                        document.getElementById('sess-name').innerText = "فترة راحة";
                        document.getElementById('t-mins').innerText = "00";
                    }
                }
                setInterval(up, 1000); up();
            </script>
        """, height=350)
        st.markdown(f'<div style="text-align:center; font-weight:bold;">مدير المدرسة: هيثم الغافري | المدير المساعد: توفيق اليعقوبي</div>', unsafe_allow_html=True)
        
    with col3:
        st.markdown("""
            <div style="background-color:rgba(26, 77, 161, 0.2); border:2px solid white; padding:15px; margin-bottom:10px; text-align:center;">
                <h3 style="color:#b8d000; margin:0;">رؤية المدرسة</h3>
                <p style="font-size:0.9rem;">نحو مدرسةٍ رائدةٍ بأداءٍ متميزٍ وشراكةٍ مجتمعيةٍ فاعلةٍ</p>
            </div>
            <div style="background-color:rgba(26, 77, 161, 0.2); border:2px solid white; padding:15px; text-align:center;">
                <h3 style="color:#b8d000; margin:0;">رسالة المدرسة</h3>
                <p style="font-size:0.8rem;">نسعى إلى توفير بيئة تعليمية محفزة تحقق التميز...</p>
            </div>
        """, unsafe_allow_html=True)
        if st.button("الجدول العام للمعلمين", use_container_width=True):
            st.image("جدول.png")

with tab2:
    status_text = f"الحصة الحالية: {current_session}" if current_session else "الوقت الحالي: فترة استراحة (لا توجد حصص)"
    st.markdown(f'<h3 style="text-align:center; color:#b8d000; margin-bottom:15px;">{status_text}</h3>', unsafe_allow_html=True)
    
    if all_data and current_day in all_data:
        day_rows = all_data[current_day]
        cols = st.columns(4)
        for i, row in enumerate(day_rows):
            with cols[i % 4]:
                # المنطق المطلوب: إذا لم نكن في وقت حصة (مثلاً 08:06)، يظهر فراغ
                # الحصة يجب أن تكون من ضمن الحصص (الأولى - الثامنة) حصراً لتظهر الأسماء
                teacher = row.get(current_session, "") if current_session in ["الأولى", "الثانية", "الثالثة", "الرابعة", "الخامسة", "السادسة", "السابعة", "الثامنة"] else ""
                
                st.markdown(f"""
                    <table class="live-grade-table">
                        <tr>
                            <td class="class-name-cell">الصف {row["الصف"]}</td>
                            <td class="teacher-live-cell">{teacher}</td>
                        </tr>
                    </table>
                """, unsafe_allow_html=True)
    else:
        st.info(f"اليوم هو {current_day} (إجازة مدرسية) أو لا توجد بيانات.")

with tab3:
    st.markdown("""
        <div style="display:flex; gap:10px; direction:rtl;">
            <div style="flex:2; border:2px solid white; padding:10px;">
                <table style="width:100%; text-align:center; border-collapse:collapse; background-color:white;">
                    <tr style="background-color:#b8d000; color:black;">
                        <th>جناح الخامس</th><th>جناح السادس</th><th>جناح السابع</th><th>جناح الثامن</th>
                    </tr>
                    <tr style="color:#1a4da1; font-weight:bold;"><td>-</td><td>-</td><td>-</td><td>-</td></tr>
                </table>
            </div>
            <div style="flex:1; background-color:#1a4da1; border:2px solid white; padding:15px; text-align:center;">
                <h3 style="margin:0; color:#b8d000;">المادة المناوبة</h3>
                <p>المادة: <b>اللغة العربية</b></p>
                <p>المعلم المشرف: <b>محمد الشلع</b></p>
            </div>
        </div>
    """, unsafe_allow_html=True)

st.markdown("""
    <div class="ticker-footer"><div class="ticker-text">
        مدرسة عمر بن مسعود للتعليم الأساسي ترحب بكم ... نتمنى لطلابنا يوماً دراسياً موفقاً
    </div></div>
    """, unsafe_allow_html=True)

# تحديث الصفحة كل 30 ثانية لضمان دقة ظهور واختفاء الأسماء
time.sleep(30)
st.rerun()
