from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.main import app
from app.models.prediction_model import Base
from app.api.routes import get_app_db

TEST_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    TEST_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)


def override_get_app_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_app_db] = override_get_app_db

client = TestClient(app)


def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Prediction Service is running"}


@patch("app.api.routes.PredictionService.create_prediction")
def test_predict_success(mock_create_prediction):
    mock_obj = MagicMock()
    mock_obj.id = 1
    mock_obj.predicted_class = "setosa"
    mock_create_prediction.return_value = mock_obj

    response = client.post(
        "/predict",
        json={
            "sepal_length": 5.1,
            "sepal_width": 3.5,
            "petal_length": 1.4,
            "petal_width": 0.2
        }
    )

    data = response.json()

    assert response.status_code == 200
    assert data["prediction_id"] == 1
    assert data["predicted_class"] == "setosa"


def test_predict_validation_error():
    response = client.post(
        "/predict",
        json={
            "sepal_length": 5.1,
            "sepal_width": 3.5,
            "petal_length": 1.4
        }
    )

    assert response.status_code == 422


@patch("app.api.routes.PredictionService.create_prediction")
def test_predict_internal_error(mock_create_prediction):
    mock_create_prediction.side_effect = Exception("prediction failed")

    response = client.post(
        "/predict",
        json={
            "sepal_length": 5.1,
            "sepal_width": 3.5,
            "petal_length": 1.4,
            "petal_width": 0.2
        }
    )

    data = response.json()

    assert response.status_code == 500
    assert "Prediction error" in data["detail"]


@patch("app.api.routes.FeedbackService.create_feedback")
def test_feedback_success(mock_create_feedback):
    mock_obj = MagicMock()
    mock_obj.id = 1
    mock_create_feedback.return_value = mock_obj

    response = client.post(
        "/feedback",
        json={
            "prediction_id": 1,
            "is_correct": True,
            "true_label": "setosa"
        }
    )

    data = response.json()

    assert response.status_code == 200
    assert data["message"] == "Feedback saved successfully"
    assert data["feedback_id"] == 1


def test_feedback_validation_error():
    response = client.post(
        "/feedback",
        json={
            "prediction_id": 1
        }
    )

    assert response.status_code == 422


@patch("app.api.routes.FeedbackService.create_feedback")
def test_feedback_internal_error(mock_create_feedback):
    mock_create_feedback.side_effect = Exception("feedback failed")

    response = client.post(
        "/feedback",
        json={
            "prediction_id": 1,
            "is_correct": False,
            "true_label": "virginica"
        }
    )

    data = response.json()

    assert response.status_code == 500
    assert "Feedback error" in data["detail"]