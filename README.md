# film-rate-trust-ai

## 사용된 패키지

1. **beautifulsoup4**
   - requests로 받아온 html정보를 파싱하여 필요한 정보를 추출하기 위해 사용 되었습니다.
   - [BeautifulSoup Documentation](https://www.crummy.com/software/BeautifulSoup/bs4/doc/)

2. **pymysql**
   - DB 연결 및 조회 및 추가를 위해 사용되었습니다.
   - [pymysql Documentation](https://pymysql.readthedocs.io/en/latest/)

3. **openai**
   - 주로 OpenAI API와의 통신을 위해 활용되며, GPT를 사용하기 위해 사용 되었습니다.
   - [OpenAI Documentation](https://beta.openai.com/docs/)
4. **langchain**
   - 프롬프트 체이닝을 통해 간단한 출력흐름을 구성하여 사용하기 위해 사용 되었습니다.
   - [LangChain Documentation](https://python.langchain.com/docs/)

## 함수 소개
```
get_cid(title):
   ...
   return cid

get_cid("베테랑2")
>> 142690
```
영화 제목을 인자로 받아 해당 인자의 검색 페이지에서 cid 속성을 추출합니다.

```
make_movie_data(title)
```
get_cid 함수로 추출한 cid를 사용해 영화 리뷰 정보를 크롤링합니다. star와 reviews열로 이루어진 DataFrame을 반환합니다.

```
crawl_to_db(title)
```
make_movie_data 함수로 반환된 DataFrame의 reviews열을 정규표현식을 사용하여 전처리합니다. 전처리 후 DB에 연결해 영화 제목, star, reviews를 DB에 입력합니다.


## 사용법
```
$ python movie_data_crawl.py [영화제목]
```