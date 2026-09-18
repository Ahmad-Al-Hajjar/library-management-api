import pytest
from database import TestingSession
from db_models import User, Book, Token
from sqlalchemy import select
from security.password import hash_password
from main import app
from fastapi.testclient import TestClient
client = TestClient(app)

@pytest.fixture
def normal_user_token():
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

    response = client.post("/auth/login",
                           json={
                               "user_name" : "normal_user",
                               "password" : "12345678"
                           })
    assert response.status_code == 200
    db.close()

    db = TestingSession()
    token = db.get(Token, response.json()["access_token"])

    user_id = user.id
    db.close()
    yield token

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
def admin_user_token():
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

    response = client.post("/auth/login",
                           json={
                               "user_name" : "admin_user",
                               "password" : "12345678"
                           })
    assert response.status_code == 200
    db.close()

    db = TestingSession()
    token = db.get(Token, response.json()["access_token"])

    user_id = user.id
    db.close()
    yield token

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
def add_book():
    db = TestingSession()
    book = Book(
        name = "Test Book",
        author = "Test Author",
        copies = 5,
        cost = 10
    )
    db.add(book)
    db.commit()
    db.refresh(book)

    book_id = book.id
    db.close()

    yield book

    db = TestingSession()
    book = db.get(Book, book_id)
    if book is not None:
        db.delete(book) 
    db.commit()
    db.close()
