from fastapi import APIRouter ,HTTPException, Depends
from database import get_db
from sqlalchemy.orm import Session
from sqlalchemy import select
from secrets import token_urlsafe
from db_models import Token, User, Borrow
from security.password import verify_password
from security.dependencies import get_current_user, get_current_token
from schemas import (LoginRequest,
                     TokenResponse)

router = APIRouter(prefix="/auth")

@router.post("/login",response_model = TokenResponse)
def login(data :LoginRequest, db : Session = Depends(get_db)):
    st = select(User).where(User.user_name == data.user_name)
    user = db.execute(st).scalar_one_or_none()
    if user is None:
        raise HTTPException(status_code=401, detail="invalid_credentials")
    verify = verify_password(data.password, user.password)
    if not verify :
        raise HTTPException(status_code=401, detail="invalid_credentials")
    token = Token(
        access_token = token_urlsafe(32),
        user_id = user.id,
        token_type = "bearer"
    )
    db.add(token)
    db.commit()
    db.refresh(token)

    return token

@router.delete("/logout")
def logout(token = Depends(get_current_token), db : Session =Depends(get_db)):
    db.delete(token)
    db.commit()
    return "success"

@router.get("/me")
def get_token(user = Depends(get_current_user)):
    return{
        "id": user.id,
        "name": user.name,
        "user_name": user.user_name
    }

















