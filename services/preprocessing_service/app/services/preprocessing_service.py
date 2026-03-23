from app.repositories.raw_fetch_repository import RawFetchRepository
from app.repositories.processed_data_repository import ProcessedDataRepository
from app.services.preprocessor import Preprocessor


class PreprocessingService:
    def __init__(
        self,
        raw_fetch_repository: RawFetchRepository,
        processed_data_repository: ProcessedDataRepository,
        preprocessor: Preprocessor
    ):
        self.raw_fetch_repository = raw_fetch_repository
        self.processed_data_repository = processed_data_repository
        self.preprocessor = preprocessor

    def preprocess(self, raw_db, processed_db) -> int:
        raw_df = self.raw_fetch_repository.fetch_all(raw_db)
        processed_df = self.preprocessor.process(raw_df)
        records = processed_df.to_dict(orient="records")

        self.processed_data_repository.delete_all(processed_db)
        inserted_count = self.processed_data_repository.save_all(processed_db, records)

        return inserted_count