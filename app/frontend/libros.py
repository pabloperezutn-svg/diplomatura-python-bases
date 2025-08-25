from typing import List
from fastapi import Depends, Request, HTTPException, APIRouter
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session
from fastapi.templating import Jinja2Templates
from app.core import libros as crud
from app.models import libros as models
from app.schemas import autores as schemas
from app.core.database import get_db




router = APIRouter(tags=["Frontend Libros"])
templates = Jinja2Templates(directory="templates")


@router.post("/libros/", response_model=schemas.Libro)
def create_libro(libro: schemas.LibroCreate, db: Session = Depends(get_db)):
    """Crea un nuevo libro."""
    return crud.create_libro(db=db, libro=libro)


@router.get("/libros/", response_model=List[schemas.Libro])
def read_libros(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Obtiene una lista de libros."""
    libros = crud.get_libros(db, skip=skip, limit=limit)
    return libros


@router.get("/libros/{libro_id}", response_model=schemas.Libro)
def read_libro(libro_id: int, db: Session = Depends(get_db)):
    """Obtiene un libro por su ID."""
    db_libro = crud.get_libro(db, libro_id=libro_id)
    if db_libro is None:
        raise HTTPException(status_code=404, detail="Libro no encontrado")
    return db_libro


@app.put("/libros/{libro_id}", response_model=schemas.Libro)
def update_libro(libro_id: int, libro: schemas.LibroCreate, db: Session = Depends(get_db)):
    """Actualiza un libro existente."""
    db_libro = crud.update_libro(db, libro_id=libro_id, libro=libro)
    if db_libro is None:
        raise HTTPException(status_code=404, detail="Libro no encontrado")
    return db_libro


@app.delete("/libros/{libro_id}", response_model=bool)
def delete_libro(libro_id: int, db: Session = Depends(get_db)):
    """Elimina un libro."""
    if not crud.delete_libro(db, libro_id=libro_id):
        raise HTTPException(status_code=404, detail="Libro no encontrado")
    return True