from fastapi.testclient import TestClient
from main import app

client = TestClient(app)
URL = "/session"


def test_websocket_endpoint():
    with client.websocket_connect(URL) as websocket:
        websocket.send_json({"model": "bigram", "message": "Hello, how are you?"})
        response = websocket.receive_json()
        assert response["message"] is not None
