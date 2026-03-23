import mlflow
import mlflow.sklearn

from app.core.config import settings


class MLflowService:
    def __init__(self):
        self.tracking_uri = settings.MLFLOW_TRACKING_URI
        self.experiment_name = settings.MLFLOW_EXPERIMENT_NAME
        self.model_name = settings.MLFLOW_MODEL_NAME

    def _setup(self):
        mlflow.set_tracking_uri(self.tracking_uri)
        mlflow.set_experiment(self.experiment_name)

    def log_training_run(self, model, metrics: dict, params: dict) -> dict:
        self._setup()

        with mlflow.start_run() as run:
            mlflow.log_params(params)
            mlflow.log_metric("accuracy", metrics["accuracy"])
            mlflow.log_dict(metrics["classification_report"], "classification_report.json")
            mlflow.log_dict({"confusion_matrix": metrics["confusion_matrix"]}, "confusion_matrix.json")

            mlflow.sklearn.log_model(
                sk_model=model,
                artifact_path="model",
                registered_model_name=self.model_name
            )

            return {
                "run_id": run.info.run_id,
                "experiment_id": run.info.experiment_id,
                "model_name": self.model_name
            }