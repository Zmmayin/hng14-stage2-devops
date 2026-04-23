import pytest
from unittest.mock import MagicMock, patch
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

@pytest.fixture(autouse=True)
def mock_redis():
    with patch("main.r") as mock_r:
        yield mock_r


def test_health_endpoint():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_create_job(mock_redis):
    mock_redis.hset.return_value = True
    mock_redis.lpush.return_value = True

    response = client.post("/jobs")

    assert response.status_code == 200
    data = response.json()
    assert "job_id" in data
    assert len(data["job_id"]) > 0
    mock_redis.hset.assert_called_once()
    mock_redis.lpush.assert_called_once()


def test_get_job_status(mock_redis):
    mock_redis.hget.return_value = b"queued"

    response = client.get("/jobs/test-job-123")

    assert response.status_code == 200
    data = response.json()
    assert data["job_id"] == "test-job-123"
    assert data["status"] == "queued"


def test_get_job_not_found(mock_redis):
    mock_redis.hget.return_value = None

    response = client.get("/jobs/fake-job-id")

    assert response.status_code == 404
