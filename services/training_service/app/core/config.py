import os
from dotenv import load_dotenv

load_dotenv()


class Settings:
    APP_NAME: str = "Training Service"
    APP_HOST: str = os.getenv("TRAINING_SERVICE_HOST", "0.0.0.0")
    APP_PORT: int = int(os.getenv("TRAINING_SERVICE_PORT", 8003))

    PROCESSED_POSTGRES_USER: str = os.getenv("PROCESSED_POSTGRES_USER", "postgres")
    PROCESSED_POSTGRES_PASSWORD: str = os.getenv("PROCESSED_POSTGRES_PASSWORD", "postgres")
    PROCESSED_POSTGRES_DB: str = os.getenv("PROCESSED_POSTGRES_DB", "processed_db")
    PROCESSED_POSTGRES_HOST: str = os.getenv("PROCESSED_POSTGRES_HOST", "localhost")
    PROCESSED_POSTGRES_PORT: str = os.getenv("PROCESSED_POSTGRES_PORT", "5432")

    MLFLOW_TRACKING_URI: str = os.getenv("MLFLOW_TRACKING_URI", "http://localhost:5000")
    MLFLOW_EXPERIMENT_NAME: str = os.getenv("MLFLOW_EXPERIMENT_NAME", "iris_training_experiment")
    MLFLOW_MODEL_NAME: str = os.getenv("MLFLOW_MODEL_NAME", "iris_logistic_regression")

    @property
    def processed_database_url(self) -> str:
        return (
            f"postgresql+psycopg2://{self.PROCESSED_POSTGRES_USER}:{self.PROCESSED_POSTGRES_PASSWORD}"
            f"@{self.PROCESSED_POSTGRES_HOST}:{self.PROCESSED_POSTGRES_PORT}/{self.PROCESSED_POSTGRES_DB}"
        )


settings = Settings()