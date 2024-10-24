import streamlit as st

# 홈 목록
home = st.Page("pages/home.py", title="FilmRateTrust AI 소개", default=True)

# 영화 목록
notebook = st.Page("pages/notebook.py", title="노트북 (2004)")
konan = st.Page("pages/konan.py", title="명탐정 코난 (2024)")
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