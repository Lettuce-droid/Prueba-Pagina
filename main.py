from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from database import Base, engine
from routers import books, users

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Book Catalog API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(users.router)
app.include_router(books.router)

@app.get("/health")
def health_check():
    return {"status": "ok"}

@app.get("/")
def serve_frontend():
    return FileResponse("index.html")