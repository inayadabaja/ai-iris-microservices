from app.repositories.prediction_repository import PredictionRepository
from app.services.predictor import Predictor


class PredictionService:
    def __init__(
        self,
        prediction_repository: PredictionRepository,
        predictor: Predictor
    ):
        self.prediction_repository = prediction_repository
        self.predictor = predictor

    def create_prediction(self, db, features: dict):
        predicted_class = self.predictor.predict(features)

        prediction_record = {
            **features,
            "predicted_class": predicted_class
        }

        saved_prediction = self.prediction_repository.save_prediction(db, prediction_record)
        return saved_prediction