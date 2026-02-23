import streamlit as st
import pandas as pd
import datetime
import json
import time

# إعداد الصفحة
st.set_page_config(page_title="لوحة مدرسة عمر بن مسعود", layout="wide", initial_sidebar_state="collapsed")

# تحميل البيانات
try:
    with open('weekly_data.json', 'r', encoding='utf-8') as f:
        all_data = json.load(f)
except:
    all_data = {}

# التوقيت الزمني للحصص (مطابق للمدرسة)
SCHEDULE_TIMES = [
    {"name": "الطابور", "start": "07:10", "end": "07:25"},
    {"name": "الأولى", "start": "07:25", "end": "08:05"},
    {"name": "الثانية", "start": "08:10", "end": "08:50"},
    {"name": "الثالثة", "start": "08:55", "end": "09:35"},
    {"name": "الرابعة", "start": "09:40", "end": "10:20"},
    {"name": "الفسحة", "start": "10:20", "end": "10:45"},
    {"name": "الخامسة", "start": "10:45", "end": "11:25"},
    {"name": "السادسة", "start": "11:30", "end": "12:10"},
    {"name": "السابعة", "start": "12:15", "end": "12:55"},
    {"name": "الثامنة", "start": "13:00", "end": "13:40"},
]

# ضبط المنطقة الزمنية لسلطنة عمان (UTC+4)
timezone_offset = datetime.timezone(datetime.timedelta(hours=4))
now_local = datetime.datetime.now(timezone_offset)

