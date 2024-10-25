import sys
import requests
from bs4 import BeautifulSoup
import re
import json
import pandas as pd
import pymysql
import os
from dotenv import load_dotenv

load_dotenv()

# 영화 cid 추출
def get_cid(title):
    url = f"https://search.naver.com/search.naver?where=nexearch&sm=tab_etc&pkid=68&qvt=0&query={title}"

    res = requests.get(url)
    soup = BeautifulSoup(res.text, "html.parser")

    cid = soup.select_one("div.button_like").attrs["data-cid"]
    return cid


# 영화 데이터 추출
def make_movie_data(title):
    cid = get_cid(title)
    page = 1
    star_rate = []
    reviews_data = []
    while True:
        url = f"https://m.search.naver.com/p/csearch/content/nqapirender.nhn?where=nexearch&pkid=68&fileKey=movieKBPointAPI&u1={cid}&u5=true&_callback=_nexearch_where_68_pkid_movieKBPointAPI_fileKey_{cid}_u1_true_u5_newest_u3_true_u4_2_u2&u3=newest&u4=true&u2={page}"
        response = requests.get(url)
        text = response.text
        text = text.replace("\\", "")

        # 해당 페이지에 리뷰가 있는지 확인
        # 중괄호와 그 안의 내용 추출 (개행 문자 포함)
        match = re.search(r"\{.*?\}", text, re.DOTALL)

        if match:
            json_str = match.group()  # 중괄호 안의 내용
            try:
                # 추출한 문자열을 딕셔너리로 변환
                json_dict = json.loads(json_str)
                if json_dict["html"] == "":
                    break
            except json.JSONDecodeError:
                pass
        else:
            print("중괄호 안의 내용을 찾을 수 없습니다.")

        # requests로 불러온 text 파싱 가능하게 변경
        def extract_substring(s):
            # 첫번째 '<'의 인덱스와 마지막 '>'의 인덱스 찾기
            first_bracket = s.find("<")
            last_bracket = s.rfind(">")

            # 인덱스가 유효하면 해당 부분 문자열 추출
            if (
                    first_bracket != -1
                    and last_bracket != -1
                    and first_bracket < last_bracket
            ):
                return s[first_bracket: last_bracket + 1]

        a = extract_substring(text)

        soup = BeautifulSoup(a, "html.parser")

        div = soup.find_all("div", class_="area_text_box")

        star_tag = [i.get_text(strip=True, separator=" ") for i in div]

        reviews = soup.select("span.desc._text")
        for r in reviews:
            reviews_data.append(r.text)

        for s in star_tag:
            star_rate.append(s[-2:].strip())
        page += 1

    df = pd.DataFrame({"star": star_rate, "reviews": reviews_data})

    return df


# 추출된 데이터 전처리 및 db저장
def crawl_to_db(title):
    df = make_movie_data(title)
    df["reviews"] = df["reviews"].apply(
        lambda x: re.sub(r"[^가-힣\s]", "", str(x)) if pd.notna(x) else x
    )

    # 빈 행 삭제 (한글만 남긴 후 빈 행이 생길 수 있음)
    df = df.dropna(subset=["reviews"])  # None 값 제거
    df = df[df["reviews"].str.strip() != ""]  # 공백만 있는 값 제거

    host = os.getenv('DB_HOST')
    port = os.getenv('DB_PORT')
    user = os.getenv('DB_USER')
    passwd = os.getenv('DB_PASSWD')
    db_name = os.getenv('DB_NAME')

    con = pymysql.connect(
        host=host,
        port=int(port),
        user=user,
        passwd=passwd,
        db=db_name,
        charset="utf8",
    )

    cur = con.cursor()

    # movie 테이블에 title 컬럼에 입력받은 영화 제목 추가
    add_movie_query = f"insert into movie (title) values ('{title}');"
    cur.execute(add_movie_query)

    # movie_id 검색
    movie_id_query = f"select id from movie where title='{title}';"

    # 검색한 값 확인
    cur.execute(movie_id_query)
    movie_id = cur.fetchone()

    # df의 reviews와 star 열 값을 db의  insert original_rating, review 행에 추가
    for star, review in zip(df["star"], df["reviews"]):
        insert_query = f"INSERT INTO reviews (movie_id, original_rating, review) VALUES ({movie_id[0]}, {star}, '{review}');"
        cur.execute(insert_query)

    con.commit()
    con.close()

if __name__ == "__main__":
    if len(sys.argv) > 1:
        argument = sys.argv[1]
        crawl_to_db(argument)
    else:
        print("No argument provided.")