from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Boolean
from datetime import datetime

from app.models.prediction_model import Base


class Feedback(Base):
    __tablename__ = "feedback"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    prediction_id = Column(Integer, ForeignKey("predictions.id"), nullable=False)
    is_correct = Column(Boolean, nullable=False)
    true_label = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)