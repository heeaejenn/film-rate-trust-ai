import pymysql
import pandas as pd
import os
from DataCreator import DataCreator
from contextlib import closing

class ReviewPredictor:
    def __init__(self, db_config):
        self.host = db_config['DB_HOST']
        self.port = int(db_config['DB_PORT'])
        self.user = db_config['DB_USER']
        self.passwd = db_config['DB_PASSWD']
        self.db_name = db_config['DB_NAME']
        self.df = None
        self.model_path = '3_ver1.pt'

    def connect_to_db(self):
        """Connect to the database and return the connection object."""
        return pymysql.connect(
            host=self.host,
            port=self.port,
            user=self.user,
            passwd=self.passwd,
            db=self.db_name,
            charset="utf8",
        )

    def fetch_reviews(self):
        """Fetch reviews from the database and store them in a DataFrame."""
        db = self.connect_to_db()
        cursor = db.cursor()

        # SQL query to select data
        sql = "SELECT * FROM reviews;"
        cursor.execute(sql)

        # Get column names
        column_names = [i[0] for i in cursor.description]

        # Fetch all results
        results = cursor.fetchall()

        # Convert results to a DataFrame
        self.df = pd.DataFrame(results, columns=column_names)

        # Close the database connection
        db.close()

    def predict_sentiment(self):
        """Predict sentiment using the DataCreator class."""
        if self.df is None:
            raise ValueError("DataFrame is empty. Please fetch reviews first.")

        # Initialize DataCreator with the DataFrame and model path
        data_creator = DataCreator(self.df, self.model_path)

        # Get the number of samples
        num_samples = len(data_creator.df)

        # Predict sentiment
        result = data_creator.predict_sentiment(num_samples)

        return result

    def insert_reviews(self, data):
        try:
            with closing(pymysql.connect(
                    host=self.host,
                    port=self.port,
                    user=self.user,
                    passwd=self.passwd,
                    db=self.db_name,
                    charset="utf8",
            )) as db:
                with db.cursor() as cursor:
                    for _, row in data.iterrows():
                        sentiment_score = row['sentiment_score']
                        new_rating = row['new_rating']
                        review_text = row['review']  # 리뷰 텍스트를 고유 식별자로 사용

                        # 특정 리뷰에 대해 sentiment_score와 new_rating 값을 업데이트
                        sql = """
                        UPDATE reviews
                        SET new_rating = %s, sentiment_score = %s
                        WHERE review = %s;
                        """
                        cursor.execute(sql, (new_rating, sentiment_score, review_text))

                    # 변경사항 커밋
                    db.commit()
        except Exception as e:
            print(f"Error occurred: {e}")
            if 'db' in locals():
                db.rollback()








