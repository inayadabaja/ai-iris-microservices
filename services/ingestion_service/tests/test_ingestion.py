from fastapi.testclient import TestClient
from unittest.mock import patch
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.main import app
from app.models.raw_data_model import Base
from app.api.routes import get_db

TEST_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    TEST_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)


def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db

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