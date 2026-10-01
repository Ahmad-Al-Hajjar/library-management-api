from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase
from config import settings

engine = create_engine(settings.database_url, echo=True)

SessionLocal =sessionmaker(bind=engine, autoflush=False, autocommit=False)

class Base(DeclarativeBase):
    pass

def get_db():
    db =SessionLocal()
    try:
        yield db
    finally:
        db.close()



######################




test_engine = create_engine(settings.test_database_url, echo=True)

TestingSession = sessionmaker(bind= test_engine, autoflush=False, autocommit=False)

def get_test_db():
    db = TestingSession()
    try:
        yield db
    finally:
        db.close()