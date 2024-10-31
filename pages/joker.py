import pymysql
import streamlit as st
import sys
import os
import pandas as pd


# 테스트 코드가 있는 디렉토리를 경로에 추가
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../visualizers')))

# selectbox, barchart 모듈 가져오기
from selectbox import *
from barchart import *
from sum_reviews import *

st.title('조커: 폴리 아 되 (2024)')
st.markdown('<span style="font-size: 18px;">네이버 리뷰 평점 별 관람평 요약</span>', unsafe_allow_html=True)
st.markdown("""
    <style>
    .custom-subheader {
        font-size: 20px; /* Increase font size */
        font-weight: bold; /* Make text bold */
        color: #333; /* Adjust color if needed */
        margin-bottom: 5px; /* Reduce space below the subheader */
    }
    .custom-divider {
        border: none;
        border-top: 1px solid gray; /* Gray divider line */
        margin-top: 0px; /* Reduce space above the divider */
        margin-bottom: 10px; /* Adjust space below the divider */
    }
    </style>
""", unsafe_allow_html=True)

# Use HTML for the subheader with custom class
st.markdown('<p class="custom-subheader">기본 정보</p>', unsafe_allow_html=True)

# Add a gray divider closer to the subheader
st.markdown('<hr class="custom-divider">', unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    st.image("data/movie_poster/joker.jpeg", width=225, use_column_width=False)
with col2:
    st.markdown("""
    <style>
    .info-table {
        font-family: Arial, sans-serif;
        font-size: 16px;
        line-height: 1.6;
    }
    .rating-section {
        margin-top: 20px;
        font-family: Arial, sans-serif;
        font-size: 16px;
    }
    .rating-score {
        font-weight: bold;
        font-size: 18px;
        color: #007BFF; /* Blue color for the rating score */
    }
    </style>

    <div class="info-table">
        <p><strong>개봉</strong> 2024.10.01.</p>
        <p><strong>등급</strong> 15세 이상 관람가</p>
        <p><strong>장르</strong> 범죄, 드라마, 뮤지컬</p>
        <p><strong>국가</strong> 미국</p>
        <p><strong>러닝타임</strong> 138분</p>
        <p><strong>배급</strong> 워너 브러더스 코리아㈜</p>
    </div>

    <div class="rating-section">
        <p><strong>실관람객 평점</strong> 6.25/10</p>
    </div>
    """, unsafe_allow_html=True)

# Custom CSS to change subheader font size and adjust divider spacing
st.markdown("""
    <style>
    .custom-subheader {
        font-size: 20px; /* Increase font size */
        font-weight: bold; /* Make text bold */
        color: #333; /* Adjust color if needed */
        margin-bottom: 5px; /* Reduce space below the subheader */
    }
    .custom-divider {
        border: none;
        border-top: 1px solid gray; /* Gray divider line */
        margin-top: 0px; /* Reduce space above the divider */
        margin-bottom: 10px; /* Adjust space below the divider */
    }
    </style>
""", unsafe_allow_html=True)

# Use HTML for the subheader with custom class
st.markdown('<p class="custom-subheader">관람평 분석</p>', unsafe_allow_html=True)

# Add a gray divider closer to the subheader
st.markdown('<hr class="custom-divider">', unsafe_allow_html=True)

df_reviews = connect_reviews_table()
chart_image = create_bar_chart(5, df_reviews)

selected_option = ranking_selectbox()
df_reviews = get_sum_reviews_tables(movie_id=5)
get_sum_review_by_ranking(df_reviews, selected_option)