from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from dotenv import load_dotenv
import pymysql
import os
import sys

# 환경변수 로드
load_dotenv()

# 필요한 환경변수 변수에 저장
host = os.getenv('DB_HOST')
port = os.getenv('DB_PORT')
user = os.getenv('DB_USER')
passwd = os.getenv('DB_PASSWD')
db_name = os.getenv('DB_NAME')

# chain 생성
model = ChatOpenAI(
    model="gpt-4o-mini",
    temperature=0,
)

prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "사용자 말투를 살려서 입력하는 리뷰 데이터를 요약하여 5줄로 출력하세요"),
        ("human", "{reviews}"),
    ]
)

chain = prompt | model | StrOutputParser()

# 리뷰 요약
def summarize(reviews):
    summary = chain.invoke({"reviews": reviews})
    return summary

# 구간별 리뷰를 요약 후 DB 작성
def summarize_all(title):
    db = pymysql.connect(
        host=host,
        port=int(port),
        user=user,
        passwd=passwd,
        db=db_name,
        charset="utf8",
    )
    cursor = db.cursor()

    # title의 movie_id 검색
    id_sql = f"""select id from movie where title='{title}';"""
    cursor.execute(id_sql)
    movie_id = cursor.fetchone()[0]

    # reviews 테이블의 review column 가져오기
    cursor.execute(f"SELECT review FROM reviews WHERE movie_id={movie_id} AND new_rating >= 0 AND new_rating < 2;")
    new0to2 = cursor.fetchall()

    cursor.execute(f"SELECT review FROM reviews WHERE movie_id={movie_id} AND new_rating >= 2 AND new_rating < 4;")
    new2to4 = cursor.fetchall()

    cursor.execute(f"SELECT review FROM reviews WHERE movie_id={movie_id} AND new_rating >= 4 AND new_rating < 6;")
    new4to6 = cursor.fetchall()

    cursor.execute(f"SELECT review FROM reviews WHERE movie_id={movie_id} AND new_rating >= 6 AND new_rating < 8;")
    new6to8 = cursor.fetchall()

    cursor.execute(f"SELECT review FROM reviews WHERE movie_id={movie_id} AND new_rating >= 8 AND new_rating <= 10;")
    new8to10 = cursor.fetchall()

    # 가공하기 쉽도록 처리
    new0to2 = [line[0] for line in new0to2]
    new2to4 = [line[0] for line in new2to4]
    new4to6 = [line[0] for line in new4to6]
    new6to8 = [line[0] for line in new6to8]
    new8to10 = [line[0] for line in new8to10]

    reviews = [new0to2, new2to4, new4to6, new6to8, new8to10]
    summary = []

    for review in reviews:
        summary.append(summarize(review))

    # summary insert 
    for i, summarized_review in enumerate(summary):
        insert_sql = f"""insert into summarized_reviews (movie_id, rating, summary) values ({movie_id}, {i * 2 + 2}, "{summarized_review}");"""
        cursor.execute(insert_sql)

    db.commit()
    db.close()

if __name__ == "__main__":
    if len(sys.argv) > 1:
        argument = sys.argv[1]
        summarize_all(argument)
    else:
        print("No argument provided.")