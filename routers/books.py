from fastapi import APIRouter, HTTPException, Query, Depends
from sqlalchemy import select
from sqlalchemy.orm import Session
from database import get_db
from security.dependencies import get_admin
from db_models import Book, Borrow
from schemas import (BookRequest,
                    BookUpdate,
                    BookResponse)

router = APIRouter(prefix="/books")

@router.get("/{id}")
def get_book(id : int, db :Session =Depends(get_db)):
    book = db.get(Book, id)
    if book is None:
        raise HTTPException(status_code=404, detail="book not found")
    return book


@router.post("", status_code=201, response_model=BookResponse)
def add_book(
    book: BookRequest,
    db: Session = Depends(get_db),
    user = Depends(get_admin)
):
    new_book = Book(
        name=book.name,
        author=book.author,
        copies=book.copies,
        cost=book.cost
    )

    db.add(new_book)
    db.commit()
    db.refresh(new_book)

    return new_book

@router.delete("/{id}", status_code=200)
def delete_book(
     id :int,
     db =Depends(get_db),
     user = Depends(get_admin)):
    book =db.get(Book, id)
    if book is None:
            raise HTTPException(
                status_code=404,
                detail="book_not_found"
            )
    for borrow in book.borrows:
        if borrow.returned_at is None:
             raise HTTPException(status_code=400, detail="borrowed_book_cannot_be_delete")
    db.delete(book)
    db.commit()
    return {
         "message" : "Book removed successfully"}

@router.put("/{id}")
def update_book(
     id :int,
     data : BookUpdate,
     db = Depends(get_db),
     user = Depends(get_admin)):

    book =db.get(Book, id)
    if book is None:
            raise HTTPException(
                status_code=404,
                detail="book_not_found"
            )
    book.name = data.name
    book.author = data.author
    book.copies = data.copies
    book.cost = data.cost

    db.commit()
    return {
        "message" : "Book updated successfully"
    }

@router.get("", response_model=list[BookResponse])
def get_books(name : str | None = None,
               author : str | None = None,
               min_cost : float | None = Query(default=None, ge=0),
               max_cost : float | None = Query(default=None, ge=0),
               skip : int = Query(default=0, ge=0),
               limit : int = Query(default=10, ge=1, le=30), 
               db :Session = Depends(get_db)):

    if min_cost is not None and max_cost is not None and min_cost > max_cost:
         raise HTTPException(status_code=400, detail="min_cost_cannot_be_greater_than_max_cost")
    
    st = select(Book)

    if name is not None:
        for word in name.split():
            st = st.where(Book.name.ilike(f"%{word}%"))
    if author is not None:
        for word in author.split():
            st = st.where(Book.author.ilike(f"%{word}%"))
    if min_cost is not None:
            st = st.where(Book.cost >= min_cost)
    if max_cost is not None:
            st = st.where(Book.cost <= max_cost)
    st = st.order_by(Book.id)
    st = st.offset(skip).limit(limit)
    books = db.execute(st).scalars().all()
    
    return books
