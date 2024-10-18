# from dotenv import load_dotenv
# from openai import OpenAI
import requests
from bs4 import BeautifulSoup
import re
import json
import pandas as pd


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
                return s[first_bracket : last_bracket + 1]

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


# 추출된 데이터 전처리 및 csv 파일 생성
def crawl_to_csv(title):
    df = make_movie_data(title)
    df["reviews"] = df["reviews"].apply(
        lambda x: re.sub(r"[^가-힣\s]", "", str(x)) if pd.notna(x) else x
    )

    # 빈 행 삭제 (한글만 남긴 후 빈 행이 생길 수 있음)
    df = df.dropna(subset=["reviews"])  # None 값 제거
    df = df[df["reviews"].str.strip() != ""]  # 공백만 있는 값 제거

    return df.to_csv(f"{title}_data.csv")


crawl_to_csv("비긴어게인")
