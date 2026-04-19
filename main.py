import streamlit as st
from PIL import Image
import numpy as np
import os

# استيراد المحاضرات
import modules.lecture1_intro as lecture1
import modules.lecture2_colorspaces as lecture2
import modules.lecture3_point_ops as lecture3
import modules.lecture4_filters as lecture4
import modules.lecture5_denoising as lecture5
import modules.lecture6_edges as lecture6
import modules.lecture7_morphology as lecture7
import modules.lecture8_geometry as lecture8
import modules.lecture9_pipeline as lecture9
# إعداد الصفحة
st.set_page_config(page_title="📚 سلسلة محاضرات معالجة الصور", layout="wide")

# ✅ تغيير الاتجاه إلى اليمين والشريط الجانبي لليمين
st.markdown("""
    <style>
        html, body, [class*="css"] {
            direction: rtl;
            text-align: right;
        }

        section[data-testid="stSidebar"] {
            border-left: 1px solid #DDD;
            border-right: none;
            right: 0;
            left: auto;
        }

        section[data-testid="stSidebar"] ~ div.main {
            margin-left: 0;
            margin-right: 20rem;
        }
    </style>
""", unsafe_allow_html=True)


# الشريط الجانبي
st.sidebar.title("📚 قائمة المحاضرات")
lecture = st.sidebar.selectbox("اختر المحاضرة", [
    "🔙 الصفحة الرئيسية",
    " 1: مدخل ومعمارية الصور",
    " 2: أنظمة الألوان",
    " 3: العمليات على البكسل",
    " 4: الفلاتر والالتفاف",
    " 5: إزالة الضوضاء",
    " 6: كشف الحواف",
    " 7: العمليات المورفولوجية",
    " 8: التحويلات الهندسية",
    " 9:  تطبيق كل العمليات",
])

uploaded_file = st.sidebar.file_uploader("📤 ارفع صورة", type=["jpg", "jpeg", "png"])

# تحميل الصورة الأصلية أو الافتراضية
default_path = "assets/default.jpg"
original_image = None

if uploaded_file is not None:
    original_image = Image.open(uploaded_file).convert("RGB")
elif os.path.exists(default_path):
    original_image = Image.open(default_path).convert("RGB")
else:
    st.error("❌ لم يتم رفع صورة أو العثور على الصورة الافتراضية.")
    st.stop()

# تحويل الصورة إلى NumPy
image_np = np.array(original_image)

# ✅ الصفحة الترحيبية
if lecture == "🔙 الصفحة الرئيسية":
    st.title("👋 مرحبًا بك في سلسلة محاضرات معالجة الصور الرقمية")
    st.markdown("""
    🎓 هذا المشروع التعليمي التفاعلي يهدف إلى تبسيط مفاهيم معالجة الصور باستخدام بايثون.

    🧠 ستتعلم من خلال 9 محاضرات تفاعلية:
    - بنية الصورة الرقمية
    - أنظمة الألوان
    - الفلاتر والعمليات المورفولوجية
    - التحويلات الهندسية
    - مشروع تطبيقي ختامي

    📌 ابدأ باختيار محاضرة من القائمة الجانبية ورفع صورة لتطبيق المفاهيم عمليًا.
    """)
    #st.image("assets/default.jpg", caption="📷 مثال توضيحي", use_column_width=True)

# ✅ عند اختيار محاضرة: أظهر الشرح فقط — الصور تظهر فقط عند "تطبيق"
else:
    if lecture.startswith(" 1"):
        lecture1.run(image_np, original_image)
    elif lecture.startswith(" 2"):
        lecture2.run(image_np, original_image)
    elif lecture.startswith(" 3"):
        lecture3.run(image_np, original_image)
    elif lecture.startswith(" 4"):
        lecture4.run(image_np, original_image)
    elif lecture.startswith(" 5"):
        lecture5.run(image_np, original_image)
    elif lecture.startswith(" 6"):
        lecture6.run(image_np, original_image)
    elif lecture.startswith(" 7"):
        lecture7.run(image_np, original_image)
    elif lecture.startswith(" 8"):
        lecture8.run(image_np, original_image)
    elif lecture.startswith(" 9"):
        lecture9.run(image_np, original_image)
