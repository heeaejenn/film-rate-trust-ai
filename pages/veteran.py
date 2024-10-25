import streamlit as st
from test_codes.selectbox import *


st.title('베테랑2 (2024)')
st.markdown('<span style="font-size: 18px;">네이버 리뷰 평점 별 관람평 요약</span>', unsafe_allow_html=True)

st.image("data/movie_poster/veteran.jpeg", width=200, use_column_width=False)

selected_option = ranking_selectbox()

if st.button("조회하기"):
    if selected_option == "⭐⭐⭐⭐⭐":
        st.write(df['summary'][0])
    elif selected_option == "⭐⭐⭐⭐":
        st.write(df['summary'][1])
    elif selected_option == "⭐⭐⭐":
        st.write(df['summary'][2])    
    elif selected_option == "⭐⭐":
        st.write(df['summary'][3])  
    else:
        st.write(df['summary'][4])