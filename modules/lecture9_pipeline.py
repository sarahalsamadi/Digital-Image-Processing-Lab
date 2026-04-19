import streamlit as st
import cv2
import numpy as np
from PIL import Image
import io

# ✅ تستخدم لعرض الصور في صفوف 3 في كل صف
def show_images_in_rows(images, images_per_row=3):
    for i in range(0, len(images), images_per_row):
        row = st.columns(images_per_row)
        for j, (label, img) in enumerate(images[i:i+images_per_row]):
            with row[j]:
                st.image(img, caption=label, use_container_width=True)
                buf = io.BytesIO()
                img.save(buf, format="PNG")
                st.download_button(
                    label=f"⬇️ تحميل - {label}",
                    data=buf.getvalue(),
                    file_name=f"{label.replace(' ', '_')}.png",
                    mime="image/png"
                )

# ✅ المحاضرة 9 - المشروع النهائي
def run(img_np, original_img):
    st.header("🧪 المحاضرة 9: مشروع ختامي - بناء سلسلة عمليات (Pipeline)")

    with st.expander("📘 التعليمات"):
        st.markdown("""
        - قم برفع صورة.
        - اختر سلسلة من العمليات ليتم تطبيقها بالترتيب.
        - سترى النتيجة النهائية ويمكنك تحميلها.
        """)

    # ✅ قائمة العمليات المتاحة
    operations = st.multiselect(
        "🧰 اختر العمليات التي تريد تطبيقها بالترتيب:",
        ["Gray", "Gaussian Blur", "Median Blur", "Canny Edge", "Flip Horizontal", "Flip Vertical", "Rotate"],
        default=["Gray", "Gaussian Blur", "Canny Edge"]
    )

    rotation_angle = 0
    if "Rotate" in operations:
        rotation_angle = st.slider("🎯 زاوية التدوير (Rotate)", -180, 180, 90)

    if st.button("🚀 تنفيذ السلسلة"):
        result = img_np.copy()
        images = [("🖼️ الأصل", Image.fromarray(result))]

        for op in operations:
            if op == "Gray":
                result = cv2.cvtColor(result, cv2.COLOR_RGB2GRAY)
            elif op == "Gaussian Blur":
                result = cv2.GaussianBlur(result, (5, 5), 0)
            elif op == "Median Blur":
                result = cv2.medianBlur(result, 5)
            elif op == "Canny Edge":
                if len(result.shape) == 3:
                    result = cv2.cvtColor(result, cv2.COLOR_RGB2GRAY)
                result = cv2.Canny(result, 100, 200)
            elif op == "Flip Horizontal":
                result = cv2.flip(result, 1)
            elif op == "Flip Vertical":
                result = cv2.flip(result, 0)
            elif op == "Rotate":
                (h, w) = result.shape[:2]
                center = (w // 2, h // 2)
                M = cv2.getRotationMatrix2D(center, rotation_angle, 1.0)
                result = cv2.warpAffine(result, M, (w, h))

            # 🖼️ حفظ كل مرحلة كصورة
            img_pil = Image.fromarray(result) if len(result.shape) == 2 else Image.fromarray(cv2.cvtColor(result, cv2.COLOR_BGR2RGB))
            images.append((f"📌 بعد {op}", img_pil))

        # ✅ عرض الصور في صفوف
        show_images_in_rows(images)

    return img_np