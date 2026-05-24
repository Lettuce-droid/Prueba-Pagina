from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
import models
import schemas
import auth
from database import get_db

router = APIRouter(prefix="/books", tags=["books"])

@router.get("/", response_model=List[schemas.BookResponse])
def get_books(db: Session = Depends(get_db)):
    return db.query(models.Book).all()

@router.post("/", response_model=schemas.BookResponse)
def create_book(book: schemas.BookCreate, db: Session = Depends(get_db), current_user: models.User = Depends(auth.get_current_user)):
    new_book = models.Book(**book.model_dump(), owner_id=current_user.id)
    db.add(new_book)
    db.commit()
    db.refresh(new_book)
    return new_book

@router.put("/{book_id}", response_model=schemas.BookResponse)
def update_book(book_id: int, book_data: schemas.BookUpdate, db: Session = Depends(get_db), current_user: models.User = Depends(auth.get_current_user)):
    book = db.query(models.Book).filter(models.Book.id == book_id).first()
    if not book:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Libro no encontrado")
    if book.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="No tienes permiso para editar este libro")
    for field, value in book_data.model_dump(exclude_none=True).items():
        setattr(book, field, value)
    db.commit()
    db.refresh(book)
    return book

@router.delete("/{book_id}")
def delete_book(book_id: int, db: Session = Depends(get_db), current_user: models.User = Depends(auth.get_current_user)):
    book = db.query(models.Book).filter(models.Book.id == book_id).first()
    if not book:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Libro no encontrado")
    if book.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="No tienes permiso para eliminar este libro")
    db.delete(book)
    db.commit()
    return {"detail": "Libro eliminado"}