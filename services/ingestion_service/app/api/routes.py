from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.database import engine, SessionLocal
from app.models.raw_data_model import Base
from app.schemas.raw_data_schema import RawDataResponse
from app.services.csv_reader import CSVReader
from app.services.data_cleaner import DataCleaner
from app.repositories.raw_data_repository import RawDataRepository
from app.services.ingestion_service import IngestionService

router = APIRouter()

Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/")
def root():
    return {"message": "Ingestion Service is running"}


@router.post("/ingest", response_model=RawDataResponse)
def ingest_data(db: Session = Depends(get_db)):
    service = IngestionService(
        csv_reader=CSVReader(),
        data_cleaner=DataCleaner(),
        repository=RawDataRepository()
    )

    try:
        inserted_count = service.ingest(db, settings.CSV_FILE_PATH)
        return RawDataResponse(
            message="Data ingested successfully",
            rows_inserted=inserted_count
        )
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="CSV file not found")
    except KeyError as e:
        raise HTTPException(status_code=400, detail=f"Missing column: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ingestion error: {str(e)}")