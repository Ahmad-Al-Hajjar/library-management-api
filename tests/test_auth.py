from fastapi.testclient import TestClient
from main import app
from db_models import User
from security.password import hash_password
from database import TestingSession
#python -m pytest
client = TestClient(app)

def test_login():
    db = TestingSession()
    user= User(
        name="Test User",
        user_name="te111stuser",
        password=hash_password("12345678"),
        amount=0,
        is_admin=False
    )
    db.add(user)
    db.commit()
    db.close()

    response = client.post(
        "/auth/login",
        json={
            "user_name": "te111stuser",
            "password": "12345678"
        }
    )
    assert response.status_code == 200

    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"

    token = data["access_token"]

    response = client.get("/users/me",
                          headers={"Authorization": f"Bearer {token}"})    

    assert response.status_code == 200


def test_login_wrong_password():
    response = client.post("/auth/login",
                           json={
                               "user_name" : "te111stuser",
                               "password" : "wrongpassword"
                           })
    assert response.status_code == 401