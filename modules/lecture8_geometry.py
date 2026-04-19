import streamlit as st
import cv2
import numpy as np
from PIL import Image
import io

def run(img_np, original_img):
    st.header("🧠 المحاضرة 8: التحويلات الهندسية")

    with st.expander("📘 النظرية"):
        st.markdown("""
        - التحويلات تشمل:
            - 🔄 Translation (نقل)
            - 🔃 Rotation (تدوير)
            - 🔍 Scaling (تكبير/تصغير)
            - ↔️ Flipping (انعكاس)
            - ✂️ Cropping (قص)
        """)

    transform = st.selectbox("اختر نوع التحويل:", ["Rotation", "Scaling", "Flipping", "Cropping"])

    if transform == "Rotation":
        angle = st.slider("زاوية التدوير", -180, 180, 45)
    elif transform == "Scaling":
        scale = st.slider("نسبة التكبير/التصغير", 0.1, 3.0, 1.0)
    elif transform == "Flipping":
        flip_dir = st.radio("اتجاه الانعكاس", ["أفقي", "رأسي"])
    elif transform == "Cropping":
        x = st.number_input("X", 0, img_np.shape[1] - 1, 0)
        y = st.number_input("Y", 0, img_np.shape[0] - 1, 0)
        w = st.number_input("العرض", 1, img_np.shape[1] - x, 100)
        h = st.number_input("الارتفاع", 1, img_np.shape[0] - y, 100)

    if st.button("🚀 تنفيذ"):
        images = [("🖼️ الأصل", original_img)]
        result = img_np.copy()
        if transform == "Rotation":
            name="Rotation"
            center = (result.shape[1] // 2, result.shape[0] // 2)
            mat = cv2.getRotationMatrix2D(center, angle, 1.0)
            result = cv2.warpAffine(result, mat, (result.shape[1], result.shape[0]))
        elif transform == "Scaling":
            name="Scaling"
            result = cv2.resize(result, None, fx=scale, fy=scale)
        elif transform == "Flipping":
            name="Flipping"
            result = cv2.flip(result, 1 if flip_dir == "أفقي" else 0)
        elif transform == "Cropping":
            name="Cropping"
            result = result[int(y):int(y + h), int(x):int(x + w)]

        result_img = Image.fromarray(result)

        images.append((name, result))
        # عرض الصور
        cols = st.columns(len(images))
        for col, (label, pil_img) in zip(cols, images):
            with col:
                st.image(pil_img, caption=label, use_container_width=True)
                buf = io.BytesIO()
                pil_img = convert_to_pil(result_img)
                pil_img.save(buf, format="PNG")
                st.download_button(
                    label=f"⬇️ تحميل - {label}",
                    data=buf.getvalue(),
                    file_name=f"{label.replace(' ', '_')}.png",
                    mime="image/png")
    return img_np


def convert_to_pil(img):
    from PIL import Image
    import cv2
    if isinstance(img, Image.Image):
        return img
    if len(img.shape) == 2:
        return Image.fromarray(img)
    else:
        return Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
    