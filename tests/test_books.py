from fastapi.testclient import TestClient
from main import app
from database import TestingSession
import pytest
from security.password import hash_password
from db_models import User, Token, Book
from sqlalchemy import select
from tests.dependencies import normal_user_token, admin_user_token, add_book
client = TestClient(app)

def test_get_book(add_book):
    response = client.get(f"/books/{add_book.id}")
    
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

def test_add_book_by_normal_user(normal_user_token):
    response = client.post("/books",
                           headers= {"Authorization": f"Bearer {normal_user_token.access_token}"},
                            json = {
                                "name": "Test Book",
                                "author": "Test Author",
                                "copies": 5,
                                "cost": 10
                           })
    assert response.status_code == 403

def test_add_book_by_admin_user(admin_user_token):
    response = client.post("/books",
                           headers= {"Authorization": f"Bearer {admin_user_token.access_token}"},
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

def test_update_book_by_admin_user(admin_user_token, add_book):
    response = client.put(
        f"/books/{add_book.id}",
        headers={"Authorization": f"Bearer {admin_user_token.access_token}"},
        json={
            "name": "New Book",
            "author": "New Author",
            "copies": 10,
            "cost": 20
        })
    assert response.status_code == 200

    data = response.json()
    assert data["id"] == add_book.id
    assert data["name"] == "New Book"
    assert data["author"] == "New Author"
    assert data["copies"] == 10
    assert data["cost"] == "20.00"

    db = TestingSession()
    book = db.get(Book, add_book.id)
    
    if book is not None:
        db.delete(book)
    db.commit()
    db.close()


def test_delete_by_admin_user(admin_user_token, add_book):
    response = client.delete(f"/books/{add_book.id}",
                           headers={"Authorization": f"Bearer {admin_user_token.access_token}"})
    assert response.status_code == 200


def test_delete_by_normal_user(normal_user_token, add_book):
    response = client.delete(f"/books/{add_book.id}",
                           headers={"Authorization": f"Bearer {normal_user_token.access_token}"})
    assert response.status_code == 403