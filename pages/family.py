import streamlit as st
from test_codes.selectbox import *

st.set_page_config(page_title="FilmRateTrust AI", page_icon="data/ai_icon.webp", layout="centered", initial_sidebar_state="auto", menu_items=None)

st.title('가문의 영광: 리턴즈 (2023)')
st.markdown('<span style="font-size: 18px;">네이버 리뷰 평점 별 관람평 요약</span>', unsafe_allow_html=True)

st.image("data/movie_poster/family.jpeg", width=200, use_column_width=False)

ranking_selectbox()