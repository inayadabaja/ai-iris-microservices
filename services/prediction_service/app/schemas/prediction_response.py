from pydantic import BaseModel


class PredictionResponse(BaseModel):
    prediction_id: int
    predicted_class: str