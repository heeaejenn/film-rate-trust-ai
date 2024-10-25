import streamlit as st
from test_codes.selectbox import *


st.title('명탐정 코난: 시한장치의 마천루 (2024)')
st.markdown('<span style="font-size: 18px;">네이버 리뷰 평점 별 관람평 요약</span>', unsafe_allow_html=True)

st.image("data/movie_poster/konan.jpeg", width=200, use_column_width=False)

## sql DB 연결

# Initialize connection.
conn = st.connection('mysql', type='sql')
# Perform query.
df = conn.query('SELECT * from summarized_reviews;', ttl=600)

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