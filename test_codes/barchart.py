import pymysql
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm

def connect_reviews_table():
    # 데이터베이스 연결 설정
    conn = pymysql.connect(
        host=st.secrets["mysql"]["host"],
        port=st.secrets["mysql"]["port"],
        user=st.secrets["mysql"]["user"],
        password=st.secrets["mysql"]["password"],
        database=st.secrets["mysql"]["database"])

    try:
        # 데이터베이스 작업 수행
        with conn.cursor() as cursor:
            cursor.execute('SELECT * FROM reviews;')
            result = cursor.fetchall()
            # DataFrame 생성
            df = pd.DataFrame(result, columns=[col[0] for col in cursor.description])
    finally:
        # 데이터베이스 연결 닫기
        conn.close()

    # movie_id, original_rating, new_rating 열을 숫자로 변환
    df['movie_id'] = pd.to_numeric(df['movie_id'], errors='coerce')
    df['original_rating'] = pd.to_numeric(df['original_rating'], errors='coerce')
    df['new_rating'] = pd.to_numeric(df['new_rating'], errors='coerce')

    return df

def create_bar_chart(movie_id, df):

    connect_reviews_table()
    # Filter for movie_id 1
    # df_movie = df[df['movie_id'] == 1]
    df_movie = df[df['movie_id'] == movie_id]

    # Define rating ranges
    rating_bins = [0, 2, 4, 6, 8, 10]
    rating_labels = ['0~2', '3~4', '5~6', '7~8', '9~10']

    # Group by rating ranges for both original and new ratings
    df_movie['original_rating_range'] = pd.cut(df_movie['original_rating'], bins=rating_bins, labels=rating_labels, right=True)
    df_movie['new_rating_range'] = pd.cut(df_movie['new_rating'], bins=rating_bins, labels=rating_labels, right=True)

    # Calculate the percentage of each rating range
    original_counts = df_movie['original_rating_range'].value_counts(normalize=True).sort_index() * 100
    new_counts = df_movie['new_rating_range'].value_counts(normalize=True).sort_index() * 100

    # Plotting
    fig, ax = plt.subplots(figsize=(24, 16))

    # Stacked bar chart
    rating_colors = ['#3498db', '#2ecc71', '#f1c40f', '#e67e22', '#e74c3c']
    bars = ['Original Rating', 'New Rating']

    # Create the stacked bar for original rating
    bottom = 0
    for i, (label, color) in enumerate(zip(rating_labels, rating_colors)):
        height = original_counts[label] if label in original_counts else 0
        ax.bar(bars[0], height, bottom=bottom, color=color, label=label if i == 0 else "")
        ax.text(bars[0], bottom + height / 2, f'{label}\n{height:.2f}%', ha='center', va='center', color='black', fontsize=30)
        bottom += height

    # Create the stacked bar for new rating
    bottom = 0
    for i, (label, color) in enumerate(zip(rating_labels, rating_colors)):
        height = new_counts[label] if label in new_counts else 0
        ax.bar(bars[1], height, bottom=bottom, color=color)
        ax.text(bars[1], bottom + height / 2, f'{label}\n{height:.2f}%', ha='center', va='center', color='black', fontsize=30)
        bottom += height

    # Set x-tick labels and adjust font size
    ax.set_xticks(range(len(bars)))  # Set x-ticks to the positions of the bars
    ax.set_xticklabels(bars, fontsize=30)  # Set font size for x-tick labels

    # 폰트 설정
    plt.rc('font', family='NanumGothic')  # 또는 'Malgun Gothic'
    plt.rcParams['axes.unicode_minus'] = False  # 한글 폰트 사용 시 마이너스 기호 깨짐 방지

    # Customize chart
    ax.set_ylabel('Percentage of Reviews', fontsize=25)
    if movie_id == 1:
        ax.set_title('Rating Distribution Comparison for 베테랑2', fontsize=35)
    elif movie_id == 2:
        ax.set_title('Rating Distribution Comparison for 노트북', fontsize=35)
    elif movie_id == 3:
        ax.set_title('Rating Distribution Comparison for 명탐정 코난', fontsize=35)
    elif movie_id == 4:
        ax.set_title('Rating Distribution Comparison for 조커', fontsize=35)
    elif movie_id == 5:
        ax.set_title('Rating Distribution Comparison for 가문의 영광', fontsize=35)
    else:
        ax.set_title('영화 못찾음', fontsize=30)

    return st.pyplot(fig)

