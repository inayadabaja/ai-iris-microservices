from sqlalchemy.orm import Session

from app.models.feedback_model import Feedback


class FeedbackRepository:
    def save_feedback(self, db: Session, data: dict) -> Feedback:
        feedback = Feedback(**data)
        db.add(feedback)
        db.commit()
        db.refresh(feedback)
        return feedback

    def get_all_feedbacks(self, db: Session) -> list[Feedback]:
        return db.query(Feedback).order_by(Feedback.id.desc()).all()