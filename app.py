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

# CSS مخصص لمحاكاة التصميم الأصلي بدقة
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

    /* إخفاء عناصر Streamlit غير الضرورية */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}

    .stTabs [data-baseweb="tab-list"] {
        background-color: #0b1a32;
        border: 2px solid white;
        margin-bottom: 10px;
        padding: 5px;
    }

    .stTabs [data-baseweb="tab"] {
        color: white !important;
        font-weight: bold;
    }

    .stTabs [aria-selected="true"] {
        background-color: #1a4da1 !important;
    }

    /* تصميم مخصص للساعة والبيانات الحية */
    .header-container {
        display: flex;
        justify-content: space-between;
        align-items: center;
        background-color: #0b1a32;
        padding: 10px 15px;
        border: 2px solid white;
        margin-bottom: 15px;
    }

    .live-time-box {
        font-size: 3rem;
        font-weight: bold;
        color: white;
        text-shadow: 0 0 10px rgba(255,255,255,0.5);
    }

    .day-box {
        background-color: #1a4da1;
        border: 2px solid white;
        padding: 10px 30px;
        font-size: 1.8rem;
        font-weight: bold;
    }

    .session-card {
        border: 3px solid white;
        background-color: #1a4da1;
        padding: 15px;
        text-align: center;
        border-radius: 8px;
    }

    .circular-timer-container {
        position: relative;
        width: 200px;
        height: 200px;
        margin: 0 auto;
    }

    .vision-box {
        background-color: rgba(26, 77, 161, 0.4);
        border: 2px solid white;
        padding: 15px;
        margin-bottom: 15px;
    }

    .ticker-footer {
        background-color: #0b1a32;
        border-top: 2px solid white;
        padding: 10px;
        position: fixed;
        bottom: 0;
        left: 0;
        right: 0;
        z-index: 1000;
    }

    .ticker-text {
        display: inline-block;
        white-space: nowrap;
        animation: ticker 25s linear infinite;
        font-size: 1.2rem;
    }

    @keyframes ticker {
        0% { transform: translateX(-100%); }
        100% { transform: translateX(100%); }
    }
    </style>
    """, unsafe_allow_html=True)

# إضافة JavaScript للساعة التفاعلية والعداد
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
            document.getElementById('gregorian-date').innerText = now.toLocaleDateString('en-GB').replace(/\//g, '-');
        }}
        setInterval(updateClock, 1000);
        updateClock();
    </script>
    """, height=100)

tab1, tab2, tab3 = st.tabs(["اللوحة العامة", "جداول الفصول", "المناوبة"])

