import pymysql
import streamlit as st
import sys
import os

# test_codes의 절대 경로 추가 (직접 지정)
sys.path.append(r'C:/Users/kwkwo/film-rate-trust-ai/test_codes')

# selectbox 모듈 가져오기
from selectbox import *

st.title('조커: 폴리 아 되 (2024)')
st.markdown('<span style="font-size: 18px;">네이버 리뷰 평점 별 관람평 요약</span>', unsafe_allow_html=True)

st.image("data/movie_poster/joker.jpeg", width=200, use_column_width=False)

# 데이터베이스 연결 설정
conn = pymysql.connect(
    host=st.secrets["mysql"]["host"],
    port=st.secrets["mysql"]["port"],
    user=st.secrets["mysql"]["user"],
    password=st.secrets["mysql"]["password"],
    database=st.secrets["mysql"]["database"])

try:
    # 데이터베이스 작업 수행
    with conn.cursor() as cursor:
        cursor.execute('SELECT * FROM summarized_reviews;')
        result = cursor.fetchall()
        # DataFrame 생성
        df = pd.DataFrame(result, columns=[col[0] for col in cursor.description])
finally:
    # 데이터베이스 연결 닫기
    conn.close()

# movie_id와 rating 열을 숫자로 변환
df['movie_id'] = pd.to_numeric(df['movie_id'], errors='coerce')
df['rating'] = pd.to_numeric(df['rating'], errors='coerce')

selected_option = ranking_selectbox()

if st.button("조회하기"):
    if selected_option == "⭐⭐⭐⭐⭐":
        # 조건에 맞는 행 필터링
        filtered_df_4_10 = df[(df['movie_id'] == 4) & (df['rating'] == 10)]
        # summary 값 추출
        summary_value_4_10 = filtered_df_4_10['summary'].iloc[0] if not filtered_df_4_10.empty else None
        st.write(summary_value_4_10)
        # st.write("9~10점짜리 리뷰 요약글(df 연결 전)")
    elif selected_option == "⭐⭐⭐⭐":
        # 조건에 맞는 행 필터링
        filtered_df_4_8 = df[(df['movie_id'] == 4) & (df['rating'] == 8)]
        # summary 값 추출
        summary_value_4_8 = filtered_df_4_8['summary'].iloc[0] if not filtered_df_4_8.empty else None
        st.write(summary_value_4_8)
        # st.write("9~10점짜리 리뷰 요약글(df 연결 전)")
    elif selected_option == "⭐⭐⭐":
        # 조건에 맞는 행 필터링
        filtered_df_4_6 = df[(df['movie_id'] == 4) & (df['rating'] == 6)]
        # summary 값 추출
        summary_value_4_6 = filtered_df_4_6['summary'].iloc[0] if not filtered_df_4_6.empty else None
        st.write(summary_value_4_6)
        # st.write("9~10점짜리 리뷰 요약글(df 연결 전)")
    elif selected_option == "⭐⭐":
        # 조건에 맞는 행 필터링
        filtered_df_4_4 = df[(df['movie_id'] == 4) & (df['rating'] == 4)]
        # summary 값 추출
        summary_value_4_4 = filtered_df_4_4['summary'].iloc[0] if not filtered_df_4_4.empty else None
        st.write(summary_value_4_4)
        # st.write("9~10점짜리 리뷰 요약글(df 연결 전)")
    else:
        # 조건에 맞는 행 필터링
        filtered_df_4_2 = df[(df['movie_id'] == 4) & (df['rating'] == 2)]
        # summary 값 추출
        summary_value_4_2 = filtered_df_4_2['summary'].iloc[0] if not filtered_df_4_2.empty else None
        st.write(summary_value_4_2)
        # st.write("9~10점짜리 리뷰 요약글(df 연결 전)")