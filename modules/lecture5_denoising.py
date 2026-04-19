import streamlit as st
import io
import numpy as np
import cv2
from PIL import Image

def run(img_np, original_img):
    st.header("🧠 المحاضرة 5: إزالة الضوضاء (Denoising)")

    with st.expander("📘 النظرية"):
        st.markdown("""
        - **الضوضاء (Noise)** هي تشويش غير مرغوب فيه في الصور.
        - من الأنواع الشائعة:
            - 🧂 **Salt & Pepper**: نقاط بيضاء وسوداء.
            - 🌫️ **Gaussian Noise**: تغيير عشوائي في كل بكسل.
        - طرق الإزالة:
            - 🧹 `Median Filtering`: ممتاز لـ Salt & Pepper.
            - 🧹 `Bilateral Filtering`: يحافظ على الحواف.
        """)

    # ✅ تخزين الضوضاء في session
    if "noisy_img" not in st.session_state:
        st.session_state.noisy_img = None

    # ✅ زرين لإضافة ضوضاء
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🧂 أضف ضوضاء Salt & Pepper"):
            noisy = img_np.copy()
            row, col, _ = noisy.shape
            amount = 0.02
            num_salt = np.ceil(amount * noisy.size * 0.5)
            coords = [np.random.randint(0, i - 1, int(num_salt)) for i in noisy.shape]
            noisy[coords[0], coords[1]] = 255
            st.session_state.noisy_img = noisy
    with col2:
        if st.button("🌫️ أضف ضوضاء Gaussian"):
            mean = 0
            sigma = 25
            gauss = np.random.normal(mean, sigma, img_np.shape).astype('uint8')
            noisy = cv2.add(img_np, gauss)
            st.session_state.noisy_img = noisy

    # ✅ خيارات الفلاتر

    filter_type = st.selectbox("🎛️ اختر نوع الفلتر:", [
        "🧹 تطبيق فلتر Median",
        "🧹 تطبيق فلتر Bilateral"
    ])
    # ✅ عرض الصور فقط إذا ضوضاء موجودة
    if st.session_state.noisy_img is not None :
        images = []

        # ✅ الصورة الأصلية
        images.append(("🖼️ الأصل", original_img))

        # ✅ صورة الضوضاء
        noisy_pil = Image.fromarray(st.session_state.noisy_img)
        images.append(("🧂 صورة بها ضوضاء", noisy_pil))

        # ✅ تطبيق الفلاتر
        if st.button("🚀 تطبيق الفلاتر"):
            if filter_type=="🧹 تطبيق فلتر Median":
                result_median = cv2.medianBlur(st.session_state.noisy_img, 5)
                images.append(("🧹 Median Filter", Image.fromarray(result_median)))
            elif filter_type=="🧹 تطبيق فلتر Bilateral":
                result_bilateral = cv2.bilateralFilter(st.session_state.noisy_img, 9, 75, 75)
                images.append(("🧹 Bilateral Filter", Image.fromarray(result_bilateral)))

        # ✅ عرض الصور في صفوف (3 صور في كل صف)
        for i in range(0, len(images), 3):
            row = st.columns(3)
            for j, (label, img) in enumerate(images[i:i+3]):
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
    else:
        images = []

        # ✅ الصورة الأصلية
        images.append(("🖼️ الأصل", original_img))

        # ✅ تطبيق الفلاتر
        if st.button("🚀 تطبيق الفلاتر"):
            if filter_type=="🧹 تطبيق فلتر Median":
                result_median = cv2.medianBlur(img_np, 5)
                images.append(("🧹 Median Filter", Image.fromarray(result_median)))
            elif filter_type=="🧹 تطبيق فلتر Bilateral":
                result_bilateral = cv2.bilateralFilter(img_np, 9, 75, 75)
                images.append(("🧹 Bilateral Filter", Image.fromarray(result_bilateral)))

        # ✅ عرض الصور في صفوف (3 صور في كل صف)
        for i in range(0, len(images), 3):
            row = st.columns(3)
            for j, (label, img) in enumerate(images[i:i+3]):
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

    return img_np