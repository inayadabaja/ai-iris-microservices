from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from mlflow.exceptions import MlflowException

from app.core.database import ProcessedSessionLocal
from app.schemas.training_schema import TrainResponse, MetricsResponse, ModelInfoResponse
from app.repositories.training_data_repository import TrainingDataRepository
from app.repositories.model_metadata_repository import ModelMetadataRepository
from app.services.trainer import Trainer
from app.services.evaluator import Evaluator
from app.services.mlflow_service import MLflowService
from app.services.training_service import TrainingService

router = APIRouter()

metadata_repository = ModelMetadataRepository()


def get_processed_db():
    db = ProcessedSessionLocal()
    try:
        yield db
    finally:
        db.close()


def build_training_service() -> TrainingService:
    return TrainingService(
        training_data_repository=TrainingDataRepository(),
        model_metadata_repository=metadata_repository,
        trainer=Trainer(),
        evaluator=Evaluator(),
        mlflow_service=MLflowService()
    )


@router.get("/")
def root():
    return {"message": "Training Service is running"}


@router.post("/train", response_model=TrainResponse)
def train_model(db: Session = Depends(get_processed_db)):
    service = build_training_service()

    try:
        return service.train(db)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except MlflowException as e:
        raise HTTPException(status_code=503, detail=f"MLflow unavailable: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Training error: {str(e)}")


@router.get("/metrics/latest", response_model=MetricsResponse)
def get_latest_metrics():
    service = build_training_service()
    metrics = service.get_latest_metrics()

    if metrics is None:
        raise HTTPException(status_code=404, detail="No training metrics found")

    return metrics


@router.get("/model/info", response_model=ModelInfoResponse)
def get_model_info():
    service = build_training_service()
    info = service.get_model_info()

    if info is None:
        raise HTTPException(status_code=404, detail="No model info found")

    return info