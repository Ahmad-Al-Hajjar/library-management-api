from main import app
from database import get_db, get_test_db

app.dependency_overrides[get_db] = get_test_db