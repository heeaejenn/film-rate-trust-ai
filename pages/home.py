import streamlit as st

st.title('FilmRateTrust AI')
st.subheader('영화 관람평 평가 AI')

st.markdown('<span style="font-size: 18px;">위 5가지 영화에 대한 네이버 관람평 요약본을 확인해보세요!</span>', unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)

with col1:
    st.image("data/movie_poster/notebook.jpeg", width=300, use_column_width=True)
    st.page_link("pages/notebook.py", label="[1위] 노트북 (2004)")

with col2:
    st.image("data/movie_poster/master.jpeg", width=300, use_column_width=True)
    st.page_link("pages/master.py", label="[2위] 타짜: 원 아이드 잭 (2024)")

with col3:
    st.image("data/movie_poster/veteran.jpeg", width=300, use_column_width=True)
    st.page_link("pages/veteran.py", label="[3위] 베테랑2 (2024)")

col4, col5, col6 = st.columns(3)

with col4:
    st.image("data/movie_poster/joker.jpeg", width=300, use_column_width=True)
    st.page_link("pages/joker.py", label="[4위] 조커: 폴리 아 되 (2024)")

with col5:
    st.image("data/movie_poster/family.jpeg", width=300, use_column_width=True)
    st.page_link("pages/family.py", label="[5위] 가문의 영광: 리턴즈 (2023)")

with col6:
    st.image("data/movie_poster/blank_space.png", width=300, use_column_width=True)

