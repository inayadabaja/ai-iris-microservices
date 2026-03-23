from pydantic import BaseModel
from typing import Any


class TrainResponse(BaseModel):
    message: str
    metrics: dict[str, Any]
    mlflow: dict[str, Any]
    params: dict[str, Any]


class MetricsResponse(BaseModel):
    accuracy: float
    classification_report: dict[str, Any]
    confusion_matrix: list[list[int]]


class ModelInfoResponse(BaseModel):
    message: str
    model_name: str
    run_id: str
    experiment_id: str
    params: dict[str, Any]