# film-rate-trust-ai

## 사용된 패키지

1. **requests**
   - cid와 비동기 정보들을 http 요청으로 받아오기 위해 사용되었습니다.
   - [Requests Documentation](https://docs.python-requests.org/en/latest/)

2. **beautifulsoup4**
   - requests로 받아온 html정보를 파싱하여 필요한 정보를 추출하기 위해 사용 되었습니다.
   - [BeautifulSoup Documentation](https://www.crummy.com/software/BeautifulSoup/bs4/doc/)

3. **pandas**
   - 크롤링 한 정보들을 DataFrame으로 만들어 전처리한 후 CSV 파일로 저장하기 위해 사용됩니다.
   - [Pandas Documentation](https://pandas.pydata.org/pandas-docs/stable/)

4. **json**
   - 비동기 정보들을 JSON 형식으로 인코딩하기 위해 사용됩니다. 
   - [JSON Documentation](https://docs.python.org/3/library/json.html)

5. **re**
   - 정규 표현식을 사용하여 텍스트 데이터를 정제하기 위해 사용됩니다.
   - [re Documentation](https://docs.python.org/3/library/re.html)


## 함수 소개
```
get_cid(title)
```
영화 제목을 인자로 받아 검색어에 할당 된 cid를 추출합니다.

```
make_movie_data(title)
```
get_cid 함수로 추출한 cid를 사용해 비동기 정보를 크롤링합니다. star와 reviews열로 이루어진 DataFrame을 반환합니다.

```
crawl_to_csv(title)
```
make_movie_data 함수로 반환된 DataFrame의 reviews열을 정규표현식을 사용하여 전처리합니다. 전처리 후 csv 파일로 저장합니다.


## 사용법
```
$ python movie_data_crawl.py [영화제목]
```