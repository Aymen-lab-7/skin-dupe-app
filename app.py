import streamlit as st
import cv2
import numpy as np
from PIL import Image

# إعدادات الواجهة
st.set_page_config(page_title="Skincare Dupe Finder", page_icon="✨")

# كود الـ PWA
st.markdown("""
    <head>
        <meta name="apple-mobile-web-app-capable" content="yes">
        <meta name="apple-mobile-web-app-status-bar-style" content="black">
        <link rel="apple-touch-icon" href="https://cdn-icons-png.flaticon.com/512/3163/3163195.png">
    </head>
    """, unsafe_allow_html=True)

st.title("✨ Skincare Dupe Finder")
st.markdown("---")

# قاعدة بيانات مصغرة للمواد الفعالة وأهميتها (وزنها في الحساب)
ACTIVE_INGREDIENTS = {
    "retinol": 10, "vitamin c": 10, "niacinamide": 8, 
    "hyaluronic acid": 8, "salicylic acid": 9, "glycolic acid": 9,
    "ceramides": 7, "peptides": 8, "panthenol": 5, "zinc": 6
}

def compare_ingredients(text_high, text_budget):
    # تنظيف النصوص وتحويلها لقوائم
    list_high = [i.strip().lower() for i in text_high.replace("\n", ",").split(",")]
    list_budget = [i.strip().lower() for i in text_budget.replace("\n", ",").split(",")]
    
    score, total_weight = 0, 0
    shared_actives = []
    
    for ing in list_high:
        weight = ACTIVE_INGREDIENTS.get(ing, 1) # إذا لم تكن مادة معروفة نعطيها وزن 1
        total_weight += weight
        if any(ing in b for b in list_budget):
            score += weight
            if ing in ACTIVE_INGREDIENTS:
                shared_actives.append(ing)
    
    final_ratio = (score / total_weight) * 100 if total_weight > 0 else 0
    return round(final_ratio, 1), shared_actives

# واجهة المستخدم
col1, col2 = st.columns(2)

with col1:
    st.subheader("المنتج الغالي")
    img_high = st.file_uploader("ارفع صورة المكونات", type=["jpg", "png", "jpeg"], key="high_img")
    high_text = st.text_area("أو اكتب المكونات هنا:", key="t1")

with col2:
    st.subheader("البديل الأرخص")
    img_low = st.file_uploader("ارفع صورة المكونات", type=["jpg", "png", "jpeg"], key="low_img")
    budget_text = st.text_area("أو اكتب المكونات هنا:", key="t2")

if st.button("تحليل التطابق 🔍"):
    if (high_text or img_high) and (budget_text or img_low):
        # هنا يتم استدعاء خوارزمية المقارنة
        ratio, actives = compare_ingredients(high_text, budget_text)
        
        st.divider()
        st.metric(label="نسبة التطابق الكيميائي", value=f"{ratio}%")
        
        if ratio > 80:
            st.success("✅ هذا بديل مذهل! المكونات متطابقة بشكل كبير.")
        elif ratio > 50:
            st.warning("⚠️ بديل جيد، لكن هناك بعض الاختلافات في المواد الثانوية.")
        else:
            st.error("❌ التطابق ضعيف، قد لا يعطي نفس النتيجة.")
            
        if actives:
            st.info(f"المواد الفعالة المشتركة التي وجدناها: {', '.join(actives)}")
    else:
        st.error("من فضلك أدخل المكونات أو ارفع الصور للمقارنة.")

st.markdown("---")
st.caption("ملاحظة: هذا التطبيق يقارن المكونات المكتوبة ولا يغني عن استشارة طبيب الجلدية.")
