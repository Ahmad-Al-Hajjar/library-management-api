from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from sqlalchemy import select
from database import get_db
from security.dependencies import get_current_user, get_admin
from db_models import User, Token
from security.password import hash_password
from schemas import(UserRequest,
                    UserResponse)
router = APIRouter(prefix="/users")

@router.get("", response_model=list[UserResponse])
def get_users(db : Session =Depends(get_db)):
    st = select(User)
    users = db.execute(st).scalars().all()
    return users

@router.get("/me", status_code=200, response_model=UserResponse)
def get_user(db : Session =Depends(get_db), c_user = Depends(get_current_user)):
    return c_user

@router.delete("/delete", status_code=200)
def delete_user(db : Session =Depends(get_db), c_user = Depends(get_current_user)):
    try:
        user = db.get(User, c_user.id)
        tokens = db.execute(select(Token).where(Token.user_id == user.id)).scalars().all()

        for token in tokens:
            db.delete(token)

        db.delete(user)  
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=409,
            detail="user_cannot_be_deleted"
        )
    except Exception:
        db.rollback()
        raise HTTPException(status_code=500, detail="internal_server_error")
    return "success"

@router.post("/add_user", response_model=UserResponse, status_code=201)
def add_user(data : UserRequest, db : Session = Depends(get_db), c_user = Depends(get_admin)):
    hashed = hash_password(data.password)
    user =User(
        name = data.name,
        user_name = data.user_name,
        password = hashed,
        amount = data.amount,
        is_admin = data.is_admin     
        )
    try:
        db.add(user)
        db.commit()
        db.refresh(user)
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=409,
            detail="user_name_already_exists"
        )
    except Exception:
        db.rollback()
        raise HTTPException(status_code=500, detail="internal_server_error")
    return user

@router.get("/borrow_record")
def borrow_record(db : Session =Depends(get_db), c_user = Depends(get_current_user)):
    return c_user.borrows

