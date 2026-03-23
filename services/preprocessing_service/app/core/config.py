import os
from dotenv import load_dotenv

load_dotenv()


class Settings:
    APP_NAME: str = "Preprocessing Service"
    APP_HOST: str = os.getenv("PREPROCESSING_SERVICE_HOST", "0.0.0.0")
    APP_PORT: int = int(os.getenv("PREPROCESSING_SERVICE_PORT", 8002))

    RAW_POSTGRES_USER: str = os.getenv("RAW_POSTGRES_USER", "postgres")
    RAW_POSTGRES_PASSWORD: str = os.getenv("RAW_POSTGRES_PASSWORD", "postgres")
    RAW_POSTGRES_DB: str = os.getenv("RAW_POSTGRES_DB", "raw_db")
    RAW_POSTGRES_HOST: str = os.getenv("RAW_POSTGRES_HOST", "localhost")
    RAW_POSTGRES_PORT: str = os.getenv("RAW_POSTGRES_PORT", "5432")

    PROCESSED_POSTGRES_USER: str = os.getenv("PROCESSED_POSTGRES_USER", "postgres")
    PROCESSED_POSTGRES_PASSWORD: str = os.getenv("PROCESSED_POSTGRES_PASSWORD", "postgres")
    PROCESSED_POSTGRES_DB: str = os.getenv("PROCESSED_POSTGRES_DB", "processed_db")
    PROCESSED_POSTGRES_HOST: str = os.getenv("PROCESSED_POSTGRES_HOST", "localhost")
    PROCESSED_POSTGRES_PORT: str = os.getenv("PROCESSED_POSTGRES_PORT", "5432")

    @property
    def raw_database_url(self) -> str:
        return (
            f"postgresql+psycopg2://{self.RAW_POSTGRES_USER}:{self.RAW_POSTGRES_PASSWORD}"
            f"@{self.RAW_POSTGRES_HOST}:{self.RAW_POSTGRES_PORT}/{self.RAW_POSTGRES_DB}"
        )

    @property
    def processed_database_url(self) -> str:
        return (
            f"postgresql+psycopg2://{self.PROCESSED_POSTGRES_USER}:{self.PROCESSED_POSTGRES_PASSWORD}"
            f"@{self.PROCESSED_POSTGRES_HOST}:{self.PROCESSED_POSTGRES_PORT}/{self.PROCESSED_POSTGRES_DB}"
        )


settings = Settings()