# CSS مخصص لتحسين الألوان والوضوح
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

    /* جداول الفصول الحية */
    .live-grade-table {
        width: 100%;
        background-color: white;
        border-collapse: collapse;
        margin-bottom: 8px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.3);
    }

    .live-grade-table td {
        border: 2px solid #1a4da1;
        padding: 10px;
        font-weight: bold;
        text-align: center;
    }

    .class-name-cell {
        background-color: #1a4da1;
        color: white !important;
        width: 40%;
        font-size: 1.1rem;
    }

    /* تغيير لون الخط للأزرق الواضح بدلاً من الأسود */
    .teacher-live-cell {
        background-color: white;
        color: #0066cc !important; 
        font-size: 1rem;
    }

    .ticker-footer {
        background-color: #1a4da1;
        border: 2px solid white;
        padding: 10px;
        position: fixed;
        bottom: 5px;
        left: 10px;
        right: 10px;
        overflow: hidden;
        white-space: nowrap;
        z-index: 1000;
    }

    .ticker-text {
        display: inline-block;
        padding-left: 100%;
        animation: marquee 35s linear infinite;
        color: white;
        font-weight: bold;
        font-size: 1.2rem;
    }

    @keyframes marquee {
        0% { transform: translateX(0); }
        100% { transform: translateX(-100%); }
    }
    </style>
    """, unsafe_allow_html=True)

# الرأس مع التوقيت (يستخدم وقت المتصفح للعرض)
st.components.v1.html("""
    <div style="display: flex; justify-content: space-between; align-items: center; background-color: #0b1a32; padding: 10px 15px; border: 2px solid white; color: white; font-family: 'Cairo', sans-serif; direction: rtl;">
        <div style="background-color: #1a4da1; border: 2px solid white; padding: 5px 25px; font-size: 1.5rem; font-weight: bold;" id="current-day"></div>
        <div style="display: flex; justify-content: space-between; align-items: center; flex-grow: 1; margin: 0 20px;">
            <div style="font-size: 1.1rem;">3 رمضان 1447</div>
            <div style="font-size: 2.8rem; font-weight: bold; text-shadow: 0 0 10px white;" id="live-clock">00:00:00</div>
            <div style="font-size: 1.1rem;" id="gregorian-date"></div>
        </div>
    </div>
    <script>
        function updateClock() {
            const now = new Date();
            const days = ["الأحد", "الإثنين", "الثلاثاء", "الأربعاء", "الخميس", "الجمعة", "السبت"];
            document.getElementById('current-day').innerText = days[now.getDay()];
            document.getElementById('live-clock').innerText = now.toLocaleTimeString('en-GB');
            const d = now.getDate(); const m = now.getMonth() + 1; const y = now.getFullYear();
            document.getElementById('gregorian-date').innerText = d + "-" + m + "-" + y;
        }
        setInterval(updateClock, 1000);
        updateClock();
    </script>
    """, height=100)

# تحديد الحصة واليوم برمجياً في بايثون (باستخدام توقيت عمان)
def get_current_session_info():
    now = datetime.datetime.now(timezone_offset)
    current_time = now.strftime("%H:%M")
    for session in SCHEDULE_TIMES:
        if session["start"] <= current_time < session["end"]:
            return session["name"]
    return None

current_session_name = get_current_session_info()
days_map = {0: "الإثنين", 1: "الثلاثاء", 2: "الأربعاء", 3: "الخميس", 6: "الأحد"}
current_day_name = days_map.get(now_local.weekday(), "الأحد")

tab1, tab2, tab3 = st.tabs(["اللوحة العامة", "جداول الفصول الحالية", "المناوبة"])

with tab1:
    col_right, col_center, col_left = st.columns([1, 1.2, 1])
    with col_right:
        st.markdown('<div style="background-color:#1a4da1; padding:8px; text-align:center; font-weight:bold; border:2px solid white; border-bottom:none;">برنامج اليوم الدراسي</div>', unsafe_allow_html=True)
        st.markdown("""
            <table style="width:100%; border-collapse:collapse; color:white; border:1px solid white; text-align:center; font-size:0.9rem;">
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
        
    with col_center:
        # العداد التفاعلي (يستخدم وقت المتصفح للمزامنة)
        st.components.v1.html("""
            <div style="text-align: center; color: white; font-family: 'Cairo', sans-serif; direction: rtl;">
                <div style="border: 3px solid white; background-color: #1a4da1; padding: 10px; border-radius: 8px; margin-bottom: 20px;">
                    <div style="font-size: 1.2rem;">الحصة الحالية</div>
                    <div style="font-size: 2.5rem; font-weight: bold;" id="session-name-js">...</div>
                </div>
                <div style="position: relative; width: 180px; height: 180px; margin: 0 auto;">
                    <svg viewBox="0 0 100 100" style="transform: rotate(-90deg); width: 100%; height: 100%;">
                        <circle cx="50" cy="50" r="45" fill="none" stroke="rgba(255,255,255,0.2)" stroke-width="8"></circle>
                        <circle id="progress-js" cx="50" cy="50" r="45" fill="none" stroke="white" stroke-width="8" stroke-dasharray="283" stroke-dashoffset="283"></circle>
                    </svg>
                    <div style="position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%) rotate(0deg);">
                        <div style="font-size: 3.5rem; font-weight: bold;" id="timer-js">00</div>
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
                function update() {
                    const now = new Date();
                    const cur = now.getHours().toString().padStart(2,'0') + ":" + now.getMinutes().toString().padStart(2,'0');
                    let active = sch.find(s => cur >= s.s && cur < s.e);
                    if(active) {
                        document.getElementById('session-name-js').innerText = active.n;
                        const [eh, em] = active.e.split(':').map(Number);
                        const endD = new Date(); endD.setHours(eh, em, 0);
                        document.getElementById('timer-js').innerText = Math.ceil((endD - now)/60000);
                        const [sh, sm] = active.s.split(':').map(Number);
                        const startD = new Date(); startD.setHours(sh, sm, 0);
                        const offset = 283 - ((now - startD)/(endD - startD) * 283);
                        document.getElementById('progress-js').style.strokeDashoffset = offset;
                    } else {
                        document.getElementById('session-name-js').innerText = "استراحة / خارج الدوام";
                        document.getElementById('timer-js').innerText = "00";
                    }
                }
                setInterval(update, 1000); update();
            </script>
        """, height=350)
        st.markdown(f'<div style="text-align:center; font-weight:bold; line-height:1.8;">مدير المدرسة الأستاذ: هيثم بن حمد الغافري<br>المدير المساعد الأستاذ: توفيق بن سعيد اليعقوبي</div>', unsafe_allow_html=True)
        
    with col_left:
        st.markdown("""
            <div style="background-color:rgba(26, 77, 161, 0.2); border:2px solid white; padding:15px; margin-bottom:10px; text-align:center;">
                <h3 style="color:#b8d000; margin:0;">رؤية المدرسة</h3>
                <p style="font-weight:bold;">نحو مدرسةٍ رائدةٍ بأداءٍ متميزٍ وشراكةٍ مجتمعيةٍ فاعلةٍ</p>
            </div>
            <div style="background-color:rgba(26, 77, 161, 0.2); border:2px solid white; padding:15px; text-align:center;">
                <h3 style="color:#b8d000; margin:0;">رسالة المدرسة</h3>
                <p style="font-size:0.85rem;">نسعى إلى توفير بيئة تعليمية محفزة تحقق التميز في الأداء التعليمي...</p>
            </div>
        """, unsafe_allow_html=True)
        if st.button("الجدول العام للمعلمين", use_container_width=True):
            st.image("جدول.png")

with tab2:
    st.markdown(f'<h3 style="text-align:center; color:#b8d000; margin-bottom:20px;">حصص المعلمين - {current_day_name} | الحصة {current_session_name if current_session_name else "---"}</h3>', unsafe_allow_html=True)
    
    if all_data and current_day_name in all_data:
        day_data = all_data[current_day_name]
        cols = st.columns(4)
        for i, row in enumerate(day_data):
            with cols[i % 4]:
                teacher_info = row.get(current_session_name, "---") if current_session_name else "---"
                st.markdown(f"""
                    <table class="live-grade-table">
                        <tr>
                            <td class="class-name-cell">{row["الصف"]}</td>
                            <td class="teacher-live-cell">{teacher_info}</td>
                        </tr>
                    </table>
                """, unsafe_allow_html=True)
    else:
        st.warning(f"لا توجد بيانات ليوم {current_day_name} أو اليوم عطلة.")

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
        وَقُلِ اعْمَلُوا فَسَيَرَى اللَّهُ عَمَلَكُمْ وَرَسُولُهُ وَالْمُؤْمِنُونَ ... مدرسة عمر بن مسعود للتعليم الأساسي ترحب بكم
    </div></div>
    """, unsafe_allow_html=True)

# إعادة التشغيل كل دقيقة لمزامنة الحصة الحالية
time.sleep(60)
st.rerun()
