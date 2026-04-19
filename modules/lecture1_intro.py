import streamlit as st
import io
from PIL import Image

def run(img_np, original_img):
    st.header("🧠 المحاضرة 1: مدخل ومعمارية الصور")
    with st.expander("📖 الشرح النظري"):
        st.markdown("""
        - الصورة الرقمية هي **مصفوفة من البكسلات (Pixels)**.
        - كل بكسل يمثل قيمة لونية (لون أو رمادي).
        - الأبعاد: `Height × Width × Channels` (مثلًا 512×512×3).
        - القنوات: R/G/B أو Gray.
        - العمق اللوني (bit depth): عدد البتات لكل بكسل (مثلًا 8bit = 0–255).
        """)

    st.markdown("### 🎯 اضغط على الزر التالي لتطبيق الشرح على الصورة:")

    if st.button("🚀 تطبيق", key="lecture1_apply"):
        st.success("✅ تم تنفيذ العملية بنجاح")

        height, width = img_np.shape[0], img_np.shape[1]
        channels = img_np.shape[2] if len(img_np.shape) == 3 else 1
        dtype = img_np.dtype
        bit_depth = img_np.dtype.itemsize * 8
        st.subheader("📋 معلومات الصورة:")
        st.markdown(f"""
        - 📏 الأبعاد: `{height} × {width}`
        - 🎨 عدد القنوات: `{channels}`
        - 🧬 نوع البيانات: `{dtype}`
        - 🌈 العمق اللوني: `{bit_depth} بت`""")
        # عرض الصورة الأصلية فقط بعد التطبيق
        col1, col2 = st.columns([1, 1])
        with col1:
            st.image(original_img, caption="🖼️ الصورة الأصلية", use_container_width=True)

            # زر تحميل الصورة
            buf = io.BytesIO()
            original_img.save(buf, format="PNG")
            byte_im = buf.getvalue()

            st.download_button(
                label="⬇️ تحميل الصورة الأصلية",
                data=byte_im,
                file_name="original.png",
                mime="image/png"
            )

    return img_np