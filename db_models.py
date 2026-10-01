from database import Base
from sqlalchemy import String, Integer, DECIMAL, DateTime, ForeignKey, Boolean
from datetime import datetime, timedelta
from sqlalchemy.orm import Mapped, mapped_column, relationship

class Book(Base):
    __tablename__= "books"
    id :Mapped[int] = mapped_column(
        Integer,
        primary_key=True
    )
    name :Mapped[str] = mapped_column(
        String(100)
    )
    author :Mapped[str] = mapped_column(
        String(100)
    )
    copies :Mapped[int] = mapped_column(
        Integer
    )
    cost :Mapped[float] = mapped_column(
        DECIMAL(10, 2)
    )
    borrows :Mapped[list["Borrow"]] = relationship(
        back_populates="book"
    )

class User(Base):
    __tablename__="users"
    id:Mapped[int] =mapped_column(
        Integer,
        primary_key=True
    )
    name :Mapped[str] = mapped_column(
        String(100)
    )
    user_name :Mapped[str] = mapped_column(
        String(100),
        unique=True,
        index=True
    )
    password :Mapped[str] = mapped_column(
        String(255)
    )
    amount :Mapped[float] = mapped_column(
        DECIMAL(10, 2)
    )
    is_admin :Mapped[bool] = mapped_column(
        Boolean
    )
    borrows :Mapped[list["Borrow"]] = relationship(
        back_populates="user"
    )
    tokens :Mapped[list["Token"]] = relationship(
        back_populates="user"
    )

class Borrow(Base):
    __tablename__="records"
    id :Mapped[int] =mapped_column(
        Integer,
        primary_key=True
    )

    user_id :Mapped[int] =mapped_column(
        ForeignKey("users.id")
    )
    book_id :Mapped[int] =mapped_column(
        ForeignKey("books.id")
    )
    borrow_date: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.now
    )
    due_date: Mapped[datetime] = mapped_column(
        DateTime,
        default=lambda: datetime.now() + timedelta(days=5)
    )
    returned_at: Mapped[datetime | None] = mapped_column(
        DateTime,
        nullable=True
    )
    user :Mapped["User"] = relationship(
        back_populates="borrows"
    )
    book :Mapped["Book"] = relationship(
        back_populates="borrows"
    )

class Token(Base):
    __tablename__="tokens"
    access_token :Mapped[str] = mapped_column(
        String(200),
        primary_key=True
    ) 
    user_id :Mapped[int] = mapped_column(
        ForeignKey("users.id")
    )
    token_type :Mapped[str] = mapped_column(
        String(100)
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.now
    )
    expires_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=lambda: datetime.now() + timedelta(days=5)
    )
    user :Mapped["User"] = relationship(
        back_populates="tokens"
    )
    