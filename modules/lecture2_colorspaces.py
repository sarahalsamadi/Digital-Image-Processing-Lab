import streamlit as st
import cv2
from PIL import Image
import io

def run(img_np, original_img):
    st.header("🧠 المحاضرة 2: أنظمة الألوان")
    with st.expander("📖 الشرح النظري"):
        st.markdown("""
        - RGB: النظام اللوني الأساسي في الشاشات.
        - BGR: ترتيب OpenCV الافتراضي.
        - Gray: صورة رمادية، قناة واحدة.
        - HSV: فصل اللون عن الإضاءة، مناسب للتتبع.
        """)

    st.markdown("### 🎯 اختر أنظمة الألوان التي تريد تحويل الصورة إليها:")

    apply_gray = st.checkbox("Gray")
    apply_hsv = st.checkbox(" HSV")
    apply_rgb=st.checkbox("  قنوات R/G/B")
    #option = st.selectbox("اختر نوع التحويل:", ["Gray", "HSV", "R/G/B Channels"])

    if st.button("🚀 تطبيق"):
        images = [("🖼️ الأصل", original_img)]

        if apply_gray:
            gray = cv2.cvtColor(img_np, cv2.COLOR_RGB2GRAY)
            images.append(("🌑 رمادي", Image.fromarray(gray)))

        if apply_hsv:
            hsv = cv2.cvtColor(img_np, cv2.COLOR_RGB2HSV)
            images.append(("🌈 HSV", Image.fromarray(hsv)))

        if apply_rgb:
            channels = cv2.split(img_np)
            labels = ["🔴 Red", "🟢 Green", "🔵 Blue"]
            for i, ch in enumerate(channels):
                color_img = cv2.merge([ch if j == i else ch*0 for j in range(3)])
                images.append((labels[i], Image.fromarray(color_img)))

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