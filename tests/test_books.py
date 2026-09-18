from fastapi.testclient import TestClient
from main import app
from database import TestingSession
import pytest
from security.password import hash_password
from db_models import User, Token, Book
from sqlalchemy import select
client = TestClient(app)

@pytest.fixture
def normal_user():
    db = TestingSession()
    user = User(
        name="Normal User",
        user_name="normal_user",
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

    tokens = db.execute(select(Token).where(Token.user_id == user_id)).scalars().all()
    for token in tokens:
        db.delete(token)

    user = db.get(User, user_id)
    if user is not None:
        db.delete(user)
        
    db.commit()
    db.close()

@pytest.fixture
def admin_user():
    db = TestingSession()
    user = User(
        name="Admin User",
        user_name="admin_user",
        password=hash_password("12345678"),
        amount=0,
        is_admin=True
    )
    db.add(user)
    db.commit()
    db.refresh(user)

    user_id = user.id
    db.close()
    yield user

    db = TestingSession()

    tokens = db.execute(select(Token).where(Token.user_id == user_id)).scalars().all()
    for token in tokens:
        db.delete(token)

    user = db.get(User, user_id)
    if user is not None:
        db.delete(user)
        
    db.commit()
    db.close()

def test_get_book():
    response = client.get("/books/1")
    
    assert response.status_code == 200

def test_not_found_book():
    response = client.get("/books/999")
    assert response.status_code == 404

def test_add_book_without_token():
    response = client.post("/books",
                          json = {
                                "name": "Test Book",
                                "author": "Test Author",
                                "copies": 5,
                                "cost": 10
                           })
    assert response.status_code == 401

def test_add_book_by_normal_user(normal_user):
    response = client.post("/auth/login",
                           json={
                               "user_name" : "normal_user",
                               "password" : "12345678"
                           })
    assert response.status_code == 200
    
    data = response.json()
    token = data["access_token"]

    response = client.post("/books",
                           headers= {"Authorization": f"Bearer {token}"},
                            json = {
                                "name": "Test Book",
                                "author": "Test Author",
                                "copies": 5,
                                "cost": 10
                           })
    assert response.status_code == 403


def test_add_book_by_admin_user(admin_user):
    response = client.post("/auth/login",
                           json={
                               "user_name" : "admin_user",
                               "password" : "12345678"
                           })
    assert response.status_code == 200
    
    data = response.json()
    token = data["access_token"]

    response = client.post("/books",
                           headers= {"Authorization": f"Bearer {token}"},
                            json = {
                                "name": "Test Book",
                                "author": "Test Author",
                                "copies": 5,
                                "cost": 10
                           })
    assert response.status_code == 201

    db = TestingSession()
    book_id = response.json()["id"]
    book = db.get(Book, book_id)

    if book is not None:
        db.delete(book)
    db.commit()
    db.close()


def test_update_book_by_admin_user(admin_user):
    response = client.post(
        "/auth/login",
        json={
            "user_name": "admin_user",
            "password": "12345678"
        }
    )

    assert response.status_code == 200

    token = response.json()["access_token"]

    response = client.post(
        "/books",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "name": "Old Book",
            "author": "Old Author",
            "copies": 5,
            "cost": 10
        }
    )

    assert response.status_code == 201

    book_id = response.json()["id"]

    response = client.put(
        f"/books/{book_id}",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "name": "New Book",
            "author": "New Author",
            "copies": 10,
            "cost": 20
        })
    assert response.status_code == 200

    data = response.json()
    assert data["id"] == book_id
    assert data["name"] == "New Book"
    assert data["author"] == "New Author"
    assert data["copies"] == 10
    assert data["cost"] == "20.00"

    db = TestingSession()
    book = db.get(Book, book_id)
    
    if book is not None:
        db.delete(book)
    db.commit()
    db.close()