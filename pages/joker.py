import streamlit as st
from test_codes.selectbox import *

st.title('조커: 폴리 아 되 (2024)')
st.markdown('<span style="font-size: 18px;">네이버 리뷰 평점 별 관람평 요약</span>', unsafe_allow_html=True)

st.image("data/movie_poster/joker.jpeg", width=200, use_column_width=False)

## sql DB 연결

# Initialize connection using st.secrets.
conn = st.connection('mysql', type='sql')
# Perform query.
df = conn.query('SELECT * from summarized_reviews;', ttl=600)

selected_option = ranking_selectbox()

if st.button("조회하기"):
    if selected_option == "⭐⭐⭐⭐⭐":
        st.write(df['summary'][0])
        # st.write("9~10점짜리 리뷰 요약글(df 연결 전)")
    elif selected_option == "⭐⭐⭐⭐":
        st.write(df['summary'][1])
        # st.write("7~8점짜리 리뷰 요약글(df 연결 전)")
    elif selected_option == "⭐⭐⭐":
        st.write(df['summary'][2]) 
        # st.write("5~6점짜리 리뷰 요약글(df 연결 전)")   
    elif selected_option == "⭐⭐":
        st.write(df['summary'][3])  
        # st.write("3~4점짜리 리뷰 요약글(df 연결 전)")
    else:
       st.write(df['summary'][4])
       # st.write("0~2점짜리 리뷰 요약글(df 연결 전)")