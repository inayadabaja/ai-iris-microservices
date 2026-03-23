import pandas as pd

from app.repositories.training_data_repository import TrainingDataRepository
from app.repositories.model_metadata_repository import ModelMetadataRepository
from app.services.trainer import Trainer
from app.services.evaluator import Evaluator
from app.services.mlflow_service import MLflowService


class TrainingService:
    def __init__(
        self,
        training_data_repository: TrainingDataRepository,
        model_metadata_repository: ModelMetadataRepository,
        trainer: Trainer,
        evaluator: Evaluator,
        mlflow_service: MLflowService
    ):
        self.training_data_repository = training_data_repository
        self.model_metadata_repository = model_metadata_repository
        self.trainer = trainer
        self.evaluator = evaluator
        self.mlflow_service = mlflow_service

    def train(self, db) -> dict:
        df = self.training_data_repository.fetch_processed_data(db)

        if df.empty:
            raise ValueError("No processed data found for training")

        train_df = df[df["dataset_type"] == "train"].copy()
        test_df = df[df["dataset_type"] == "test"].copy()

        if train_df.empty or test_df.empty:
            raise ValueError("Train or test dataset is missing")

        feature_columns = ["sepal_length", "sepal_width", "petal_length", "petal_width"]

        X_train = train_df[feature_columns]
        y_train = train_df["target"]

        X_test = test_df[feature_columns]
        y_test = test_df["target"]

        model = self.trainer.train(X_train, y_train)
        metrics = self.evaluator.evaluate(model, X_test, y_test)

        params = {
            "model_type": "LogisticRegression",
            "random_state": 42,
            "max_iter": 200,
            "train_rows": len(train_df),
            "test_rows": len(test_df),
            "n_features": len(feature_columns)
        }

        mlflow_info = self.mlflow_service.log_training_run(
            model=model,
            metrics=metrics,
            params=params
        )

        result = {
            "message": "Model trained successfully",
            "metrics": metrics,
            "mlflow": mlflow_info,
            "params": params
        }

        self.model_metadata_repository.save_latest_result(result)
        return result

    def get_latest_metrics(self) -> dict | None:
        result = self.model_metadata_repository.get_latest_result()
        if not result:
            return None

        return {
            "accuracy": result["metrics"]["accuracy"],
            "classification_report": result["metrics"]["classification_report"],
            "confusion_matrix": result["metrics"]["confusion_matrix"]
        }

    def get_model_info(self) -> dict | None:
        result = self.model_metadata_repository.get_latest_result()
        if not result:
            return None

        return {
            "message": result["message"],
            "model_name": result["mlflow"]["model_name"],
            "run_id": result["mlflow"]["run_id"],
            "experiment_id": result["mlflow"]["experiment_id"],
            "params": result["params"]
        }