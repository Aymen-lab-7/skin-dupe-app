import streamlit as st

st.set_page_config(page_title="Skincare Dupe Finder", page_icon="✨")

# كود حقن تطبيق الويب التقدمي PWA
st.markdown("""
    <head>
        <meta name="apple-mobile-web-app-capable" content="yes">
        <meta name="apple-mobile-web-app-status-bar-style" content="black">
        <link rel="apple-touch-icon" href="https://cdn-icons-png.flaticon.com/512/3163/3163195.png">
    </head>
    """, unsafe_allow_html=True)

st.title("✨ Skincare Dupe Finder")
st.subheader("قارن المكونات واكتشف البديل الأرخص بذكاء")

col1, col2 = st.columns(2)
with col1:
    high_end = st.text_area("قائمة مكونات المنتج الغالي:")
with col2:
    budget = st.text_area("قائمة مكونات المنتج البديل:")

if st.button("تحليل التطابق 🔍"):
    if high_end and budget:
        st.balloons()
        st.success("تم التحليل! (سيظهر هنا منطق المقارنة)")
    else:
        st.error("يرجى إدخال المكونات أولاً")
