import pytest
from fastapi.testclient import TestClient
from main import app
from db_models import User, Token
from security.password import hash_password
from database import TestingSession
from sqlalchemy import select
client = TestClient(app)


@pytest.fixture
def test_add_user():
    db = TestingSession()
    user= User(
        name="Test User",
        user_name="t_user",
        password=hash_password("12345678"),
        amount=0,
        is_admin=False
    )
    db.add(user)
    db.commit()
    db.refresh(user)

    user_id = user.id
    db.close()

    yield user

    db = TestingSession()
    tokens = db.execute(
        select(Token).where(Token.user_id == user.id)
    ).scalars().all()

    for token in tokens:
        db.delete(token)

        user = db.get(User, user_id)

    if user is not None:
        db.delete(user)

    db.commit()
    db.close()


def test_login(test_add_user):
    response = client.post(
        "/auth/login",
        json={
            "user_name": "t_user",
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


def test_login_wrong_password(test_add_user):
    response = client.post("/auth/login",
                           json={
                               "user_name" : "t_user",
                               "password" : "wrongpassword"
                           })
    assert response.status_code == 401


