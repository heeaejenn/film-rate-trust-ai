from KoBERT_Sentiment import *
import pandas as pd

class DataCreator:
    def __init__(self, local_data, model_save_path):
        # 데이터 로드 및 전처리
        self.data = pd.read_csv(local_data)
        self.df = self.data.rename(columns={'Unnamed: 0': 'index', 'sentiment': 'label', 'reviews': 'document'})
        self.df = self.df.drop('index', axis=1)
        self.df = self.df.dropna(how='any')
        self.df['label'] = self.df['label'].astype(int)
        self.df.drop_duplicates(subset=['document'], inplace=True)

        # 모델 설정
        self.model_save_path = model_save_path
        self.sentiment_predictor = SentimentPredictor(self.model_save_path)

    def predict_sentiment(self, num_samples=100):
        # 예시 문장 리스트
        example_sentences = self.df['document'].tolist()[:num_samples]
        results = []

        # 각 문장에 대해 예측 수행
        for sentence in example_sentences:
            positive_probability = self.sentiment_predictor.predict(sentence)
            results.append({"문장": sentence, "긍정 확률": positive_probability})

        # 결과 데이터프레임 생성
        results_df = pd.DataFrame(results)

        # 결과에 대한 추가 계산
        results_df['star'] = self.df['star'][:num_samples].reset_index(drop=True)
        results_df['result'] = results_df['긍정 확률'] * results_df['star']
        results_df['result'] = round(results_df['result'])

        return results_df
