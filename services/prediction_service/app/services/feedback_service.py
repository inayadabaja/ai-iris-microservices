from app.repositories.feedback_repository import FeedbackRepository


class FeedbackService:
    def __init__(self, feedback_repository: FeedbackRepository):
        self.feedback_repository = feedback_repository

    def create_feedback(self, db, feedback_data: dict):
        return self.feedback_repository.save_feedback(db, feedback_data)