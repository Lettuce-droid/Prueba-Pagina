from fastapi import FastAPI
from database import Base, engine
from routers import books, users

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Book Catalog API")

app.include_router(users.router)
app.include_router(books.router)

@app.get("/health")
def health_check():
    return {"status": "ok"}