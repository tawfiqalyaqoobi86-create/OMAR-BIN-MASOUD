import streamlit as st
import pandas as pd
import datetime
import json
import re

# إعداد الصفحة
st.set_page_config(page_title="لوحة مدرسة عمر بن مسعود", layout="wide", initial_sidebar_state="collapsed")

# CSS مخصص لمحاكاة التصميم الأصلي
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700&family=Tajawal:wght@400;700&display=swap');
    
    html, body, [data-testid="stAppViewContainer"], [data-testid="stHeader"] {
        font-family: 'Cairo', 'Tajawal', Tahoma, sans-serif;
        direction: rtl;
        text-align: right;
        background: radial-gradient(circle, #1a4da1 0%, #0b1a32 100%);
        color: white;
    }

    [data-testid="stHeader"] {
        background: transparent;
    }

    .stTabs [data-baseweb="tab-list"] {
        background-color: #0b1a32;
        border: 2px solid white;
        margin-bottom: 10px;
        padding: 5px;
    }

    .stTabs [data-baseweb="tab"] {
        color: white !important;
        font-weight: bold;
        background-color: transparent;
    }

    .stTabs [aria-selected="true"] {
        background-color: #1a4da1 !important;
    }

    /* الرأس */
    .custom-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        background-color: #0b1a32;
        padding: 10px 15px;
        border-bottom: 2px solid white;
        margin-bottom: 15px;
    }

    .time-section {
        border: 2px solid white;
        padding: 5px 20px;
        display: flex;
        justify-content: space-between;
        align-items: center;
        flex-grow: 1;
        margin-left: 15px;
    }

    .day-box {
        background-color: #1a4da1;
        border: 2px solid white;
        padding: 10px 30px;
        font-size: 1.5rem;
        font-weight: bold;
    }

    /* الجداول */
    .stTable {
        background-color: rgba(255,255,255,0.1);
        color: white;
    }
    
    table {
        color: white !important;
    }

    .session-card {
        border: 3px solid white;
        background-color: #1a4da1;
        padding: 15px;
        text-align: center;
        border-radius: 8px;
        margin-bottom: 20px;
    }

    .circular-timer-mock {
        width: 150px;
        height: 150px;
        border: 10px solid rgba(26, 77, 161, 0.4);
        border-top: 10px solid white;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 3rem;
        font-weight: bold;
        margin: 0 auto;
    }

    .vision-box {
        background-color: #0b1a32;
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
        text-align: center;
        white-space: nowrap;
        overflow: hidden;
    }

    .ticker-text {
        display: inline-block;
        animation: ticker 20s linear infinite;
    }

    @keyframes ticker {
        0% { transform: translateX(-100%); }
        100% { transform: translateX(100%); }
    }
    </style>
    """, unsafe_allow_html=True)

# استخراج البيانات الأساسية
now = datetime.datetime.now()
days_ar = ["الإثنين", "الثلاثاء", "الأربعاء", "الخميس", "الجمعة", "السبت", "الأحد"]
current_day_ar = days_ar[now.weekday()]

# الرأس المخصص
st.markdown(f"""
    <div class="custom-header">
        <div class="day-box">{current_day_ar}</div>
        <div class="time-section">
            <div style="font-size: 1.2rem;">3 رمضان 1447</div>
            <div style="font-size: 2.5rem; font-weight: bold;">{now.strftime("%H:%M:%S")}</div>
            <div style="font-size: 1.2rem;">{now.strftime("%d-%m-%Y")}</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

tab1, tab2, tab3 = st.tabs(["اللوحة العامة", "جداول الفصول", "المناوبة"])

