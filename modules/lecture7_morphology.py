import streamlit as st
import cv2
import numpy as np
from PIL import Image
import io

def run(img_np, original_img):
    st.header("🧠 المحاضرة 7: العمليات المورفولوجية")

    with st.expander("📘 النظرية"):
        st.markdown("""
        - تستخدم العمليات المورفولوجية لتحسين الصور الثنائية.
        - تشمل:
            - 🔸 Erosion (تآكل)
            - 🔸 Dilation (توسيع)
            - 🔸 Opening (إزالة النقاط الصغيرة)
            - 🔸 Closing (سد الفجوات)
        """)

    kernel_size = st.slider("📏 حجم العنصر البنائي (Kernel)", 1, 15, 3, step=2,format="%d")
    operation = st.selectbox("اختر العملية:", ["Erosion", "Dilation", "Opening", "Closing"])

    if st.button("🚀 تنفيذ"):
        images = [("🖼️ الأصل", original_img)]
        img_np = ensure_numpy(img_np)
        gray = cv2.cvtColor(img_np, cv2.COLOR_RGB2GRAY)
        _, binary = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)

        kernel = np.ones((kernel_size, kernel_size), np.uint8)

        if operation == "Erosion":
            name="Erosion"
            result = cv2.erode(binary, kernel, iterations=1)
        elif operation == "Dilation":
            name="Dilation"
            result = cv2.dilate(binary, kernel, iterations=1)
        elif operation == "Opening":
            name="Opening"
            result = cv2.morphologyEx(binary, cv2.MORPH_OPEN, kernel)
        else:
            name="Closing"
            result = cv2.morphologyEx(binary, cv2.MORPH_CLOSE, kernel)

        result_img = Image.fromarray(result)

        images.append(( name, result))
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
    
def ensure_numpy(img):
    from PIL import Image
    import numpy as np

    if isinstance(img, Image.Image):
        return np.array(img)
    return img