from fastapi.testclient import TestClient
from backend.main import app

client = TestClient(app)


def test_job_creation_missing_file():
    response = client.post("/api/jobs", files={})
    assert response.status_code == 422
