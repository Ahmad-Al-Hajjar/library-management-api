from main import app
from database import TestingSession
from sqlalchemy import select
from db_models import User
from fastapi.testclient import TestClient
from tests.dependencies import normal_user_token, admin_user_token
client = TestClient(app)

def test_add_user_by_admin_user(admin_user_token):
    response = client.post("/users/add_user",
                           headers={"Authorization": f"Bearer {admin_user_token.access_token}"},
                           json={
                               "name" : "user",
                               "user_name" : "username",
                               "password" : "12345678",
                               "amount" : 100,
                               "is_admin" : True                                                                                            
                           })
    assert response.status_code == 201

    db = TestingSession()
    user = db.execute(select(User).where(User.user_name == "username")).scalar_one_or_none()
    if user is not None:
        db.delete(user)
    db.commit()
    db.close()

def test_add_user_by_normal_user(normal_user_token):
    response = client.post("/users/add_user",
                               headers={"Authorization": f"Bearer {normal_user_token.access_token}"},
                               json={
                                   "name" : "user",
                                   "user_name" : "username",
                                   "password" : "12345678",
                                   "amount" : 100,
                                   "is_admin" : True                                                                                            
                               })
    assert response.status_code == 403

    db = TestingSession()
    user = db.execute(select(User).where(User.user_name == "username")).scalar_one_or_none()
    if user is not None:
        db.delete(user)
    db.commit()
    db.close()

def test_duplicate_user_name(admin_user_token):
    response = client.post("/users/add_user",
                           headers={"Authorization": f"Bearer {admin_user_token.access_token}"},
                           json={
                               "name" : "user",
                               "user_name" : "username",
                               "password" : "12345678",
                               "amount" : 100,
                               "is_admin" : True                                                                                            
                           })
    assert response.status_code == 201

    response = client.post("/users/add_user",
                           headers={"Authorization": f"Bearer {admin_user_token.access_token}"},
                           json={
                               "name" : "user",
                               "user_name" : "username",
                               "password" : "12345678",
                               "amount" : 100,
                               "is_admin" : True                                                                                            
                           })
    assert response.status_code == 409

    db = TestingSession()
    user = db.execute(select(User).where(User.user_name == "username")).scalar_one_or_none()
    if user is not None:
        db.delete(user)
    db.commit()
    db.close()

def test_delete_user(normal_user_token):
    response = client.delete("/users/delete",
                             headers={"Authorization": f"Bearer {normal_user_token.access_token}"})
    assert response.status_code == 200

def test_get_me(normal_user_token):
    response = client.get("/users/me",
                             headers={"Authorization": f"Bearer {normal_user_token.access_token}"})
    assert response.status_code == 200