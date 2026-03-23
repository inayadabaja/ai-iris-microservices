import time
import requests
import pandas as pd
import mlflow
import mlflow.pyfunc

from app.core.config import settings


class Predictor:
    def __init__(self):
        self.model = None
        mlflow.set_tracking_uri(settings.MLFLOW_TRACKING_URI)

    def _load_model_from_mlflow(self):
        model_uri = f"models:/{settings.MLFLOW_MODEL_NAME}/latest"
        return mlflow.pyfunc.load_model(model_uri=model_uri)

    def _trigger_training(self):
        url = f"{settings.TRAINING_API_URL}/train"
        response = requests.post(url, timeout=120)
        response.raise_for_status()
        return response.json()

    def load_model(self):
        if self.model is not None:
            return self.model

        try:
            self.model = self._load_model_from_mlflow()
            return self.model
        except Exception as first_error:
            # On tente un entraînement automatique une seule fois
            self._trigger_training()
            time.sleep(5)

            try:
                self.model = self._load_model_from_mlflow()
                return self.model
            except Exception as second_error:
                raise RuntimeError(
                    f"Impossible de charger le modèle après entraînement automatique. "
                    f"Première erreur: {first_error}. Deuxième erreur: {second_error}"
                )

    def predict(self, features: dict) -> str:
        model = self.load_model()

        input_df = pd.DataFrame([features])
        prediction = model.predict(input_df)
        predicted_value = prediction[0]

        label_mapping = {
            0: "setosa",
            1: "versicolor",
            2: "virginica",
            "0": "setosa",
            "1": "versicolor",
            "2": "virginica",
            "setosa": "setosa",
            "versicolor": "versicolor",
            "virginica": "virginica",
        }

        return label_mapping.get(predicted_value, str(predicted_value))