import streamlit as st
import cv2
import numpy as np
from PIL import Image
import io

def run(img_np, original_img):
    st.header("🧠 المحاضرة 6: كشف الحواف (Edge Detection)")

    with st.expander("📘 النظرية"):
        st.markdown("""
        - تعتمد **كشف الحواف** على التدرج في الصورة (Gradient).
        - أشهر الخوارزميات:
            - 🔹 Sobel Filter
            - 🔹 Laplacian
            - 🔹 Canny (تدعم التحكم بالعتبات)
        """)

    method = st.selectbox("اختر نوع كشف الحواف:", ["Sobel", "Laplacian", "Canny"])

    if method == "Canny":
        t1 = st.slider("عتبة أولى (Threshold1)", 0, 255, 100)
        t2 = st.slider("عتبة ثانية (Threshold2)", 0, 255, 200)

    if st.button("🚀 تنفيذ"):
        gray = cv2.cvtColor(img_np, cv2.COLOR_RGB2GRAY)
        images = [("🖼️ الأصل", original_img)]

        if method == "Sobel":
            name="Sobel"
            edge = cv2.Sobel(gray, cv2.CV_64F, 1, 1, ksize=5)
            edge = cv2.convertScaleAbs(edge)

        elif method == "Laplacian":
            name="Laplacian"
            edge = cv2.Laplacian(gray, cv2.CV_64F)
            edge = cv2.convertScaleAbs(edge)
        else:
            name="Canny"
            edge = cv2.Canny(gray, t1, t2)

        result = Image.fromarray(edge)
        images.append((name, result))
        # عرض الصور
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
                    mime="image/png")
    return img_np