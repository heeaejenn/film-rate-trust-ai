import pandas as pd
import streamlit as st

### SQL DB 연결

# Initialize connection.
# conn = st.connection('mysql', type='sql')
# # Perform query.
# summarized_reviews_db = conn.query('SELECT * from summarized_reviews;', ttl=600)


data_df = pd.DataFrame(
    {
        "ranking": [
            "⭐⭐⭐⭐⭐",
            "⭐⭐⭐⭐",
            "⭐⭐⭐",
            "⭐⭐",
            "⭐"
        ],
    }
)

def ranking_selectbox():
    option = st.selectbox(
        "평점 요약 확인하기:",
        data_df)

    if st.button("조회하기"):
        if option == "⭐⭐⭐⭐⭐":
            st.write("9~10점짜리 요약글~~")
        elif option == "⭐⭐⭐⭐":
            st.write("7~8점짜리 요약글~")
        elif option == "⭐⭐⭐":
            st.write("5~6점짜리 요약글~")    
        elif option == "⭐⭐":
            st.write("3~4점짜리 요약글~")  
        else:
            st.write("0~2점짜리 요약글~")