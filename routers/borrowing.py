from fastapi import APIRouter, HTTPException, Depends
from datetime import datetime
from database import get_db
from security.dependencies import get_current_user
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from sqlalchemy import select
from db_models import Borrow, User, Book
from schemas import (
    BorrowRequest,
    ReturnRequest
)
router = APIRouter()

@router.post("/borrow", status_code=201)
def borrow_book(data : BorrowRequest, db : Session = Depends(get_db), user = Depends(get_current_user)):
    try:
        st = (select(Book).where(Book.id == data.book_id).with_for_update())
        book = db.execute(st).scalar_one_or_none()
        if book is None:
            raise HTTPException(status_code=404, detail="book_not_found")

        if book.copies <= 0:
            raise HTTPException(status_code=409, detail="no_copies_available")

        for borrow in user.borrows:
            if borrow.book_id == data.book_id and borrow.returned_at is None:
                raise HTTPException(status_code=409, detail="already_borrowed")

        new_borrow = Borrow(
            user_id = user.id,
            book_id = data.book_id
        )
        db.add(new_borrow)

        book.copies -=1
        user.amount +=book.cost
        db.commit()
    
    except HTTPException:
        db.rollback()
        raise
    except Exception:
        db.rollback()
        raise HTTPException(status_code=500, detail="internal_server_error")   
    return {
        "message": "you borrowed the book successfully"
    }

@router.post("/return", status_code=201)
def return_book(data : ReturnRequest, db : Session = Depends(get_db), user = Depends(get_current_user)):
    try:
        st = (select(Book).where(Book.id == data.book_id).with_for_update())
        book = db.execute(st).scalar_one_or_none()
        if book is None:
            raise HTTPException(status_code=404, detail="book_not_found")
        borrow_r= None
        for borrow in user.borrows:
            if borrow.book_id == data.book_id and borrow.returned_at is None:
                borrow_r = borrow
                break
        if borrow_r is None:
            raise HTTPException(status_code=404, detail="borrow_record_not_found")

        borrow_r.returned_at = datetime.now()
        book.copies +=1
        db.commit()    
    except HTTPException:
        db.rollback()
        raise  

    except Exception:
        db.rollback()
        raise HTTPException(status_code=500, detail="internal_server_error")
    
    return {
        "message" : "You returned the book successfully"
        } 
