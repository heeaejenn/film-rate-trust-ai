import pandas as pd
import torch
import torch.nn.functional as F
from kobert_tokenizer import KoBERTTokenizer
from transformers import BertForSequenceClassification
import warnings

# 경고 메시지 출력 비활성화
warnings.simplefilter("ignore")

class SentimentPredictor:
    def __init__(self, model_path, device=None):
        # 장치 설정 (Apple M1/M2 장치에서는 GPU 사용 불가, CPU로 설정)
        if torch.backends.mps.is_available():
            self.device = torch.device("mps")  # Apple Silicon M1/M2용
        else:
            self.device = torch.device("cpu")  # 다른 장치용 CPU 설정

        # KoBERT 모델과 토크나이저 로드
        self.tokenizer = KoBERTTokenizer.from_pretrained('skt/kobert-base-v1')
        self.model = BertForSequenceClassification.from_pretrained('skt/kobert-base-v1', num_labels=2)

        # 모델 로드
        print(f'모델 로딩 {model_path}')
        self.model.load_state_dict(torch.load(model_path, map_location=self.device))
        self.model.to(self.device)

        # 평가 모드로 전환
        self.model.eval()

    def predict(self, text):
        # 입력 텍스트를 토큰화하고 모델로 예측 수행
        encoding = self.tokenizer(text, return_tensors='pt', padding='max_length', truncation=True, max_length=128)
        input_ids = encoding['input_ids'].to(self.device)
        attention_mask = encoding['attention_mask'].to(self.device)

        with torch.no_grad():
            outputs = self.model(input_ids=input_ids, attention_mask=attention_mask)
            logits = outputs.logits

            # 소프트맥스 함수로 확률 변환
            probabilities = F.softmax(logits, dim=-1)
            positive_prob = probabilities[0][1].cpu().item()  # 긍정 클래스의 확률

        return positive_prob
