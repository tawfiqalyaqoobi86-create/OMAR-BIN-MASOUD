import streamlit as st
import pandas as pd
import datetime

# إعداد الصفحة
st.set_page_config(page_title="لوحة المدرسة - Streamlit", layout="wide", initial_sidebar_state="collapsed")

# CSS مخصص لتحسين المظهر
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700&family=Tajawal:wght@400;700&display=swap');
    
    html, body, [data-testid="stAppViewContainer"] {
        font-family: 'Tajawal', sans-serif;
        direction: rtl;
        text-align: right;
    }
    
    .main-header {
        background-color: #1a4da1;
        color: white;
        padding: 20px;
        border-radius: 10px;
        text-align: center;
        margin-bottom: 20px;
    }
    
    .status-card {
        background-color: #f0f2f6;
        padding: 20px;
        border-radius: 10px;
        border-right: 5px solid #1a4da1;
        margin-bottom: 10px;
    }
    
    .session-table th {
        background-color: #1a4da1 !important;
        color: white !important;
    }
    </style>
    """, unsafe_allow_html=True)

# الرأس
st.markdown('<div class="main-header"><h1>مدرسة عمر بن مسعود للتعليم الأساسي</h1></div>', unsafe_allow_html=True)

# التبويبات
tab1, tab2, tab3 = st.tabs(["اللوحة العامة", "جداول الفصول", "المناوبة"])

with tab1:
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.subheader("برنامج اليوم الدراسي")
        schedule_data = {
            "الحصة": ["الطابور", "الأولى", "الثانية", "الثالثة", "الرابعة", "الفسحة", "الخامسة", "السادسة", "السابعة", "الثامنة"],
            "الزمن": [15, 40, 40, 40, 40, 25, 40, 40, 40, 40],
            "من": ["07:10", "07:25", "08:10", "08:55", "09:40", "10:20", "10:45", "11:30", "12:15", "13:00"],
            "إلى": ["07:25", "08:05", "08:50", "09:35", "10:20", "10:45", "11:25", "12:10", "12:55", "13:40"]
        }
        st.table(pd.DataFrame(schedule_data))
        
    with col2:
        st.info("رؤية المدرسة : نحو مدرسةٍ رائدةٍ بأداءٍ متميزٍ وشراكةٍ مجتمعيةٍ فاعلةٍ")
        st.success("رسالة المدرسة: نسعى إلى توفير بيئة تعليمية محفزة تحقق التميز في الأداء التعليمي...")
        
        # عرض الوقت الحالي
        now = datetime.datetime.now()
        st.metric("التاريخ", now.strftime("%Y-%m-%d"))
        st.metric("الوقت", now.strftime("%H:%M:%S"))

with tab2:
    st.subheader("جداول الفصول الدراسية")
    import json
    try:
        with open('weekly_data.json', 'r', encoding='utf-8') as f:
            all_data = json.load(f)
        
        day = st.selectbox("اختر اليوم", list(all_data.keys()))
        class_list = [row['الصف'] for row in all_data[day]]
        selected_class = st.selectbox("اختر الصف", class_list)
        
        # تصفية البيانات حسب الصف
        class_data = [row for row in all_data[day] if row['الصف'] == selected_class]
        if class_data:
            df_class = pd.DataFrame(class_data).transpose()
            df_class.columns = ["التفاصيل"]
            st.table(df_class)
    except Exception as e:
        st.error(f"حدث خطأ في تحميل البيانات: {e}")

with tab3:
    st.subheader("جدول المناوبة")
    st.write("بيانات المناوبة اليومية")
    # عرض صورة الجدول العام إذا كانت موجودة
    try:
        st.image("جدول.png", caption="الجدول العام للمعلمين")
    except:
        st.error("لم يتم العثور على ملف الصورة جدول.png")

st.divider()
st.markdown('<p style="text-align:center;">وَقُلِ اعْمَلُوا فَسَيَرَى اللَّهُ عَمَلَكُمْ وَرَسُولُهُ وَالْمُؤْمِنُونَ</p>', unsafe_allow_html=True)
