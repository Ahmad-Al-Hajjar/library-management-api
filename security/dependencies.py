from fastapi import HTTPException, Depends, Header
from database import get_db
from sqlalchemy.orm import Session
from db_models import Token
from datetime import datetime

def get_current_token(db : Session = Depends(get_db), authorization : str | None = Header(default=None)):
    if authorization is None:
        raise HTTPException(status_code=401, detail="token_missing")
    if not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="invalid_token")
    t = authorization.replace("Bearer ", "", 1)
    token = db.get(Token, t)
    if token is None:
        raise HTTPException(status_code=401, detail="invalid_token")
    if token.expires_at < datetime.now():
        raise HTTPException(status_code=401, detail="token_has_expired")
    return token

def get_current_user(token = Depends(get_current_token)):
    return token.user

def get_admin(user =Depends(get_current_user)):
    if not user.is_admin:
        raise HTTPException(status_code=403, detail="admin_required")
    return user