from fastapi.testclient import TestClient
from unittest.mock import patch

from app.main import app

client = TestClient(app)


def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Preprocessing Service is running"}


@patch("app.api.routes.PreprocessingService.preprocess")
def test_preprocess_success(mock_preprocess):
    mock_preprocess.return_value = 147

    response = client.post("/preprocess")
    data = response.json()

    assert response.status_code == 200
    assert data["message"] == "Data preprocessed successfully"
    assert data["rows_inserted"] == 147


@patch("app.api.routes.PreprocessingService.preprocess")
def test_preprocess_no_raw_data(mock_preprocess):
    mock_preprocess.side_effect = ValueError("No raw data found for preprocessing")

    response = client.post("/preprocess")
    data = response.json()

    assert response.status_code == 400
    assert data["detail"] == "No raw data found for preprocessing"


@patch("app.api.routes.PreprocessingService.preprocess")
def test_preprocess_internal_error(mock_preprocess):
    mock_preprocess.side_effect = Exception("unexpected preprocessing error")

    response = client.post("/preprocess")
    data = response.json()

    assert response.status_code == 500
    assert "Preprocessing error" in data["detail"]