from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import app_engine, AppSessionLocal
from app.models.prediction_model import Base
from app.models.feedback_model import Feedback
from app.schemas.prediction_request import PredictionRequest
from app.schemas.prediction_response import PredictionResponse
from app.schemas.feedback_schema import FeedbackRequest, FeedbackResponse
from app.repositories.prediction_repository import PredictionRepository
from app.repositories.feedback_repository import FeedbackRepository
from app.services.predictor import Predictor
from app.services.prediction_service import PredictionService
from app.services.feedback_service import FeedbackService

router = APIRouter()

Base.metadata.create_all(bind=app_engine)


def get_app_db():
    db = AppSessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/")
def root():
    return {"message": "Prediction Service is running"}

@router.post("/predict", response_model=PredictionResponse)
def predict(
    request: PredictionRequest,
    db: Session = Depends(get_app_db)
):
    service = PredictionService(
        prediction_repository=PredictionRepository(),
        predictor=Predictor()
    )

    try:
        saved_prediction = service.create_prediction(
            db,
            {
                "sepal_length": request.sepal_length,
                "sepal_width": request.sepal_width,
                "petal_length": request.petal_length,
                "petal_width": request.petal_width
            }
        )

        return PredictionResponse(
            prediction_id=saved_prediction.id,
            predicted_class=saved_prediction.predicted_class
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Prediction error: {str(e)}")
    
@router.post("/feedback", response_model=FeedbackResponse)
def create_feedback(
    request: FeedbackRequest,
    db: Session = Depends(get_app_db)
):
    service = FeedbackService(feedback_repository=FeedbackRepository())

    try:
        saved_feedback = service.create_feedback(
            db,
            {
                "prediction_id": request.prediction_id,
                "is_correct": request.is_correct,
                "true_label": request.true_label
            }
        )

        return FeedbackResponse(
            message="Feedback saved successfully",
            feedback_id=saved_feedback.id
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Feedback error: {str(e)}")

@router.get("/predictions")
def get_predictions(db: Session = Depends(get_app_db)):
    repository = PredictionRepository()
    return repository.get_all_predictions(db)


@router.get("/feedbacks")
def get_feedbacks(db: Session = Depends(get_app_db)):
    repository = FeedbackRepository()
    return repository.get_all_feedbacks(db)