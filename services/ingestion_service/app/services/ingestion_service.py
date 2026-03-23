from app.services.csv_reader import CSVReader
from app.services.data_cleaner import DataCleaner
from app.repositories.raw_data_repository import RawDataRepository


class IngestionService:
    def __init__(
        self,
        csv_reader: CSVReader,
        data_cleaner: DataCleaner,
        repository: RawDataRepository
    ):
        self.csv_reader = csv_reader
        self.data_cleaner = data_cleaner
        self.repository = repository

    def ingest(self, db, file_path: str) -> int:
        df = self.csv_reader.read_csv(file_path)
        df = self.data_cleaner.clean(df)
        records = df.to_dict(orient="records")

        self.repository.delete_all(db)
        inserted_count = self.repository.save_all(db, records)

        return inserted_count