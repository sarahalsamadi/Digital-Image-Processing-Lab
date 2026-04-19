import streamlit as st
import cv2
import numpy as np
from PIL import Image
import io

def run(img_np, original_img):
    st.header("🧠 المحاضرة 3: العمليات على البكسل")
    with st.expander("📖 الشرح النظري"):
        st.markdown("""
        - **السطوع**: زيادة أو تقليل القيم.
        - **التباين**: توسيع الفرق بين القيم.
        - **الصورة السالبة**: 255 - pixel.
        - **Thresholding**: تحويل إلى أسود/أبيض.
        """)

    st.markdown("### 🎯 اختر العمليات التي تريد تطبيقها على الصورة:")

    brightness = st.slider("السطوع", -100, 100, 0)
    contrast = st.slider("التباين", 1.0, 3.0, 1.0)

    filter_type = st.selectbox(" اختر نوع التطبيق:", [
        " تطبيق Negative",
        " تطبيق Threshold"
    ])

    if st.button("🚀 تنفيذ العمليات"):
        # ✅ 1. الصورة الأصلية
        images = [("🖼️ الأصل", original_img)]

        # ✅ 2. تعديل سطوع وتباين
        modified = cv2.convertScaleAbs(img_np, alpha=contrast, beta=brightness)
        modified_pil = Image.fromarray(modified)
        images.append(("🔆 سطوع + تباين", modified_pil))

        # ✅ 3. Negative
        if filter_type == " تطبيق Negative":
            negative = 255 - modified
            negative_pil = Image.fromarray(negative)
            images.append((" Negative", negative_pil))

        # ✅ 4. Threshold
        elif filter_type == " تطبيق Threshold":
            gray = cv2.cvtColor(modified, cv2.COLOR_RGB2GRAY)
            _, th = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
            th_rgb = cv2.cvtColor(th, cv2.COLOR_GRAY2RGB)
            th_pil = Image.fromarray(th_rgb)
            images.append((" Threshold", th_pil))

        # ✅ عرض الصور في أعمدة
        cols = st.columns(len(images))
        for col, (label, pil_img) in zip(cols, images):
            with col:
                st.image(pil_img, caption=label, use_container_width=True)
                buf = io.BytesIO()
                pil_img.save(buf, format="PNG")
                st.download_button(
                    label=f"⬇️ تحميل - {label}",
                    data=buf.getvalue(),
                    file_name=f"{label.replace(' ', '_')}.png",
                    mime="image/png"
                )

    return img_np