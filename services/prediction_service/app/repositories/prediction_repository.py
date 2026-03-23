from sqlalchemy.orm import Session

from app.models.prediction_model import Prediction


class PredictionRepository:
    def save_prediction(self, db: Session, data: dict) -> Prediction:
        prediction = Prediction(**data)
        db.add(prediction)
        db.commit()
        db.refresh(prediction)
        return prediction

    def get_all_predictions(self, db: Session) -> list[Prediction]:
        return db.query(Prediction).order_by(Prediction.id.desc()).all()