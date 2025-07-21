from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_register_and_login():
    payload = {
        "username": "testuser",
        "email": "test@example.com",
        "password": "password123",
        "role": "student",
    }
    response = client.post("/users/register", json=payload)
    assert response.status_code == 201
    assert response.json()["username"] == "testuser"

    login_payload = {"username": "testuser", "password": "password123"}
    login_resp = client.post("/users/login", json=login_payload)
    assert login_resp.status_code == 200
    assert "access_token" in login_resp.json()

    token = login_resp.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    me = client.get("/users/me", headers=headers)
    assert me.status_code == 200
    assert me.json()["email"] == "test@example.com"
