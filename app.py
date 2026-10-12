import streamlit as st
import pandas as pd
import plotly.express as px

# 1. ตั้งค่าการแสดงผลของหน้าเว็บ
st.set_page_config(
    page_title="Thailand Red List - สถานภาพสัตว์ป่า",
    page_icon="🐾",
    layout="wide"
)

st.title("🐾 ระบบรายงานสถานภาพชนิดพันธุ์สัตว์ที่ถูกคุกคามในประเทศไทย")
st.caption("พัฒนาด้วย Streamlit, Pandas และ Plotly (อ้างอิงข้อมูลจาก data.go.th)")

# 2. ฟังก์ชันโหลดข้อมูล
@st.cache_data
def load_data():
    df = pd.read_csv("data.csv")
    return df

try:
    df = load_data()

    # 3. Interactive Widgets ใน Sidebar
    st.sidebar.header("🔍 ตัวกรองข้อมูล (Interactive Widgets)")

    animal_groups = ["ทั้งหมด"] + list(df['กลุ่มสัตว์'].dropna().unique())
    selected_group = st.sidebar.selectbox("เลือกกลุ่มสัตว์:", animal_groups)

    status_list = ["ทั้งหมด"] + list(df['สถานภาพของชนิดพันธุ์'].dropna().unique())
    selected_status = st.sidebar.selectbox("เลือกสถานภาพ:", status_list)

    filtered_df = df.copy()
    if selected_group != "ทั้งหมด":
        filtered_df = filtered_df[filtered_df['กลุ่มสัตว์'] == selected_group]
    if selected_status != "ทั้งหมด":
        filtered_df = filtered_df[filtered_df['สถานภาพของชนิดพันธุ์'] == selected_status]

    col1, col2, col3 = st.columns(3)
    col1.metric("จำนวนชนิดพันธุ์ทั้งหมดในเงื่อนไข", f"{len(filtered_df):,} ชนิด")
    col2.metric("กลุ่มสัตว์ที่เลือก", selected_group)
    col3.metric("สถานภาพที่เลือก", selected_status)

    st.markdown("---")

    # 4. แสดงกราฟ 2 รูปแบบ
    st.subheader("📊 กราฟวิเคราะห์ข้อมูล")
    chart_col1, chart_col2 = st.columns(2)

    with chart_col1:
        status_counts = filtered_df['สถานภาพของชนิดพันธุ์'].value_counts().reset_index()
        status_counts.columns = ['สถานภาพ', 'จำนวนชนิด']
        fig1 = px.bar(
            status_counts, 
            x='สถานภาพ', 
            y='จำนวนชนิด',
            color='สถานภาพ',
            title="1. จำนวนชนิดพันธุ์แบ่งตามสถานภาพความเสี่ยง",
            text_auto=True
        )
        st.plotly_chart(fig1, use_container_width=True)

    with chart_col2:
        group_counts = filtered_df['กลุ่มสัตว์'].value_counts().reset_index()
        group_counts.columns = ['กลุ่มสัตว์', 'จำนวนชนิด']
        fig2 = px.pie(
            group_counts, 
            names='กลุ่มสัตว์', 
            values='จำนวนชนิด',
            title="2. สัดส่วนชนิดพันธุ์แบ่งตามกลุ่มสัตว์",
            hole=0.4
        )
        st.plotly_chart(fig2, use_container_width=True)

    # 5. แสดงตารางข้อมูล
    st.markdown("---")
    st.subheader("📋 รายชื่อพันธุ์สัตว์")
    st.dataframe(
        filtered_df[['ลำดับที่', 'กลุ่มสัตว์', 'ชื่อไทย', 'ชื่อวิทยาศาสตร์', 'สถานภาพของชนิดพันธุ์', 'Status']],
        use_container_width=True
    )

except FileNotFoundError:
    st.error("❌ ไม่พบไฟล์ 'data.csv' กรุณาตรวจสอบว่าไฟล์อยู่ในโฟลเดอร์เดียวกันหรือยัง")