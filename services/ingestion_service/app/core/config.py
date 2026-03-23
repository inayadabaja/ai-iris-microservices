import os
from dotenv import load_dotenv

load_dotenv()


class Settings:
    APP_NAME: str = "Ingestion Service"
    APP_HOST: str = os.getenv("INGESTION_SERVICE_HOST", "0.0.0.0")
    APP_PORT: int = int(os.getenv("INGESTION_SERVICE_PORT", 8001))

    POSTGRES_USER: str = os.getenv("POSTGRES_USER", "postgres")
    POSTGRES_PASSWORD: str = os.getenv("POSTGRES_PASSWORD", "postgres")
    POSTGRES_DB: str = os.getenv("POSTGRES_DB", "raw_db")
    POSTGRES_HOST: str = os.getenv("POSTGRES_HOST", "localhost")
    POSTGRES_PORT: str = os.getenv("POSTGRES_PORT", "5432")

    CSV_FILE_PATH: str = os.getenv("CSV_FILE_PATH", "/app/data/raw/iris.csv")

    @property
    def database_url(self) -> str:
        return (
            f"postgresql+psycopg2://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}"
            f"@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"
        )


settings = Settings()