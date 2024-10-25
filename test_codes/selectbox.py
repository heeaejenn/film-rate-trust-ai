import streamlit as st
import pandas as pd

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

## sql DB 연결

# Initialize connection.
conn = st.connection('mysql', type='sql')
# Perform query.
df = conn.query('SELECT * from summarized_reviews;', ttl=600)

def ranking_selectbox():
    option = st.selectbox(
        "평점 요약 확인하기:",
        data_df)
    return option


