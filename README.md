# Library Management API

A backend API for managing a library system using FastAPI, SQLAlchemy, and MySQL.

The project supports users, books, borrowing and returning books, authentication, authorization, testing, and database migrations with Alembic.

---

## Technologies

- Python
- FastAPI
- SQLAlchemy
- MySQL
- PyMySQL
- Pydantic
- bcrypt
- Alembic
- pytest

---

## Project Structure

```text
Python.pro/
│
├── alembic/
│   ├── versions/
│   ├── env.py
│   └── script.py.mako
│
├── routers/
│   ├── auth.py
│   ├── books.py
│   ├── borrowing.py
│   └── users.py
│
├── security/
│   └── password.py
│
├── tests/
│   ├── dependencies.py
│   ├── test_auth.py
│   ├── test_books.py
│   ├── test_borrowing.py
│   └── test_users.py
│
├── config.py
├── database.py
├── db_models.py
├── schemas.py
├── main.py
├── alembic.ini
├── requirements.txt
├── .env
└── .gitignore