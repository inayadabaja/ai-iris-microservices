from sqlalchemy.orm import Session
from app.models.raw_data_model import RawIrisData


class RawDataRepository:
    def delete_all(self, db: Session) -> None:
        db.query(RawIrisData).delete()
        db.commit()

    def save_all(self, db: Session, records: list[dict]) -> int:
        objects = [RawIrisData(**record) for record in records]
        db.add_all(objects)
        db.commit()
        return len(objects)