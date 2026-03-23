from pydantic import BaseModel


class FeedbackRequest(BaseModel):
    prediction_id: int
    is_correct: bool
    true_label: str | None = None


class FeedbackResponse(BaseModel):
    message: str
    feedback_id: int