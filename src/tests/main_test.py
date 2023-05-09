from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_get_models():
    response = client.get("/models")
    assert response.status_code == 200
