import requests
from flask import current_app


class PredictionFrontendService:
    def predict(self, payload: dict) -> dict:
        api_url = f"{current_app.config['PREDICTION_API_URL']}/predict"
        response = requests.post(api_url, json=payload, timeout=30)
        response.raise_for_status()
        return response.json()

    def send_feedback(self, payload: dict) -> dict:
        api_url = f"{current_app.config['PREDICTION_API_URL']}/feedback"
        response = requests.post(api_url, json=payload, timeout=30)
        response.raise_for_status()
        return response.json()