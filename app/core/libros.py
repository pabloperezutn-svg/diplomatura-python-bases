from sqlalchemy.orm import Session
from app.models.libros import Libro
from app.schemas.autores import LibroCreate

def get_libro(db: Session, libro_id: int):
    """Obtiene un libro por su ID."""
    return db.query(Libro).filter(Libro.libro_id == libro_id).first()


def get_libros(db: Session, skip: int = 0, limit: int = 100):
    """Obtiene una lista de libros con paginación."""
    return db.query(Libro).offset(skip).limit(limit).all()


def create_libro(db: Session, libro: LibroCreate):
    """Crea un nuevo libro en la base de datos."""
    db_libro = Libro(**libro.dict())
    db.add(db_libro)
    db.commit()
    db.refresh(db_libro)
    return db_libro


def update_libro(db: Session, libro_id: int, libro: LibroCreate):
    """Actualiza un libro existente."""
    db_libro = get_libro(db, libro_id=libro_id)
    if db_libro:
        for var, value in vars(libro).items():
            setattr(db_libro, var, value) if value else None
        db.commit()
        db.refresh(db_libro)
        return db_libro
    else:
        return None  # O lanza una excepción, según tu manejo de errores


def delete_libro(db: Session, libro_id: int):
    """Elimina un libro de la base de datos."""
    db_libro = get_libro(db, libro_id=libro_id)
    if db_libro:
        db.delete(db_libro)
        db.commit()
        return True
    else:
        return False  # O lanza una excepción, según tu manejo de errores