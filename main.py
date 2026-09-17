from fastapi import FastAPI      
from routers.books import router as books_router
from routers.users import router as users_router
from routers.borrowing import router as borrowing_router
from routers.auth import router as auth_router

app = FastAPI()
app.include_router(books_router)
app.include_router(users_router)
app.include_router(borrowing_router)
app.include_router(auth_router)


