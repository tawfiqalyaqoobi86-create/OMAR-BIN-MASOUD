import streamlit as st
import pandas as pd
import datetime
import json
import time

# إعداد الصفحة
st.set_page_config(page_title="لوحة مدرسة عمر بن مسعود الحية", layout="wide", initial_sidebar_state="collapsed")

# البيانات الثابتة للجدول الزمني
SCHEDULE_TIMES = [
    {"name": "الطابور", "start": "07:30", "end": "07:40"},
    {"name": "الأولى", "start": "07:40", "end": "08:15"},
    {"name": "الثانية", "start": "08:15", "end": "08:50"},
    {"name": "الثالثة", "start": "08:50", "end": "09:25"},
    {"name": "الرابعة", "start": "09:25", "end": "10:00"},
    {"name": "الفسحة", "start": "10:00", "end": "10:10"},
    {"name": "الخامسة", "start": "10:10", "end": "10:45"},
    {"name": "السادسة", "start": "10:45", "end": "11:20"},
    {"name": "السابعة", "start": "11:20", "end": "11:55"},
    {"name": "الثامنة", "start": "11:55", "end": "12:30"},
]

# تحميل البيانات
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

# CSS لإصلاح التصميم والتذييل
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
    
    .grade-group-box { border: 2px solid #1a4da1; margin-bottom: 15px; background-color: rgba(0,0,0,0.2); border-radius: 5px; overflow: hidden; }
    .grade-header { background-color: #1a4da1; color: white; text-align: center; font-weight: bold; padding: 5px; font-size: 1.1rem; border-bottom: 1px solid white; }
    .class-row-table { width: 100%; border-collapse: collapse; background-color: white; table-layout: fixed; }
    .class-row-table td { border: 1px solid #1a4da1; padding: 10px 5px; font-weight: bold; text-align: center; height: 55px; vertical-align: middle; }
    .class-label-cell { background-color: #1a4da1; color: white !important; width: 35%; font-size: 1rem; }
    .teacher-name-cell { background-color: white; color: #1a4da1 !important; width: 65%; font-size: 0.95rem; }
    
    .ticker-container {
        position: fixed; bottom: 0; left: 0; width: 100%;
        background-color: #1a4da1; border-top: 2px solid white;
        padding: 10px 0; z-index: 9999; overflow: hidden;
    }
    .ticker-move {
        display: inline-block; white-space: nowrap; padding-right: 100%;
        animation: ticker 40s linear infinite; font-weight: bold; font-size: 1.2rem; color: white;
    }
    @keyframes ticker { 0% { transform: translateX(-100%); } 100% { transform: translateX(100%); } }
    
    .stTabs [data-baseweb="tab-list"] { background-color: #0b1a32; border: 2px solid white; padding: 5px; }
    .stTabs [data-baseweb="tab"] { color: white !important; font-weight: bold; }
    .stTabs [aria-selected="true"] { background-color: #1a4da1 !important; }
    </style>
    """, unsafe_allow_html=True)

# الجزء العلوي: الساعة الحية
st.components.v1.html("""
    <div style="display: flex; justify-content: space-between; align-items: center; background-color: #0b1a32; padding: 5px 15px; border: 2px solid white; color: white; font-family: 'Cairo', sans-serif; direction: rtl;">
        <div style="display: flex; align-items: center;">
            <img src="logo.png.png" style="height: 50px; margin-left: 20px;" alt="Logo">
            <div style="background-color: transparent; border: none; padding: 2px 15px; font-size: 2rem; font-weight: bold;" id="js-day">...</div>
        </div>
        <div style="display: flex; justify-content: space-between; align-items: center; flex-grow: 1; margin: 0 20px;">
            <div style="font-size: 1.1rem;">11 رمضان 1447</div>
            <div style="font-size: 2rem; font-weight: bold; text-shadow: 0 0 10px white;" id="js-clock">00:00:00</div>
            <div style="font-size: 1.1rem;" id="js-date">...</div>
        </div>
    </div>
    <script>
        function update() {
            const now = new Date();
            const days = ["الأحد", "الإثنين", "الثلاثاء", "الأربعاء", "الخميس", "الجمعة", "السبت"];
            document.getElementById('js-day').innerText = days[now.getDay()];
            document.getElementById('js-clock').innerText = now.toLocaleTimeString('en-GB');
            document.getElementById('js-date').innerText = now.getDate() + "-" + (now.getMonth()+1) + "-" + now.getFullYear();
        }
        setInterval(update, 1000); update();
    </script>
    """, height=100)

tab1, tab2, tab3 = st.tabs(["اللوحة العامة", "جداول الفصول الحالية", "المناوبة"])

with tab1:
    col1, col2, col3 = st.columns([1, 1.2, 1])
    with col1:
        st.markdown('<div style="background-color:#1a4da1; padding:5px; text-align:center; font-weight:bold; border-radius: 8px 8px 0 0; box-shadow: 0 4px 12px rgba(0, 0, 0, 0.5);">برنامج اليوم الدراسي</div>', unsafe_allow_html=True)
        st.markdown('<table style="width:100%; text-align:center; border:none; border-collapse:collapse; font-size:0.8rem; background:white; color:black; box-shadow: 0 4px 12px rgba(0, 0, 0, 0.5); border-radius: 0 0 8px 8px; overflow: hidden;"><tr><th style="background:#1a4da1; color:white;">الحصة</th><th style="background:#1a4da1; color:white;">من</th><th style="background:#1a4da1; color:white;">إلى</th></tr><tr><td>الطابور</td><td>07:30</td><td>07:40</td></tr><tr><td>الأولى</td><td>07:40</td><td>08:15</td></tr><tr><td>الثانية</td><td>08:15</td><td>08:50</td></tr><tr><td>الثالثة</td><td>08:50</td><td>09:25</td></tr><tr><td>الرابعة</td><td>09:25</td><td>10:00</td></tr><tr><td>الفسحة</td><td>10:00</td><td>10:10</td></tr><tr><td>الخامسة</td><td>10:10</td><td>10:45</td></tr><tr><td>السادسة</td><td>10:45</td><td>11:20</td></tr><tr><td>السابعة</td><td>11:20</td><td>11:55</td></tr><tr><td>الثامنة</td><td>11:55</td><td>12:30</td></tr></table>', unsafe_allow_html=True)
    with col2:
        st.components.v1.html("""
            <div style="text-align: center; color: white; font-family: 'Cairo', sans-serif; direction: rtl;">
                <div style="background-color: #1a4da1; padding: 10px; border-radius: 8px; margin-bottom: 20px; box-shadow: 0 4px 12px rgba(0, 0, 0, 0.5);">
                    <div style="font-size: 1.2rem;">الحصة الحالية</div>
                    <div style="font-size: 2.5rem; font-weight: bold;" id="cur-sess">...</div>
                </div>
                <div style="position: relative; width: 180px; height: 180px; margin: 0 auto;">
                    <svg viewBox="0 0 100 100" style="transform: rotate(-90deg); width: 100%; height: 100%;">
                        <circle cx="50" cy="50" r="45" fill="none" stroke="rgba(255,255,255,0.2)" stroke-width="8"></circle>
                        <circle id="p-circle" cx="50" cy="50" r="45" fill="none" stroke="white" stroke-width="8" stroke-dasharray="283" stroke-dashoffset="283" style="transition: stroke-dashoffset 1s linear;"></circle>
                    </svg>
                    <div style="position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%) rotate(0deg);">
                        <div style="font-size: 3.5rem; font-weight: bold;" id="timer-val">00</div>
                        <div style="font-size: 1.1rem; font-weight: bold;">دقيقة</div>
                    </div>
                </div>
                <div style="margin-top:20px; font-weight:bold;">هيثم الغافري | توفيق اليعقوبي</div>
            </div>
            <script>
                const schedule = [
                    {n:"الطابور", s:"07:30", e:"07:40"}, {n:"الأولى", s:"07:40", e:"08:15"},
                    {n:"الثانية", s:"08:15", e:"08:50"}, {n:"الثالثة", s:"08:50", e:"09:25"},
                    {n:"الرابعة", s:"09:25", e:"10:00"}, {n:"الفسحة", s:"10:00", e:"10:10"},
                    {n:"الخامسة", s:"10:10", e:"10:45"}, {n:"السادسة", s:"10:45", e:"11:20"},
                    {n:"السابعة", s:"11:20", e:"11:55"}, {n:"الثامنة", s:"11:55", e:"12:30"}
                ];
                function updateTimer() {
                    const now = new Date();
                    const curTime = now.getHours().toString().padStart(2,'0') + ":" + now.getMinutes().toString().padStart(2,'0');
                    let active = schedule.find(s => curTime >= s.s && curTime < s.e);
                    
                    if(active) {
                        document.getElementById('cur-sess').innerText = active.n;
                        const [eh, em] = active.e.split(':').map(Number);
                        const ed = new Date(); ed.setHours(eh, em, 0);
                        const diffMins = Math.ceil((ed - now)/60000);
                        document.getElementById('timer-val').innerText = diffMins > 0 ? diffMins : "00";
                        
                        const [sh, sm] = active.s.split(':').map(Number);
                        const sd = new Date(); sd.setHours(sh, sm, 0);
                        const offset = 283 - (((now - sd)/(ed - sd)) * 283);
                        document.getElementById('p-circle').style.strokeDashoffset = Math.max(0, Math.min(283, offset));
                    } else {
                        document.getElementById('cur-sess').innerText = "فترة استراحة";
                        document.getElementById('timer-val').innerText = "00";
                        document.getElementById('p-circle').style.strokeDashoffset = 283;
                    }
                }
                setInterval(updateTimer, 1000); updateTimer();
            </script>
        """, height=380)
    with col3:
        st.markdown('<div style="background-color:rgba(26, 77, 161, 0.3); border:2px solid white; padding:15px; text-align:center;">رؤية المدرسة : نحو مدرسةٍ رائدةٍ بأداءٍ متميزٍ</div>', unsafe_allow_html=True)
        if st.button("الجدول العام للمعلمين", use_container_width=True):
            st.image("جدول.png")

with tab2:
    sessions_list = [s["name"] for s in SCHEDULE_TIMES]
    now_py = datetime.datetime.now()
    cur_time_py = now_py.strftime("%H:%M")
    
    auto_idx = 0
    for i, s in enumerate(SCHEDULE_TIMES):
        if s["start"] <= cur_time_py < s["end"]:
            auto_idx = i + 1
            break
            
    chosen_session = st.selectbox("اختر الحصة لعرض المعلمين", ["تلقائي"] + sessions_list, index=0)
    final_session = sessions_list[auto_idx-1] if (chosen_session == "تلقائي" and auto_idx > 0) else (None if chosen_session == "تلقائي" else chosen_session)

    current_day = {0: "الإثنين", 1: "الثلاثاء", 2: "الأربعاء", 3: "الخميس", 6: "الأحد"}.get(now_py.weekday(), "الأحد")
    st.markdown(f'<h2 style="text-align:center; color:#ffffff;">المعلمين المتواجدين في الحصة {final_session if final_session else "---"}</h2>', unsafe_allow_html=True)
    
    day_data = all_data.get(current_day) or all_data.get(current_day.replace("إ", "ا"))
    
    if day_data and final_session and final_session not in ["الفسحة", "الطابور"]:
        grades = ["الخامس", "السادس", "السابع", "الثامن", "التاسع", "العاشر", "الحادي عشر", "الثاني عشر"]
        grid_cols = st.columns(4)
        for idx, g_name in enumerate(grades):
            with grid_cols[idx % 4]:
                st.markdown(f'<div class="grade-group-box"><div class="grade-header">الصف {g_name}</div>', unsafe_allow_html=True)
                for row in day_data:
                    c_code = row.get("الصف", "")
                    # منطق توزيع الصفوف
                    is_match = False
                    if idx < 6: # من الخامس للعاشر
                        if f"{idx+5}/" in c_code: is_match = True
                    elif g_name == "الحادي عشر" and "11/" in c_code: is_match = True
                    elif g_name == "الثاني عشر" and "12/" in c_code: is_match = True
                    
                    if is_match:
                        teacher = row.get(final_session, "")
                        st.markdown(f"""<table class="class-row-table"><tr><td class="class-label-cell">{CLASS_MAP.get(c_code, c_code)}</td><td class="teacher-name-cell">{teacher}</td></tr></table>""", unsafe_allow_html=True)
                st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.warning("لا توجد حصص حالياً أو الحصة المختارة هي فترة استراحة.")

st.markdown('<div class="ticker-container"><div class="ticker-move">مدرسة عمر بن مسعود للتعليم الأساسي ترحب بكم ... نتمنى لطلابنا يوماً دراسياً موفقاً ومليئاً بالنجاح والتميز ...</div></div>', unsafe_allow_html=True)

time.sleep(60)
st.rerun()
