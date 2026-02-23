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

# CSS مخصص لمحاكاة التصميم الأصلي بدقة متناهية
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700&family=Tajawal:wght@400;700&display=swap');
    
    html, body, [data-testid="stAppViewContainer"], [data-testid="stHeader"] {
        font-family: 'Cairo', 'Tajawal', Tahoma, sans-serif;
        direction: rtl;
        text-align: right;
        background: radial-gradient(circle, #1a4da1 0%, #0b1a32 100%) !important;
        color: white !important;
    }

    /* إخفاء عناصر Streamlit */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    [data-testid="stSidebar"] {display: none;}

    .stTabs [data-baseweb="tab-list"] {
        background-color: #0b1a32;
        border: 2px solid white;
        margin-bottom: 10px;
        padding: 5px;
    }

    .stTabs [data-baseweb="tab"] {
        color: white !important;
        font-weight: bold;
        font-size: 1.1em;
    }

    .stTabs [aria-selected="true"] {
        background-color: #1a4da1 !important;
    }

    /* تنسيق الجداول المخصص ليكون مثل الأصل */
    .custom-table {
        width: 100%;
        border-collapse: collapse;
        color: white;
        border: 2px solid white;
    }

    .custom-table th {
        background-color: #1a4da1;
        color: white;
        padding: 10px;
        border: 1px solid white;
        text-align: center;
    }

    .custom-table td {
        background-color: rgba(26, 77, 161, 0.1);
        color: white;
        padding: 8px;
        border: 1px solid white;
        text-align: center;
        font-weight: bold;
    }

    .custom-table tr:nth-child(even) td {
        background-color: rgba(26, 77, 161, 0.2);
    }

    .custom-table td:first-child {
        background-color: #1a4da1;
        color: white;
    }

    /* تنسيق زر الجدول العام */
    .stButton > button {
        background-color: #0b1a32 !important;
        color: white !important;
        border: 2px solid white !important;
        border-radius: 8px !important;
        padding: 15px 30px !important;
        font-weight: bold !important;
        font-size: 1.1rem !important;
        box-shadow: 0 4px 8px rgba(255, 255, 255, 0.4) !important;
        transition: all 0.3s ease !important;
        width: 100% !important;
    }

    .stButton > button:hover {
        background-color: #1a4da1 !important;
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 12px rgba(255, 255, 255, 0.6) !important;
    }

    /* تنسيق جداول الفصول في التبويب الثاني */
    .grade-table-container {
        background-color: white;
        color: #1a4da1;
        width: 100%;
        border-collapse: collapse;
        font-size: 0.85em;
    }

    .grade-table-container td {
        border: 1px solid #1a4da1;
        padding: 5px;
        font-weight: bold;
        text-align: center;
    }

    .class-id-cell {
        background-color: #1a4da1;
        color: white !important;
        width: 35%;
    }

    .teacher-name-cell {
        background-color: white;
        color: #1a4da1 !important;
    }

    .ticker-footer {
        background-color: #1a4da1;
        border: 1px solid white;
        padding: 8px;
        position: fixed;
        bottom: 5px;
        left: 10px;
        right: 10px;
        overflow: hidden;
        white-space: nowrap;
        z-index: 9999;
    }

    .ticker-text {
        display: inline-block;
        padding-left: 100%;
        animation: marquee 30s linear infinite;
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

# الساعة والبيانات الحية في الأعلى
st.components.v1.html(f"""
    <div style="display: flex; justify-content: space-between; align-items: center; background-color: #0b1a32; padding: 10px 15px; border: 2px solid white; color: white; font-family: 'Cairo', sans-serif; direction: rtl;">
        <div style="background-color: #1a4da1; border: 2px solid white; padding: 5px 25px; font-size: 1.5rem; font-weight: bold;" id="current-day"></div>
        <div style="display: flex; justify-content: space-between; align-items: center; flex-grow: 1; margin: 0 20px;">
            <div style="font-size: 1.1rem;" id="hijri-date">3 رمضان 1447</div>
            <div style="font-size: 2.8rem; font-weight: bold; text-shadow: 0 0 10px white;" id="live-clock">00:00:00</div>
            <div style="font-size: 1.1rem;" id="gregorian-date"></div>
        </div>
    </div>
    <script>
        function updateClock() {{
            const now = new Date();
            const days = ["الأحد", "الإثنين", "الثلاثاء", "الأربعاء", "الخميس", "الجمعة", "السبت"];
            document.getElementById('current-day').innerText = days[now.getDay()];
            document.getElementById('live-clock').innerText = now.toLocaleTimeString('en-GB');
            const d = now.getDate(); const m = now.getMonth() + 1; const y = now.getFullYear();
            document.getElementById('gregorian-date').innerText = d + "-" + m + "-" + y;
        }}
        setInterval(updateClock, 1000);
        updateClock();
    </script>
    """, height=100)

tab1, tab2, tab3 = st.tabs(["اللوحة العامة", "جداول الفصول", "المناوبة"])

with tab1:
    col_right, col_center, col_left = st.columns([1, 1.2, 1])
    
    with col_right:
        st.markdown('<div style="background-color:#1a4da1; padding:8px; text-align:center; font-weight:bold; border:2px solid white; border-bottom:none;">برنامج اليوم الدراسي</div>', unsafe_allow_html=True)
        html_schedule = """
        <table class="custom-table">
            <thead>
                <tr><th>الحصة</th><th>الزمن</th><th>من</th><th>إلى</th></tr>
            </thead>
            <tbody>
                <tr><td>الطابور</td><td>15</td><td>07:10</td><td>07:25</td></tr>
                <tr><td>الأولى</td><td>40</td><td>07:25</td><td>08:05</td></tr>
                <tr><td>الثانية</td><td>40</td><td>08:10</td><td>08:50</td></tr>
                <tr><td>الثالثة</td><td>40</td><td>08:55</td><td>09:35</td></tr>
                <tr><td>الرابعة</td><td>40</td><td>09:40</td><td>10:20</td></tr>
                <tr><td>الفسحة</td><td>25</td><td>10:20</td><td>10:45</td></tr>
                <tr><td>الخامسة</td><td>40</td><td>10:45</td><td>11:25</td></tr>
                <tr><td>السادسة</td><td>40</td><td>11:30</td><td>12:10</td></tr>
                <tr><td>السابعة</td><td>40</td><td>12:15</td><td>12:55</td></tr>
                <tr><td>الثامنة</td><td>40</td><td>13:00</td><td>13:40</td></tr>
            </tbody>
        </table>
        """
        st.markdown(html_schedule, unsafe_allow_html=True)
        
    with col_center:
        st.components.v1.html("""
            <div style="text-align: center; color: white; font-family: 'Cairo', sans-serif; direction: rtl;">
                <div style="border: 3px solid white; background-color: #1a4da1; padding: 10px; border-radius: 8px; margin-bottom: 20px;">
                    <div style="font-size: 1.2rem;">الحصة الحالية</div>
                    <div style="font-size: 2.5rem; font-weight: bold;" id="current-session-name">...</div>
                </div>
                <div style="position: relative; width: 180px; height: 180px; margin: 0 auto;">
                    <svg viewBox="0 0 100 100" style="transform: rotate(-90deg); width: 100%; height: 100%;">
                        <circle cx="50" cy="50" r="45" fill="none" stroke="rgba(255,255,255,0.2)" stroke-width="8"></circle>
                        <circle id="timer-progress" cx="50" cy="50" r="45" fill="none" stroke="white" stroke-width="8" 
                                stroke-dasharray="283" stroke-dashoffset="0" stroke-linecap="round" style="transition: stroke-dashoffset 1s linear;"></circle>
                    </svg>
                    <div style="position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%) rotate(0deg); text-align: center;">
                        <div style="font-size: 3.5rem; font-weight: bold;" id="timer-mins">00</div>
                        <div style="font-size: 1.2rem; font-weight: bold;">دقيقة</div>
                    </div>
                </div>
                <div style="margin-top: 30px; line-height: 1.8;">
                    <p style="margin:2px;">مدير المدرسة الأستاذ: <b>هيثم بن حمد الغافري</b></p>
                    <p style="margin:2px;">المدير المساعد الأستاذ: <b>توفيق بن سعيد اليعقوبي</b></p>
                </div>
            </div>
            <script>
                const schedule = [
                    { name: "الطابور", start: "07:10", end: "07:25" },
                    { name: "الأولى", start: "07:25", end: "08:05" },
                    { name: "الثانية", start: "08:10", end: "08:50" },
                    { name: "الثالثة", start: "08:55", end: "09:35" },
                    { name: "الرابعة", start: "09:40", end: "10:20" },
                    { name: "الفسحة", start: "10:20", end: "10:45" },
                    { name: "الخامسة", start: "10:45", end: "11:25" },
                    { name: "السادسة", start: "11:30", end: "12:10" },
                    { name: "السابعة", start: "12:15", end: "12:55" },
                    { name: "الثامنة", start: "13:00", end: "13:40" }
                ];
                function updateTimer() {
                    const now = new Date();
                    const hh = now.getHours().toString().padStart(2, '0');
                    const mm = now.getMinutes().toString().padStart(2, '0');
                    const currentTime = hh + ":" + mm;
                    let active = null;
                    for (let s of schedule) { if (currentTime >= s.start && currentTime < s.end) { active = s; break; } }
                    if (active) {
                        document.getElementById('current-session-name').innerText = active.name;
                        const [eh, em] = active.end.split(':').map(Number);
                        const endD = new Date(); endD.setHours(eh, em, 0);
                        const diff = Math.ceil((endD - now) / 60000);
                        document.getElementById('timer-mins').innerText = diff;
                        const [sh, sm] = active.start.split(':').map(Number);
                        const startD = new Date(); startD.setHours(sh, sm, 0);
                        const progress = ((now - startD) / (endD - startD)) * 283;
                        document.getElementById('timer-progress').style.strokeDashoffset = progress;
                    } else {
                        document.getElementById('current-session-name').innerText = "خارج الدوام";
                        document.getElementById('timer-mins').innerText = "00";
                        document.getElementById('timer-progress').style.strokeDashoffset = 283;
                    }
                }
                setInterval(updateTimer, 1000); updateTimer();
            </script>
        """, height=400)
        
    with col_left:
        st.markdown("""
            <div style="background-color:rgba(26, 77, 161, 0.2); border:2px solid white; padding:15px; margin-bottom:15px; text-align:center;">
                <h3 style="color:#b8d000; margin-top:0;">رؤية المدرسة</h3>
                <p style="font-weight:bold; font-size:1.1rem;">نحو مدرسةٍ رائدةٍ بأداءٍ متميزٍ وشراكةٍ مجتمعيةٍ فاعلةٍ</p>
            </div>
            <div style="background-color:rgba(26, 77, 161, 0.2); border:2px solid white; padding:15px; margin-bottom:15px; text-align:center;">
                <h3 style="color:#b8d000; margin-top:0;">رسالة المدرسة</h3>
                <p style="font-size:0.9rem; line-height:1.5;">نسعى إلى توفير بيئة تعليمية محفزة تحقق التميز في الأداء التعليمي، من خلال تنمية قدرات الطلبة، وتمكين الكوادر التعليمية...</p>
            </div>
        """, unsafe_allow_html=True)
        if st.button("الجدول العام للمعلمين"):
            st.image("جدول.png")

with tab2:
    if all_data:
        days_list = ["الأحد", "الإثنين", "الثلاثاء", "الأربعاء", "الخميس"]
        sel_day = st.selectbox("اختر اليوم", days_list)
        if sel_day in all_data:
            day_rows = all_data[sel_day]
            cols = st.columns(4)
            for i, row in enumerate(day_rows):
                with cols[i % 4]:
                    st.markdown(f"""
                        <div style="background-color:#b8d000; color:black; text-align:center; font-weight:bold; padding:3px; border:1px solid white;">
                            الصف {row["الصف"]}
                        </div>
                        <table class="grade-table-container">
                    """, unsafe_allow_html=True)
                    for k, v in row.items():
                        if k != "الصف":
                            st.markdown(f"""
                                <tr>
                                    <td class="class-id-cell">{k}</td>
                                    <td class="teacher-name-cell">{v}</td>
                                </tr>
                            """, unsafe_allow_html=True)
                    st.markdown("</table><br>", unsafe_allow_html=True)
    else:
        st.error("بيانات الجداول غير متوفرة.")

with tab3:
    st.markdown("""
        <div style="display:flex; gap:20px; direction:rtl;">
            <div style="flex:2; border:2px solid white; padding:10px; background-color:rgba(0,0,0,0.3);">
                <table style="width:100%; text-align:center; border-collapse:collapse; color:white;">
                    <tr style="background-color:#b8d000; color:black; border:1px solid white;">
                        <th style="padding:10px;">جناح الخامس</th><th style="padding:10px;">جناح السادس</th><th style="padding:10px;">جناح السابع</th><th style="padding:10px;">جناح الثامن</th>
                    </tr>
                    <tr style="border:1px solid white; background-color:white; color:#1a4da1; font-weight:bold;">
                        <td style="padding:15px;">-</td><td style="padding:15px;">-</td><td style="padding:15px;">-</td><td style="padding:15px;">-</td>
                    </tr>
                </table>
            </div>
            <div style="flex:1; background-color:#1a4da1; border:3px solid white; padding:20px; text-align:center; border-radius:10px;">
                <h3 style="margin:0; color:#b8d000;">المادة المناوبة</h3>
                <hr style="border:1px solid white;">
                <p style="font-size:1.3rem;">المادة: <b>اللغة العربية</b></p>
                <p style="font-size:1.3rem;">المعلم المشرف: <b>محمد الشلع</b></p>
            </div>
        </div>
    """, unsafe_allow_html=True)

# تذييل الصفحة المتحرك
st.markdown("""
    <div class="ticker-footer">
        <div class="ticker-text">
            وَقُلِ اعْمَلُوا فَسَيَرَى اللَّهُ عَمَلَكُمْ وَرَسُولُهُ وَالْمُؤْمِنُونَ ... مدرسة عمر بن مسعود للتعليم الأساسي ترحب بكم ... نتمنى لطلابنا الأعزاء يوماً دراسياً موفقاً ومليئاً بالنجاح والتميز ...
        </div>
    </div>
    """, unsafe_allow_html=True)
