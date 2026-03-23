from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import RawSessionLocal, ProcessedSessionLocal
from app.schemas.processed_data_schema import ProcessedDataResponse
from app.repositories.raw_fetch_repository import RawFetchRepository
from app.repositories.processed_data_repository import ProcessedDataRepository
from app.services.preprocessor import Preprocessor
from app.services.preprocessing_service import PreprocessingService

router = APIRouter()


def get_raw_db():
    db = RawSessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_processed_db():
    db = ProcessedSessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/")
def root():
    return {"message": "Preprocessing Service is running"}


@router.post("/preprocess", response_model=ProcessedDataResponse)
def preprocess_data(
    raw_db: Session = Depends(get_raw_db),
    processed_db: Session = Depends(get_processed_db)
):
    service = PreprocessingService(
        raw_fetch_repository=RawFetchRepository(),
        processed_data_repository=ProcessedDataRepository(),
        preprocessor=Preprocessor()
    )

    try:
        inserted_count = service.preprocess(raw_db, processed_db)

        return ProcessedDataResponse(
            message="Data preprocessed successfully",
            rows_inserted=inserted_count
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Preprocessing error: {str(e)}")