with tab1:
    col_right, col_center, col_left = st.columns([1, 1.2, 1])
    
    with col_right:
        st.markdown('<div style="background-color:#1a4da1; padding:8px; text-align:center; font-weight:bold;">برنامج اليوم الدراسي</div>', unsafe_allow_html=True)
        schedule_data = {
            "الحصة": ["الطابور", "الأولى", "الثانية", "الثالثة", "الرابعة", "الفسحة", "الخامسة", "السادسة", "السابعة", "الثامنة"],
            "الزمن": [15, 40, 40, 40, 40, 25, 40, 40, 40, 40],
            "من": ["07:10", "07:25", "08:10", "08:55", "09:40", "10:20", "10:45", "11:30", "12:15", "13:00"],
            "إلى": ["07:25", "08:05", "08:50", "09:35", "10:20", "10:45", "11:25", "12:10", "12:55", "13:40"]
        }
        st.table(pd.DataFrame(schedule_data))
        
    with col_center:
        st.markdown('<div class="session-card"><div style="font-size:1.2rem;">الحصة الحالية</div><div style="font-size:2.5rem; font-weight:bold;">السادسة</div></div>', unsafe_allow_html=True)
        st.markdown('<div class="circular-timer-mock">12<div style="font-size:1rem; position:absolute; bottom:30px;">دقيقة</div></div>', unsafe_allow_html=True)
        st.markdown("""
            <div style="margin-top: 30px; text-align: center; line-height: 1.8;">
                <b>مدير المدرسة الأستاذ: هيثم بن حمد الغافري</b><br>
                <b>المدير المساعد الأستاذ: توفيق بن سعيد اليعقوبي</b>
            </div>
        """, unsafe_allow_html=True)
        
    with col_left:
        st.markdown("""
            <div class="vision-box">
                <h4 style="color:#b8d000; text-align:center;">رؤية المدرسة</h4>
                <p style="text-align:center; font-size:0.9rem;">نحو مدرسةٍ رائدةٍ بأداءٍ متميزٍ وشراكةٍ مجتمعيةٍ فاعلةٍ</p>
            </div>
            <div class="vision-box">
                <h4 style="color:#b8d000; text-align:center;">رسالة المدرسة</h4>
                <p style="text-align:center; font-size:0.8rem;">نسعى إلى توفير بيئة تعليمية محفزة تحقق التميز في الأداء التعليمي، من خلال تنمية قدرات الطلبة...</p>
            </div>
        """, unsafe_allow_html=True)
        if st.button("الجدول العام للمعلمين", use_container_width=True):
            st.image("جدول.png")

with tab2:
    try:
        with open('weekly_data.json', 'r', encoding='utf-8') as f:
            all_data = json.load(f)
        
        selected_day = st.selectbox("اختر اليوم", list(all_data.keys()), index=list(all_data.keys()).index(current_day_ar) if current_day_ar in all_data else 0)
        
        # عرض الجداول في شبكة (4 أعمدة)
        day_data = all_data[selected_day]
        cols = st.columns(4)
        for i, row in enumerate(day_data):
            with cols[i % 4]:
                st.markdown(f'<div style="background-color:#b8d000; color:black; text-align:center; font-weight:bold; padding:2px; margin-top:10px;">الصف {row["الصف"]}</div>', unsafe_allow_html=True)
                # تحويل الصف إلى DataFrame عمودي للعرض
                class_df = pd.DataFrame([row]).transpose().reset_index()
                class_df.columns = ["الحصة", "المادة/المعلم"]
                st.dataframe(class_df[class_df["الحصة"] != "الصف"], hide_index=True, use_container_width=True)
    except Exception as e:
        st.error(f"خطأ في تحميل البيانات: {e}")

with tab3:
    st.markdown("""
        <div style="display:flex; gap:10px;">
            <div style="flex:2; border:2px solid white; padding:10px;">
                <table style="width:100%; text-align:center; border-collapse:collapse;">
                    <tr style="background-color:#1a4da1;">
                        <th>جناح الخامس</th><th>جناح السادس</th><th>جناح السابع</th><th>جناح الثامن</th>
                    </tr>
                    <tr><td>-</td><td>-</td><td>-</td><td>-</td></tr>
                </table>
            </div>
            <div style="flex:1; background-color:#1a4da1; border:2px solid white; padding:15px; text-align:center;">
                <h4 style="margin:0;">المادة المناوبة</h4>
                <hr>
                <p>المادة: <span id="replacement-subject">اللغة العربية</span></p>
                <p>المعلم المشرف: <span id="supervising-teacher">محمد الشلع</span></p>
            </div>
        </div>
    """, unsafe_allow_html=True)

# التذييل (شريط الأخبار)
st.markdown("""
    <div class="ticker-footer">
        <div class="ticker-text">وَقُلِ اعْمَلُوا فَسَيَرَى اللَّهُ عَمَلَكُمْ وَرَسُولُهُ وَالْمُؤْمِنُونَ ... مدرسة عمر بن مسعود للتعليم الأساسي ترحب بكم</div>
    </div>
    """, unsafe_allow_html=True)
