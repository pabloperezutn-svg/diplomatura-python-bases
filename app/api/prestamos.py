from sqlalchemy.orm import Session
from app.models.prestamos import Prestamo
from app.schemas.prestamos import PrestamoCreate, EstadoPrestamo
from datetime import datetime

from typing import List
from fastapi import Depends, Request, HTTPException, APIRouter
from fastapi.responses import HTMLResponse
from app.core import prestamos as crud
from app.models import prestamos as models
from app.schemas import autores as schemas
from app.core.database import get_db

router = APIRouter(tags=["Prestamos API"])

@router.post("/prestamos/", response_model=schemas.Prestamo)
def create_prestamo(prestamo: schemas.PrestamoCreate, db: Session = Depends(get_db)):
    """Crea un nuevo préstamo."""
    return crud.create_prestamo(db=db, prestamo=prestamo)


@router.get("/prestamos/", response_model=List[schemas.Prestamo])
def read_prestamos(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Obtiene una lista de préstamos."""
    prestamos = crud.get_prestamos(db, skip=skip, limit=limit)
    return prestamos


@router.get("/prestamos/{prestamo_id}", response_model=schemas.Prestamo)
def read_prestamo(prestamo_id: int, db: Session = Depends(get_db)):
    """Obtiene un préstamo por su ID."""
    db_prestamo = crud.get_prestamo(db, prestamo_id=prestamo_id)
    if db_prestamo is None:
        raise HTTPException(status_code=404, detail="Prestamo no encontrado")
    return db_prestamo


@router.put("/prestamos/{prestamo_id}", response_model=schemas.Prestamo)
def update_prestamo(prestamo_id: int, prestamo: schemas.PrestamoCreate, db: Session = Depends(get_db)):
    """Actualiza un préstamo existente."""
    db_prestamo = crud.update_prestamo(db, prestamo_id=prestamo_id, prestamo=prestamo)
    if db_prestamo is None:
        raise HTTPException(status_code=404, detail="Prestamo no encontrado")
    return db_prestamo


@router.delete("/prestamos/{prestamo_id}", response_model=bool)
def delete_prestamo(prestamo_id: int, db: Session = Depends(get_db)):
    """Elimina un préstamo."""
    if not crud.delete_prestamo(db, prestamo_id=prestamo_id):
        raise HTTPException(status_code=404, detail="Prestamo no encontrado")
    return True