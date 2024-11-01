import streamlit as st

st.set_page_config(page_title="FilmRateTrust AI", page_icon="data/ai_icon.webp", layout="centered", initial_sidebar_state="auto", menu_items=None)

# 홈 목록
home = st.Page("pages/home.py", title="FilmRateTrust AI 소개", default=True)

# 영화 목록
notebook = st.Page("pages/notebook.py", title="노트북 (2004)")
konan = st.Page("pages/master.py", title="타짜: 원 아이드 잭 (2019)")
veteran = st.Page('pages/veteran.py', title="베테랑2 (2024)")
joker = st.Page('pages/joker.py', title="조커: 폴리 아 되 (2024)")
family = st.Page('pages/family.py', title="가문의 영광: 리턴즈 (2023)")

pg = st.navigation(
    {
        "홈": [home],
        "영화 목록": [notebook, konan, veteran, joker, family],
    }
)
pg.run()

with st.sidebar:
    st.markdown("[감성 분석 계산식 확인하러 가기](https://github.com/heeaejenn/film-rate-trust-ai/blob/main/README.md) 💡")
