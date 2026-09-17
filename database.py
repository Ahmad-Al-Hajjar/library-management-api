from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase
DATABASE_URL = ("mysql+pymysql://root:1234@localhost:3306/Library")

engine = create_engine(DATABASE_URL, echo=True)

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



test_db_url = ("mysql+pymysql://root:1234@localhost:3306/Library_test")
test_engine = create_engine(test_db_url, echo=True)

TestingSession = sessionmaker(bind= test_engine, autoflush=False, autocommit=False)

def get_test_db():
    db = TestingSession()
    try:
        yield db
    finally:
        db.close()