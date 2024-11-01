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

5. **streamlit**
   - 웹 애플리케이션을 쉽게 만들고 데이터 시각화 및 사용자 인터페이스 구축을 지원합니다.
   - [Streamlit Documentation](https://docs.streamlit.io/)
     
6. **matplotlib**
   - 데이터 시각화를 위한 그래프와 차트를 생성하여 영화 리뷰 분석 결과를 직관적으로 전달합니다.
   - [Matplotlib Documentation](https://matplotlib.org/stable/index.html)
  
7. **pandas**
   - 영화 리뷰 데이터를 로드하고 전처리하며, DataFrame 형식으로 구조화하여 데이터 변환 및 조작을 용이하게 합니다.
   - [Pandas Documentation](https://pandas.pydata.org/docs/)


## 사용된 모델
1. **KoBERT**
   - 네이버 영화 리뷰 20만 건 데이터를 이용해 학습시키고 비긴어게인 데이터 7,490건을 테스트 데이터로 활용
   - 성능 평가 결과
     val 정확도: 89%
     test 정확도: 94%

## 별점과 감성 분석 점수 계산

### FilmRateTrust AI의 새로운 점수 기준

#### 새로운 점수 계산식
![새로운 점수 계산식](https://github.com/user-attachments/assets/897d1f95-332a-46c6-bd39-fa6909e7e204)

    예시 1: 원래 별점 2점, 감성 예측 결과 0.18점:

![예시1](https://github.com/user-attachments/assets/89b58869-884e-4977-9cad-5b93cbd6c764)

    예시 2: 원래 별점 5점, 감성 예측 결과 0.40점: 

![예시2](https://github.com/user-attachments/assets/93b5efa6-52a2-4053-9384-bc569ba59b32)

**Streamlit에 표현되는 별점 기준**

| 새로운 별점 | 새로운 점수 구간 |
|-------------|------------------|
| 1점         | 0-2              |
| 2점         | 2-4              |
| 3점         | 4-6              |
| 4점         | 6-8              |
| 5점         | 8-10             |


## 사용법
```
$ python movie_data_crawl.py [영화제목]
$ run_sentiment.py 
```

## 함수 소개
1. **movie_data_crawl.py**
   - 영화 리뷰 데이터 크롤링
   - DB 접근 후 영화 제목, 원래 별점, 리뷰 입력
     
2. **KoBERT_Sentiment.py**
   - 데이터 로드 및 전처리 진행
   - 학습한 모델 불러오기
   - 모델 적용 및 긍정 확률 반환
     
3. **Data_Creator.py**
   - KoBERT_sentiment 불러오기
   - sentiment_score, new_rating 적용한 데이터프레임 반환
     
4. **DB_Creator.py**
   - DB 접근 및 데이터 불러오기
   - Data_Creator 불러오기
   - DB에 sentiment_score,new_rating 업데이트
     
5. **summarized.py**
   - 새로운 별점으로 분류된 리뷰 요약 진행
     
6. **main.py**
   - 페이지 제목, 아이콘, 레이아웃 설정
   - 홈 페이지 및 영화별 페이지 생성
   - 홈과 영화 목록을 위한 내비게이션 메뉴 설정
     
7. **pages/home.py**
   - 영화 제목 및 서브헤더 설정
   - 네이버 관람평 요약본 안내
   - 영화 포스터와 관련 페이지 링크 생성
     
8. **pages/family.py ~ 나머지 .py**
   - 영화 제목 및 설명 설정
   - 영화 기본 정보 및 포스터 표시
   - 관람평 분석을 위한 데이터베이스 연결 및 차트 생성
   - 관람객 평점 및 관람평 요약 선택 기능 제공
     
9. **visualizers/barchart.py**
   - 데이터베이스 연결 및 데이터 가져오기
   - 바 차트 생성 로직
   - 디스플레이 기능
     
10. **visualizers/selectbox.py**
   - 평점 요약 선택 상자 표시
   - 데이터프레임 생성
   - 사용자 선택 옵션 반환
     
11. **visualizers/sum_reviews.py**
   - 영화 리뷰 데이터베이스 연결
   - 영화 ID에 따른 리뷰 요약 조회
   - 평점별 요약 리뷰 표시


