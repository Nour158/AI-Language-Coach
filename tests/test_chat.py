from fastapi.testclient import TestClient

from backend.main import app

client = TestClient(app)


def test_health():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_chat_returns_structured_json():
    response = client.post(
        "/chat",
        json={
            "message": "I like traveling.",
            "history": [],
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert "response" in data
    assert "history" in data
    assert data["source"] == "mock"
    assert len(data["history"]) == 2


def test_empty_chat_message_is_rejected():
    response = client.post(
        "/chat",
        json={
            "message": "",
            "history": [],
        },
    )

    assert response.status_code == 422
