from tests.dependencies import normal_user_token, add_book
from fastapi.testclient import TestClient
from main import app
from db_models import Book
from database import TestingSession
client = TestClient(app)

def test_borrow_book(normal_user_token, add_book):
    copies = add_book.copies
    response = client.post("/borrow",
                      headers= {"Authorization": f"Bearer {normal_user_token.access_token}"},
                            json = {
                                "book_id" : add_book.id
                                })
    db = TestingSession()
    book = db.get(Book, add_book.id)
    db.close()

    assert response.status_code == 201
    assert book.copies == copies -1

def test_return_book(normal_user_token, add_book):
    response = client.post("/borrow",
                      headers= {"Authorization": f"Bearer {normal_user_token.access_token}"},
                            json = {
                                "book_id" : add_book.id
                                })
    assert response.status_code == 201

    response = client.post("/return",
                      headers= {"Authorization": f"Bearer {normal_user_token.access_token}"},
                            json = {
                                "book_id" : add_book.id
                                })
    assert response.status_code == 201

def test_borrow_book_not_found(normal_user_token):
    response = client.post("/borrow",
                      headers= {"Authorization": f"Bearer {normal_user_token.access_token}"},
                            json = {
                                "book_id" : 99999
                                })
    assert response.status_code == 404

def test_borrow_with_no_copies(normal_user_token, add_book):
    db = TestingSession()
    book = db.get(Book, add_book.id)
    book.copies = 0
    db.commit()
    db.refresh(book)
    db.close()


    response = client.post("/borrow",
                      headers= {"Authorization": f"Bearer {normal_user_token.access_token}"},
                            json = {
                                "book_id" : book.id
                                })

    assert response.status_code == 409

def test_borrow_same_book_twice(normal_user_token, add_book):
    response = client.post("/borrow",
                      headers= {"Authorization": f"Bearer {normal_user_token.access_token}"},
                            json = {
                                "book_id" : add_book.id
                                })
    assert response.status_code == 201

    response = client.post("/borrow",
                      headers= {"Authorization": f"Bearer {normal_user_token.access_token}"},
                            json = {
                                "book_id" : add_book.id
                                })
    assert response.status_code == 409

def test_return_without_borrowing(normal_user_token, add_book):
    response = client.post("/return",
                      headers= {"Authorization": f"Bearer {normal_user_token.access_token}"},
                            json = {
                                "book_id" : add_book.id
                                })
    assert response.status_code == 404