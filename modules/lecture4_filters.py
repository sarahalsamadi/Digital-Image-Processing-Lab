import streamlit as st
import numpy as np
import cv2
from PIL import Image
import io

def show_images_in_rows(images, images_per_row=2):
    for i in range(0, len(images), images_per_row):
        row = st.columns(images_per_row)
        for j, (label, img) in enumerate(images[i:i + images_per_row]):
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

def run(img_np, original_img):
    st.header("🔍 المحاضرة 4: الفلاتر والالتفاف (Filtering & Convolution)")

    with st.expander("📖 الشرح النظري"):
        st.markdown("""
        - **Kernel / Mask**: مصفوفة صغيرة (مثل 3×3) تُطبق على الصورة عبر الالتفاف (Convolution).
        - **Sharpen**: توضيح التفاصيل والحواف.
        - **Blur** (Gaussian / Median): تمويه وتقليل الضوضاء.
        - **Edge**: كشف الحواف باستخدام مرشحات مثل Laplacian أو Sobel.
        """)

    filter_type = st.selectbox("🎛️ اختر نوع الفلتر:", [
        "Gaussian Blur",
        "Median Blur",
        "Sharpen",
        "Edge (Laplacian)",
        "Emboss"
    ])

    # حجم الكيرنل للفلتر
    if filter_type in ["Gaussian Blur", "Median Blur"]:
        ksize = st.slider("📐 حجم الكيرنل (يجب أن يكون فرديًا)", 3, 15, 5, step=2)

    if st.button("🚀 تنفيذ الفلتر"):
        result = img_np.copy()

        if filter_type == "Gaussian Blur":
            result = cv2.GaussianBlur(result, (ksize, ksize), 0)

        elif filter_type == "Median Blur":
            result = cv2.medianBlur(result, ksize)

        elif filter_type == "Sharpen":
            kernel = np.array([[0, -1, 0],
                               [-1, 5, -1],
                               [0, -1, 0]])
            result = cv2.filter2D(result, -1, kernel)

        elif filter_type == "Edge (Laplacian)":
            gray = cv2.cvtColor(result, cv2.COLOR_RGB2GRAY)
            edges = cv2.Laplacian(gray, cv2.CV_64F)
            result = cv2.convertScaleAbs(edges)
            result = cv2.cvtColor(result, cv2.COLOR_GRAY2RGB)  # لعرضه كصورة ملونة

        elif filter_type == "Emboss":
            kernel = np.array([[-2, -1, 0],
                               [-1, 1, 1],
                               [0, 1, 2]])
            result = cv2.filter2D(result, -1, kernel)

        # تحويل إلى PIL لعرض وتحميل
        result_img = Image.fromarray(result)

        show_images_in_rows([
            ("🖼️ الأصل", original_img),
            (f"📌 بعد {filter_type}", result_img)
        ])

    return img_np