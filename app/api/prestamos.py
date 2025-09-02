from typing import List
from fastapi import Depends, APIRouter, HTTPException, Form
from fastapi.responses import RedirectResponse
from starlette.status import HTTP_303_SEE_OTHER
from datetime import date

from sqlalchemy.orm import Session

from app.core import prestamos as crud
from app.schemas import prestamos as schemas
from app.schemas.prestamos import EstadoPrestamo  # Importa el Enum
from app.core.database import get_db

router = APIRouter(tags=["Prestamos API"])


@router.post("/prestamos/", response_model=schemas.Prestamo)
def create_prestamo(
    libro_id: int = Form(...),
    usuario_id: int = Form(...),
    fecha_devolucion_esperada: date = Form(...),
    fecha_devolucion_real: date = Form(None),
    estado: EstadoPrestamo = Form(EstadoPrestamo.activo),
    multa: float = Form(0.0),
    notas: str = Form(None),
    db: Session = Depends(get_db)
):
    """Crea un nuevo préstamo."""
    prestamo_data = {
        "libro_id": libro_id,
        "usuario_id": usuario_id,
        "fecha_devolucion_esperada": fecha_devolucion_esperada,
        "fecha_devolucion_real": fecha_devolucion_real,
        "estado": estado,
        "multa": multa,
        "notas": notas,
    }
    try:
        prestamo = crud.create_prestamo(db=db, prestamo=schemas.PrestamoCreate(**prestamo_data))
        return RedirectResponse(url="/prestamos", status_code=HTTP_303_SEE_OTHER)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/prestamos/{prestamo_id}/update", response_model=schemas.Prestamo)
def update_prestamo(
    prestamo_id: int,
    libro_id: int = Form(...),
    usuario_id: int = Form(...),
    fecha_devolucion_esperada: date = Form(...),
    fecha_devolucion_real: date = Form(None),
    estado: EstadoPrestamo = Form(EstadoPrestamo.activo),
    multa: float = Form(0.0),
    notas: str = Form(None),
    db: Session = Depends(get_db)
):
    """Actualiza un préstamo existente."""
    prestamo_data = {
        "libro_id": libro_id,
        "usuario_id": usuario_id,
        "fecha_devolucion_esperada": fecha_devolucion_esperada,
        "fecha_devolucion_real": fecha_devolucion_real,
        "estado": estado,
        "multa": multa,
        "notas": notas,
    }
    try:
        prestamo = crud.update_prestamo(db=db, prestamo_id=prestamo_id, prestamo=schemas.PrestamoCreate(**prestamo_data))
        if not prestamo:
            raise HTTPException(status_code=404, detail="Prestamo no encontrado")
        return RedirectResponse(url="/prestamos", status_code=HTTP_303_SEE_OTHER)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


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


@router.delete("/prestamos/{prestamo_id}", response_model=bool)
def delete_prestamo(prestamo_id: int, db: Session = Depends(get_db)):
    """Elimina un préstamo."""
    if not crud.delete_prestamo(db, prestamo_id=prestamo_id):
        raise HTTPException(status_code=404, detail="Prestamo no encontrado")
    return True