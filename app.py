import streamlit as st
import easyocr
import numpy as np
from PIL import Image

# إعداد قارئ النصوص (سيتم تحميله مرة واحدة عند تشغيل التطبيق)
@st.cache_resource
def load_ocr():
    return easyocr.Reader(['en']) # نركز على الإنجليزية لأن المكونات تكتب بها غالباً

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
    file_high = st.file_uploader("صورة المكونات (High-end)", type=["jpg", "png", "jpeg"], key="1")
    text_high = st.text_area("المكونات المستخرجة:", value=extract_text(file_high) if file_high else "", height=150)

with col2:
    st.subheader("البديل الأرخص")
    file_low = st.file_uploader("صورة المكونات (Budget)", type=["jpg", "png", "jpeg"], key="2")
    text_low = st.text_area("المكونات المستخرجة:", value=extract_text(file_low) if file_low else "", height=150)

# زر التحليل (نفس المنطق السابق)
if st.button("تحليل التطابق الكيميائي 🔍"):
    if text_high and text_low:
        # هنا تضع كود المقارنة الذي أعطيتك إياه سابقاً
        st.balloons()
        st.success("تم استخراج البيانات والمقارنة بنجاح!")
    else:
        st.error("يرجى رفع الصور أولاً ليقوم التطبيق بقراءتها.")
