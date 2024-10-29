### sidebar 내용

with st.sidebar:
    option = st.selectbox(
        "영화를 선택해주세요:",
        ("옵션 선택","노트북", "명탐정 코난", "베테랑2", "조커","가문의 영광"))

    if st.button("조회하기"):
        if option != "옵션 선택":
            if option == '노트북':
                st.switch_page("pages/notebook.py")
            elif option == '명탐정 코난':
                st.switch_page("pages/konan.py")
            elif option == '베테랑2':
                st.switch_page("pages/veteran.py")
            elif option == '조커':
                st.switch_page("pages/joker.py")
            else:
                st.switch_page("pages/family.py")

        else:
            st.write("영화를 선택해주세요.")