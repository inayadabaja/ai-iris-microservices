import os
from dotenv import load_dotenv

load_dotenv()


class Settings:
    APP_NAME: str = "Prediction Service"
    APP_HOST: str = os.getenv("PREDICTION_SERVICE_HOST", "0.0.0.0")
    APP_PORT: int = int(os.getenv("PREDICTION_SERVICE_PORT", 8004))

    APP_POSTGRES_USER: str = os.getenv("APP_POSTGRES_USER", "postgres")
    APP_POSTGRES_PASSWORD: str = os.getenv("APP_POSTGRES_PASSWORD", "postgres")
    APP_POSTGRES_DB: str = os.getenv("APP_POSTGRES_DB", "app_db")
    APP_POSTGRES_HOST: str = os.getenv("APP_POSTGRES_HOST", "localhost")
    APP_POSTGRES_PORT: str = os.getenv("APP_POSTGRES_PORT", "5432")

    MLFLOW_TRACKING_URI: str = os.getenv("MLFLOW_TRACKING_URI", "http://localhost:5000")
    MLFLOW_MODEL_NAME: str = os.getenv("MLFLOW_MODEL_NAME", "iris_logistic_regression")
    TRAINING_API_URL: str = os.getenv("TRAINING_API_URL", "http://localhost:8003")

    @property
    def app_database_url(self) -> str:
        return (
            f"postgresql+psycopg2://{self.APP_POSTGRES_USER}:{self.APP_POSTGRES_PASSWORD}"
            f"@{self.APP_POSTGRES_HOST}:{self.APP_POSTGRES_PORT}/{self.APP_POSTGRES_DB}"
        )


settings = Settings()