import pymysql
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm

# 폰트 파일 경로 설정
font_path = r'data/Noto_Sans_KR/static/NotoSansKR-Regular.ttf'
font_prop = fm.FontProperties(fname=font_path)

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
    df = connect_reviews_table()  # 데이터프레임 가져오기
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
        
        # Determine the x-position for label text
        if height <= 8:  # Change to 8% for low percentages
            ax.text(0.45, bottom + height / 2, f'{height:.2f}%', ha='left', va='center', color='black', fontsize=30)  # Move to the right (adjusted)
            # Draw a line connecting the bar and label
            ax.plot([0, 0.45], [bottom + height / 2, bottom + height / 2], color='black', linestyle='--')
        else:
            ax.text(0, bottom + height / 2, f'{label}\n{height:.2f}%', ha='center', va='center', color='black', fontsize=30)  # Stay in the center
            
        bottom += height

    # Create the stacked bar for new rating
    bottom = 0
    for i, (label, color) in enumerate(zip(rating_labels, rating_colors)):
        height = new_counts[label] if label in new_counts else 0
        ax.bar(bars[1], height, bottom=bottom, color=color)

        # Determine the x-position for label text
        if height <= 8:  # Change to 8% for low percentages
            ax.text(1.35, bottom + height / 2, f'{height:.2f}%', ha='left', va='center', color='black', fontsize=30)  # Move to the right (adjusted)
            # Draw a line connecting the bar and label
            ax.plot([1, 1.35], [bottom + height / 2, bottom + height / 2], color='black', linestyle='--')
        else:
            ax.text(1, bottom + height / 2, f'{label}\n{height:.2f}%', ha='center', va='center', color='black', fontsize=30)  # Stay in the center
            
        bottom += height

    # Set x-tick labels and adjust font size
    ax.set_xticks(range(len(bars)))  # Set x-ticks to the positions of the bars
    ax.set_xticklabels(bars, fontsize=30)  # Set font size for x-tick labels

    # Set y-tick labels font size
    ax.tick_params(axis='y', labelsize=25)  # Increase y-axis tick labels font size

    # Customize chart title using if conditions
    if movie_id == 1:
        title = 'Rating Distribution Comparison for 베테랑2'
    elif movie_id == 2:
        title = 'Rating Distribution Comparison for 가문의 영광'
    elif movie_id == 3:
        title = 'Rating Distribution Comparison for 타짜'
    elif movie_id == 4:
        title = 'Rating Distribution Comparison for 노트북'
    elif movie_id == 5:  
        title = 'Rating Distribution Comparison for 조커'
    else:
        title = '영화 못찾음'

    # Set title using plt.suptitle()
    plt.suptitle(title, fontsize=40, fontproperties=font_prop, y=0.93)

    ax.set_ylabel('Percentage of Reviews', fontsize=30)  # Increased font size for y-axis label
    return st.pyplot(fig)