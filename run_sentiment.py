import os
from DB_Creator import ReviewPredictor
from dotenv import load_dotenv


class SentimentPredictorApp:
    def __init__(self):
        # Load environment variables
        load_dotenv()

        # Set up database configuration from environment variables
        self.db_config = {
            'DB_HOST': os.getenv('DB_HOST'),
            'DB_PORT': os.getenv('DB_PORT'),
            'DB_USER': os.getenv('DB_USER'),
            'DB_PASSWD': os.getenv('DB_PASSWD'),
            'DB_NAME': os.getenv('DB_NAME')
        }

        # Create an instance of ReviewPredictor with the configuration
        self.predictor = ReviewPredictor(self.db_config)

    def run(self):
        # Fetch reviews from the database
        self.predictor.fetch_reviews()

        # Predict sentiment
        result = self.predictor.predict_sentiment()

        # Update the database with predictions for movie IDs 1 to 5
        for movie_id in range(1, 6):
            self.predictor.insert_reviews(result, movie_id)


if __name__ == "__main__":
    app = SentimentPredictorApp()
    app.run()
