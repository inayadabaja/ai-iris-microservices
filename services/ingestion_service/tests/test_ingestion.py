from fastapi.testclient import TestClient
from unittest.mock import patch

from app.main import app

client = TestClient(app)


def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Ingestion Service is running"}


@patch("app.api.routes.IngestionService.ingest")
def test_ingest_success(mock_ingest):
    mock_ingest.return_value = 147

    response = client.post("/ingest")
    data = response.json()

    assert response.status_code == 200
    assert data["message"] == "Data ingested successfully"
    assert data["rows_inserted"] == 147


@patch("app.api.routes.IngestionService.ingest")
def test_ingest_file_not_found(mock_ingest):
    mock_ingest.side_effect = FileNotFoundError()

    response = client.post("/ingest")
    data = response.json()

    assert response.status_code == 404
    assert data["detail"] == "CSV file not found"


@patch("app.api.routes.IngestionService.ingest")
def test_ingest_missing_column(mock_ingest):
    mock_ingest.side_effect = KeyError("species")

    response = client.post("/ingest")
    data = response.json()

    assert response.status_code == 400
    assert "Missing column" in data["detail"]


@patch("app.api.routes.IngestionService.ingest")
def test_ingest_internal_error(mock_ingest):
    mock_ingest.side_effect = Exception("unexpected error")

    response = client.post("/ingest")
    data = response.json()

    assert response.status_code == 500
    assert "Ingestion error" in data["detail"]