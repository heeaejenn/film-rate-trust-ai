from KoBERT_Sentiment import *
import pandas as pd

class DataCreator:
    def __init__(self, data, model_save_path):
        # 데이터 로드 및 전처리
        self.df = data

        # 모델 설정
        self.model_save_path = model_save_path
        self.sentiment_predictor = SentimentPredictor(self.model_save_path)

    def predict_sentiment(self, num_samples=100):
        # 예시 문장 리스트
        example_sentences = self.df['review'].tolist()[:num_samples]
        results = []

        # 각 문장에 대해 예측 수행
        for sentence in example_sentences:
            positive_probability = self.sentiment_predictor.predict(sentence)
            results.append({"review": sentence, "sentiment_score": positive_probability})

        # 결과 데이터프레임 생성
        results_df = pd.DataFrame(results)

        # 결과에 대한 추가 계산
        results_df['id']=self.df['id'][:num_samples].reset_index(drop=True)
        results_df['movie_id']=self.df['movie_id'][:num_samples].reset_index(drop=True)
        results_df['original_rating'] = self.df['original_rating'][:num_samples].reset_index(drop=True)
        results_df['new_rating'] = ((results_df['sentiment_score']*10*2) + (results_df['original_rating']*1))/(1+2)
        results_df['new_rating'] = round(results_df['new_rating'])

        return results_df
