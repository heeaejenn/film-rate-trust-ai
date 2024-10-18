# from dotenv import load_dotenv
# from openai import OpenAI
import requests
from bs4 import BeautifulSoup
import re
import json
import pandas as pd


def get_cid(title):
    url = f"https://search.naver.com/search.naver?where=nexearch&sm=tab_etc&pkid=68&qvt=0&query={title}"

    res = requests.get(url)
    soup = BeautifulSoup(res.text, "html.parser")

    cid = soup.select_one("div.button_like").attrs["data-cid"]
    return cid


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


# load_dotenv()
# client = OpenAI()

# system_prompt = """리뷰 감정 분석이 필요합니다.
# 긍정 또는 부정으로 판단해주세요.
# 긍정이면 값이 1 이고, 부정이면 0 으로 표현하면 됩니다.
# 여러개의 영화 리뷰를 감정 분석하여 리뷰별로 출력하세요.
# json 형식으로 출력해주세요."""


# def sentiment_data(review, system_prompt=system_prompt, num=0, retry=True):
#     user_prompt = ""
#     for i, r in enumerate(review, 1):
#         user_prompt += f"review_{num + i}: {r}\n"
#     response = client.chat.completions.create(
#         model="gpt-4o-mini",
#         messages=[
#             {"role": "system", "content": system_prompt},
#             {
#                 "role": "user",
#                 "content": """
#             {'review_1': '영화가 너무 재밌어요. 추천합니다.', 'review_2': '이 영화는 별로에요. 추천하지 않아요.'}
#             """,
#             },
#             {"role": "assistant", "content": '{"review_1": 1, "review_2": 0}'},
#             {"role": "user", "content": user_prompt},
#         ],
#         response_format={"type": "json_object"},
#         temperature=0,
#     )

#     sentiment_result = response.choices[0].message.content
#     try:
#         sentiment_result = json.loads(sentiment_result)
#         return sentiment_result
#     except json.JSONDecodeError as e:
#         if retry:
#             return sentiment_data(review, system_prompt, num, retry=False)
#         else:
#             print(e)


title = "베테랑2"

df = make_movie_data(title)
reviews = [i for i in df["reviews"]]

result_data = {}
chunk_size = 10

# for r in range(0, len(reviews), chunk_size):
#     result = sentiment_data(reviews[r : r + chunk_size], num=r)
#     result_data.update(result)
#     print(len(result))

# sentiment_values = [v for v in result_data.values()]
# df["sentiment"] = sentiment_values


# 1. 'reviews' 열에서 빈칸(공백문자 포함) 또는 NaN인 행 제거
df["reviews"] = df["reviews"].replace(
    r"^\s*$", None, regex=True
)  # 빈 문자열을 None으로 변환
df = df.dropna(subset=["reviews"])  # NaN 값 제거

# 2. 'reviews' 열의 각 값에서 구두점 제거
df["reviews"] = df["reviews"].apply(lambda x: re.sub(r"[^가-힣0-9\s]", "", x))

df.to_csv(f"{title}_movie_sentiment.csv")
