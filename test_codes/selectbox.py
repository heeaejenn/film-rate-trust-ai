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


def ranking_selectbox():
    option = st.selectbox(
        "평점 요약 확인하기:",
        data_df)
    return option


