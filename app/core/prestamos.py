from sqlalchemy.orm import Session
from app.models.prestamos import Prestamo
from app.schemas.prestamos import PrestamoCreate, EstadoPrestamo
from datetime import datetime


def get_prestamo(db: Session, prestamo_id: int):
    """Obtiene un préstamo por su ID."""
    return db.query(Prestamo).filter(Prestamo.prestamo_id == prestamo_id).first()


def get_prestamos(db: Session, skip: int = 0, limit: int = 100):
    """Obtiene una lista de préstamos con paginación."""
    return db.query(Prestamo).offset(skip).limit(limit).all()


def create_prestamo(db: Session, prestamo: PrestamoCreate):
    """Crea un nuevo préstamo en la base de datos."""
    db_prestamo = Prestamo(**prestamo.dict())
    db.add(db_prestamo)
    db.commit()
    db.refresh(db_prestamo)
    return db_prestamo


def update_prestamo(db: Session, prestamo_id: int, prestamo: PrestamoCreate):
    """Actualiza un préstamo existente."""
    db_prestamo = get_prestamo(db, prestamo_id=prestamo_id)
    if db_prestamo:
        for var, value in vars(prestamo).items():
            setattr(db_prestamo, var, value) if value else None
        db.commit()
        db.refresh(db_prestamo)
        return db_prestamo
    else:
        return None  # O lanza una excepción, según tu manejo de errores


def delete_prestamo(db: Session, prestamo_id: int):
    """Elimina un préstamo de la base de datos."""
    db_prestamo = get_prestamo(db, prestamo_id=prestamo_id)
    if db_prestamo:
        db.delete(db_prestamo)
        db.commit()
        return True
    else:
        return False  # O lanza una excepción, según tu manejo de errore