import streamlit as st
import plotly.graph_objects as go
import numpy as np

# إعداد عنوان الصفحة ومظهرها
st.set_page_config(page_title="لوحة تحكم الصوبة الذكية", layout="wide")
st.title("🌱 نظام محاكاة وتصميم الصوبة الذكية")

# لوحة التحكم الجانبية لتعديل المقاسات والتحكم في الأجهزة
st.sidebar.header("⚙️ التحكم في أبعاد الصوبة")
length = st.sidebar.slider("📏 طول الصوبة (متر)", 2, 10, 5)
width = st.sidebar.slider("↔️ عرض الصوبة (متر)", 2, 6, 3)
height = st.sidebar.slider("↕️ الارتفاع (متر)", 1, 4, 2)

st.sidebar.header("🔌 التحكم في الأجهزة (IoT)")
fan_status = st.sidebar.toggle("💨 تشغيل مروحة التهوية")
light_status = st.sidebar.toggle("💡 تشغيل إضاءة النمو (LED)")
pump_status = st.sidebar.toggle("💧 تشغيل مضخة الري بالتنقيط")

# بناء الشكل الهيدسي ثلاثي الأبعاد (3D) للصوبة
fig = go.Figure()

# رسم الأقواس أو الهيكل الخشبي/المعدني للصوبة
z_space = np.linspace(0, length, 5) # 5 أقواس متتالية
theta = np.linspace(0, np.pi, 20)

for z in z_space:
    x = (width / 2) * np.cos(theta)
    y = np.full_like(x, z)
    z_coords = height * np.sin(theta)
    
    # لون الهيكل بيتغير لو لمبات الإضاءة شغالين
    frame_color = "#ff4bbb" if light_status else "#aaaaaa"
    
    fig.add_trace(go.Scatter3d(
        x=x, y=y, z=z_coords, mode='lines',
        line=dict(color=frame_color, width=4),
        name="الهيكل الإنشائي"
    ))

# رسم خراطيم الري على الأرض (بلون أزرق متحرك لو المضخة شغالة)
water_color = "#00bfff" if pump_status else "#444444"
fig.add_trace(go.Scatter3d(
    x=[-width/4, -width/4], y=[0, length], z=[0, 0],
    mode='lines', line=dict(color=water_color, width=5), name="خط ري 1"
))
fig.add_trace(go.Scatter3d(
    x=[width/4, width/4], y=[0, length], z=[0, 0],
    mode='lines', line=dict(color=water_color, width=5), name="خط ري 2"
))

# إضافة الحساسات والمروحة في التصميم كنقاط مضيئة
fan_color = "#00ffcc" if fan_status else "#ff4b4b"
fig.add_trace(go.Scatter3d(
    x=[0], y=[length], z=[height/2],
    mode='markers', marker=dict(size=12, color=fan_color, symbol='square'),
    name="موقع المروحة والتهوية"
))

# إعدادات مظهر الشاشة الـ 3D
fig.update_layout(
    scene=dict(
        xaxis=dict(backgroundcolor="black", gridcolor="gray", showbackground=True),
        yaxis=dict(backgroundcolor="black", gridcolor="gray", showbackground=True),
        zaxis=dict(backgroundcolor="black", gridcolor="gray", showbackground=True),
    ),
    template="plotly_dark", margin=dict(r=0, l=0, b=0, t=0)
)

# عرض التصميم التفاعلي في الشاشة الرئيسية لصفحة الويب
col_viz, col_status = st.columns([3, 1])

with col_viz:
    st.plotly_chart(fig, use_container_width=True)

with col_status:
    st.subheader("📊 حالة الحساسات الآن")
    st.metric(label="🌡️ درجة الحرارة الداخية", value="24.5 °C")
    st.metric(label="💧 رطوبة التربة", value="65%")
    
    if fan_status:
        st.success("💨 المروحة تعمل الآن لتبريد الصوبة.")
    if pump_status:
        st.info("💧 مضخة الري بالتنقيط تقوم بسقاية النباتات.")
        