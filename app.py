import streamlit as st
import easyocr
import numpy as np
from PIL import Image

# 1. إعداد قارئ النصوص
@st.cache_resource
def load_ocr():
    return easyocr.Reader(['en'])

reader = load_ocr()

# 2. قاعدة بيانات المواد الفعالة (للحساب الذكي)
ACTIVE_INGREDIENTS = {
    "retinol": 10, "vitamin c": 10, "niacinamide": 8, 
    "hyaluronic acid": 8, "salicylic acid": 9, "glycolic acid": 9,
    "ceramides": 7, "peptides": 8, "panthenol": 5, "zinc": 6
}

st.set_page_config(page_title="Skincare Dupe Finder", page_icon="✨")

st.title("✨ Skincare Dupe Finder & Shop")

# 3. دالة استخراج النص
def extract_text(image_file):
    image = Image.open(image_file)
    img_array = np.array(image)
    results = reader.readtext(img_array, detail=0)
    return ", ".join(results)

# 4. دالة حساب التطابق
def calculate_dupe_ratio(high_text, low_text):
    list_high = [i.strip().lower() for i in high_text.replace("\n", ",").split(",")]
    list_low = [i.strip().lower() for i in low_text.replace("\n", ",").split(",")]
    
    score, total_weight = 0, 0
    for ing in list_high:
        weight = ACTIVE_INGREDIENTS.get(ing, 1)
        total_weight += weight
        if any(ing in b for b in list_low):
            score += weight
    
    return (score / total_weight) * 100 if total_weight > 0 else 0

# 5. واجهة المستخدم
col1, col2 = st.columns(2)

with col1:
    st.subheader("المنتج الغالي")
    file_high = st.file_uploader("صورة المكونات (High-end)", type=["jpg", "png", "jpeg"], key="up_high")
    text_high = st.text_area("المكونات المستخرجة 1:", value=extract_text(file_high) if file_high else "", height=150, key="res_high")

with col2:
    st.subheader("البديل الأرخص")
    file_low = st.file_uploader("صورة المكونات (Budget)", type=["jpg", "png", "jpeg"], key="up_low")
    text_low = st.text_area("المكونات المستخرجة 2:", value=extract_text(file_low) if file_low else "", height=150, key="res_low")

# 6. زر التحليل والربح
if st.button("تحليل التطابق الكيميائي 🔍"):
    if text_high and text_low:
        ratio = calculate_dupe_ratio(text_high, text_low)
        st.divider()
        st.metric(label="نسبة التطابق", value=f"{round(ratio, 1)}%")
        
        if ratio > 70:
            st.success("✅ هذا بديل ممتاز! المكونات متطابقة بنسبة كبيرة.")
            # زر الأفلييت (يمكنك استبدال الرابط برابطك الخاص)
            amazon_url = "https://www.amazon.com/s?k=skincare+moisturizer&tag=YOUR_TAG_HERE"
            st.markdown(f'''
                <a href="{amazon_url}" target="_blank">
                    <button style="background-color: #FF9900; color: white; border: none; padding: 15px; border-radius: 10px; cursor: pointer; width: 100%; font-weight: bold;">
                        🛒 اشتري البديل الموفر الآن (أمازون)
                    </button>
                </a>
            ''', unsafe_allow_html=True)
        else:
            st.warning("⚠️ التطابق متوسط، قد لا يعطي نفس النتيجة تماماً.")
    else:
        st.error("يرجى رفع الصور أولاً.")
