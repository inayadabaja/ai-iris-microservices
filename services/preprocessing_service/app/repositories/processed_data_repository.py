from sqlalchemy.orm import Session
from app.models.processed_data_model import ProcessedIrisData


class ProcessedDataRepository:
    def delete_all(self, db: Session) -> None:
        db.query(ProcessedIrisData).delete()
        db.commit()

    def save_all(self, db: Session, records: list[dict]) -> int:
        objects = [ProcessedIrisData(**record) for record in records]
        db.add_all(objects)
        db.commit()
        return len(objects)