from fastapi.testclient import TestClient
from unittest.mock import patch

from app.main import app

client = TestClient(app)


def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Training Service is running"}


@patch("app.api.routes.TrainingService.train")
def test_train_success(mock_train):
    mock_train.return_value = {
        "message": "Model trained successfully",
        "metrics": {
            "accuracy": 0.97,
            "classification_report": {
                "0": {"precision": 1.0, "recall": 1.0, "f1-score": 1.0, "support": 10}
            },
            "confusion_matrix": [[10, 0], [0, 20]]
        },
        "mlflow": {
            "run_id": "123abc",
            "experiment_id": "456",
            "model_name": "iris_logistic_regression"
        },
        "params": {
            "model_type": "LogisticRegression",
            "random_state": 42,
            "max_iter": 200,
            "train_rows": 117,
            "test_rows": 30,
            "n_features": 4
        }
    }

    response = client.post("/train")
    data = response.json()

    assert response.status_code == 200
    assert data["message"] == "Model trained successfully"
    assert "metrics" in data
    assert "mlflow" in data
    assert "params" in data


@patch("app.api.routes.TrainingService.train")
def test_train_no_processed_data(mock_train):
    mock_train.side_effect = ValueError("No processed data found for training")

    response = client.post("/train")
    data = response.json()

    assert response.status_code == 400
    assert data["detail"] == "No processed data found for training"


@patch("app.api.routes.TrainingService.train")
def test_train_internal_error(mock_train):
    mock_train.side_effect = Exception("training failed")

    response = client.post("/train")
    data = response.json()

    assert response.status_code == 500
    assert "Training error" in data["detail"]


@patch("app.api.routes.TrainingService.get_latest_metrics")
def test_get_latest_metrics(mock_metrics):
    mock_metrics.return_value = {
        "accuracy": 0.97,
        "classification_report": {"0": {"precision": 1.0}},
        "confusion_matrix": [[10, 0], [0, 20]]
    }

    response = client.get("/metrics/latest")
    data = response.json()

    assert response.status_code == 200
    assert "accuracy" in data
    assert "classification_report" in data
    assert "confusion_matrix" in data


@patch("app.api.routes.TrainingService.get_latest_metrics")
def test_get_latest_metrics_not_found(mock_metrics):
    mock_metrics.return_value = None

    response = client.get("/metrics/latest")
    data = response.json()

    assert response.status_code == 404
    assert data["detail"] == "No training metrics found"


@patch("app.api.routes.TrainingService.get_model_info")
def test_get_model_info(mock_info):
    mock_info.return_value = {
        "message": "Model trained successfully",
        "model_name": "iris_logistic_regression",
        "run_id": "123abc",
        "experiment_id": "456",
        "params": {"model_type": "LogisticRegression"}
    }

    response = client.get("/model/info")
    data = response.json()

    assert response.status_code == 200
    assert data["model_name"] == "iris_logistic_regression"


@patch("app.api.routes.TrainingService.get_model_info")
def test_get_model_info_not_found(mock_info):
    mock_info.return_value = None

    response = client.get("/model/info")
    data = response.json()

    assert response.status_code == 404
    assert data["detail"] == "No model info found"