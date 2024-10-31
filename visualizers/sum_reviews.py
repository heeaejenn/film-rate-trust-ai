import pymysql
import streamlit as st
import sys
import os
import pandas as pd

def get_sum_reviews_tables(movie_id=None):

    # 데이터베이스 연결 설정
    conn = pymysql.connect(
        host=st.secrets["mysql"]["host"],
        port=st.secrets["mysql"]["port"],
        user=st.secrets["mysql"]["user"],
        password=st.secrets["mysql"]["password"],
        database=st.secrets["mysql"]["database"]
    )

    try:
        # 데이터베이스 작업 수행
        with conn.cursor() as cursor:
            # SQL 쿼리 작성: movie_id가 제공된 경우 해당 값을 기준으로 필터링
            if movie_id is not None:
                query = 'SELECT * FROM summarized_reviews WHERE movie_id = %s;'
                cursor.execute(query, (movie_id,))
            else:
                query = 'SELECT * FROM summarized_reviews;'
                cursor.execute(query)
                
            result_reviews = cursor.fetchall()
            df_reviews = pd.DataFrame(result_reviews, columns=[col[0] for col in cursor.description])

    finally:
        # 데이터베이스 연결 닫기
        conn.close()

    return df_reviews

def get_sum_review_by_ranking(df_reviews, selected_option):
    if st.button("조회하기"):
        if selected_option == "⭐⭐⭐⭐⭐":
            # rating이 10인 summary 값을 리스트로 변환
            summary_10 = df_reviews[df_reviews['rating'] == 10]['summary'].tolist()
            # 각 summary 값을 문자열로 출력
            for summary in summary_10:
                st.write(summary)
        elif selected_option == "⭐⭐⭐⭐":
            summary_8 = df_reviews[df_reviews['rating'] == 8]['summary'].tolist()
            for summary in summary_8:
                st.write(summary)
        elif selected_option == "⭐⭐⭐":
            summary_6 = df_reviews[df_reviews['rating'] == 6]['summary'].tolist()
            for summary in summary_6:
                st.write(summary)
        elif selected_option == "⭐⭐":
            summary_4 = df_reviews[df_reviews['rating'] == 4]['summary'].tolist()
            for summary in summary_4:
                st.write(summary)
        else:
            summary_2 = df_reviews[df_reviews['rating'] == 2]['summary'].tolist()
            for summary in summary_2:
                st.write(summary)