with tab1:
    col_right, col_center, col_left = st.columns([1, 1.2, 1])
    
    with col_right:
        st.markdown('<div style="background-color:#1a4da1; padding:8px; text-align:center; font-weight:bold; border:2px solid white;">برنامج اليوم الدراسي</div>', unsafe_allow_html=True)
        schedule_data = {
            "الحصة": ["الطابور", "الأولى", "الثانية", "الثالثة", "الرابعة", "الفسحة", "الخامسة", "السادسة", "السابعة", "الثامنة"],
            "من": ["07:10", "07:25", "08:10", "08:55", "09:40", "10:20", "10:45", "11:30", "12:15", "13:00"],
            "إلى": ["07:25", "08:05", "08:50", "09:35", "10:20", "10:45", "11:25", "12:10", "12:55", "13:40"]
        }
        st.table(pd.DataFrame(schedule_data))
        
    with col_center:
        # الحصة الحالية والعداد التفاعلي باستخدام JS
        st.components.v1.html("""
            <div style="text-align: center; color: white; font-family: 'Cairo', sans-serif; direction: rtl;">
                <div style="border: 3px solid white; background-color: #1a4da1; padding: 10px; border-radius: 8px; margin-bottom: 20px;">
                    <div style="font-size: 1.2rem;">الحصة الحالية</div>
                    <div style="font-size: 2.5rem; font-weight: bold;" id="current-session-name">جاري الحساب...</div>
                </div>
                
                <div style="position: relative; width: 180px; height: 180px; margin: 0 auto;">
                    <svg viewBox="0 0 100 100" style="transform: rotate(-90deg); width: 100%; height: 100%;">
                        <circle cx="50" cy="50" r="45" fill="none" stroke="rgba(255,255,255,0.2)" stroke-width="8"></circle>
                        <circle id="timer-progress" cx="50" cy="50" r="45" fill="none" stroke="white" stroke-width="8" 
                                stroke-dasharray="283" stroke-dashoffset="0" stroke-linecap="round" style="transition: stroke-dashoffset 1s linear;"></circle>
                    </svg>
                    <div style="position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%) rotate(0deg); text-align: center;">
                        <div style="font-size: 3rem; font-weight: bold;" id="timer-mins">00</div>
                        <div style="font-size: 1rem;">دقيقة</div>
                    </div>
                </div>
                
                <div style="margin-top: 30px; line-height: 1.8;">
                    <b>مدير المدرسة الأستاذ: هيثم بن حمد الغافري</b><br>
                    <b>المدير المساعد الأستاذ: توفيق بن سعيد اليعقوبي</b>
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
                    const currentTime = now.getHours().toString().padStart(2, '0') + ":" + now.getMinutes().toString().padStart(2, '0');
                    
                    let activeSession = null;
                    for (let s of schedule) {
                        if (currentTime >= s.start && currentTime < s.end) {
                            activeSession = s;
                            break;
                        }
                    }

                    if (activeSession) {
                        document.getElementById('current-session-name').innerText = activeSession.name;
                        const [endH, endM] = activeSession.end.split(':').map(Number);
                        const endDate = new Date(); endDate.setHours(endH, endM, 0);
                        const diffMs = endDate - now;
                        const diffMins = Math.ceil(diffMs / 60000);
                        
                        document.getElementById('timer-mins').innerText = diffMins;
                        
                        // تحديث الدائرة
                        const [startH, startM] = activeSession.start.split(':').map(Number);
                        const startDate = new Date(); startDate.setHours(startH, startM, 0);
                        const totalMs = endDate - startDate;
                        const progress = (diffMs / totalMs) * 283;
                        document.getElementById('timer-progress').style.strokeDashoffset = 283 - progress;
                    } else {
                        document.getElementById('current-session-name').innerText = "خارج الوقت الدراسي";
                        document.getElementById('timer-mins').innerText = "00";
                        document.getElementById('timer-progress').style.strokeDashoffset = 283;
                    }
                }
                setInterval(updateTimer, 1000);
                updateTimer();
            </script>
        """, height=400)
        
    with col_left:
        st.markdown("""
            <div class="vision-box">
                <h3 style="color:#b8d000; text-align:center; margin-bottom:10px;">رؤية المدرسة</h3>
                <p style="text-align:center; font-size:1.1rem; font-weight:bold;">نحو مدرسةٍ رائدةٍ بأداءٍ متميزٍ وشراكةٍ مجتمعيةٍ فاعلةٍ</p>
            </div>
            <div class="vision-box">
                <h3 style="color:#b8d000; text-align:center; margin-bottom:10px;">رسالة المدرسة</h3>
                <p style="text-align:center; font-size:0.9rem; line-height:1.5;">نسعى إلى توفير بيئة تعليمية محفزة تحقق التميز في الأداء التعليمي، من خلال تنمية قدرات الطلبة، وتمكين الكوادر التعليمية، وتطبيق أساليب تعليم حديثة...</p>
            </div>
        """, unsafe_allow_html=True)
        if st.button("الجدول العام للمعلمين", use_container_width=True):
            st.image("جدول.png")

with tab2:
    if all_data:
        days_ar = ["الأحد", "الإثنين", "الثلاثاء", "الأربعاء", "الخميس"]
        selected_day = st.selectbox("اختر اليوم لعرض الجداول", days_ar)
        
        if selected_day in all_data:
            day_data = all_data[selected_day]
            cols = st.columns(4)
            for i, row in enumerate(day_data):
                with cols[i % 4]:
                    st.markdown(f"""
                        <div style="background-color:#b8d000; color:black; text-align:center; font-weight:bold; padding:5px; border:1px solid white;">
                            الصف {row["الصف"]}
                        </div>
                    """, unsafe_allow_html=True)
                    # تحويل البيانات لعرضها بشكل جدول صغير
                    items = []
                    for k, v in row.items():
                        if k != "الصف":
                            items.append({"الحصة": k, "المعلم/المادة": v})
                    st.table(pd.DataFrame(items))
    else:
        st.error("لم يتم العثور على بيانات الجداول. تأكد من وجود ملف weekly_data.json")

with tab3:
    st.markdown("""
        <div style="display:flex; gap:20px; direction:rtl;">
            <div style="flex:2; border:2px solid white; padding:10px; background-color:rgba(0,0,0,0.3);">
                <table style="width:100%; text-align:center; border-collapse:collapse; color:white;">
                    <tr style="background-color:#1a4da1; border:1px solid white;">
                        <th style="padding:10px;">جناح الخامس</th><th style="padding:10px;">جناح السادس</th><th style="padding:10px;">جناح السابع</th><th style="padding:10px;">جناح الثامن</th>
                    </tr>
                    <tr style="border:1px solid white;">
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

# شريط الأخبار في الأسفل
st.markdown("""
    <div class="ticker-footer">
        <div class="ticker-text">
            وَقُلِ اعْمَلُوا فَسَيَرَى اللَّهُ عَمَلَكُمْ وَرَسُولُهُ وَالْمُؤْمِنُونَ ... مدرسة عمر بن مسعود للتعليم الأساسي ترحب بكم ... نتمنى لطلابنا الأعزاء يوماً دراسياً موفقاً ومليئاً بالنجاح والتميز ...
        </div>
    </div>
    """, unsafe_allow_html=True)
