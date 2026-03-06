import streamlit as st
import easyocr
import numpy as np
from PIL import Image

# إعداد قارئ النصوص
@st.cache_resource
def load_ocr():
    return easyocr.Reader(['en'])

reader = load_ocr()

st.set_page_config(page_title="Skincare Dupe Finder", page_icon="✨")

st.title("✨ Skincare Dupe Finder")
st.write("ارفع صورة المكونات وسنقوم بقراءتها وتحليلها لك!")

def extract_text(image_file):
    image = Image.open(image_file)
    img_array = np.array(image)
    results = reader.readtext(img_array, detail=0)
    return ", ".join(results)

col1, col2 = st.columns(2)

with col1:
    st.subheader("المنتج الغالي")
    file_high = st.file_uploader("صورة المكونات (High-end)", type=["jpg", "png", "jpeg"], key="upload_high")
    # أضفنا key="high_res" هنا لمنع التكرار
    text_high = st.text_area("المكونات المستخرجة (منتج 1):", value=extract_text(file_high) if file_high else "", height=150, key="high_res")

with col2:
    st.subheader("البديل الأرخص")
    file_low = st.file_uploader("صورة المكونات (Budget)", type=["jpg", "png", "jpeg"], key="upload_low")
    # أضفنا key="low_res" هنا لمنع التكرار
    text_low = st.text_area("المكونات المستخرجة (منتج 2):", value=extract_text(file_low) if file_low else "", height=150, key="low_res")

# زر التحليل
if st.button("تحليل التطابق الكيميائي 🔍"):
    if text_high and text_low:
        st.balloons()
        st.success("تم استخراج البيانات! التطبيق الآن جاهز للمقارنة.")
    else:
        st.error("يرجى رفع الصور أو كتابة المكونات أولاً.")
