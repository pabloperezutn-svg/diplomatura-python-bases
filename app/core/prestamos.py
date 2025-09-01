from app.core.database import SessionLocal
from app.models.prestamos import Prestamo
from app.schemas.prestamos import PrestamoCreate


class GestorPrestamos:
    def __init__(self):
        self.session = SessionLocal()

    def get_prestamo(self, prestamo_id: int):
        """Obtiene un préstamo por su ID."""
        return self.session.query(Prestamo).filter(Prestamo.prestamo_id == prestamo_id).first()

    def get_prestamos(self, skip: int = 0, limit: int = 100):
        """Obtiene una lista de préstamos con paginación."""
        return self.session.query(Prestamo).offset(skip).limit(limit).all()

    def create_prestamo(self, prestamo: PrestamoCreate):
        """Crea un nuevo préstamo en la base de datos."""
        db_prestamo = Prestamo(**prestamo.dict())
        self.session.add(db_prestamo)
        self.session.commit()
        self.session.refresh(db_prestamo)
        return db_prestamo

    def update_prestamo(self, prestamo_id: int, prestamo: PrestamoCreate):
        """Actualiza un préstamo existente."""
        db_prestamo = self.get_prestamo(prestamo_id=prestamo_id)
        if db_prestamo:
            for var, value in vars(prestamo).items():
                setattr(db_prestamo, var, value) if value else None
            self.session.commit()
            self.session.refresh(db_prestamo)
            return db_prestamo
        else:
            return None  # O lanza una excepción, según tu manejo de errores

    def delete_prestamo(self, prestamo_id: int):
        """Elimina un préstamo de la base de datos."""
        db_prestamo = self.get_prestamo(prestamo_id=prestamo_id)
        if db_prestamo:
            self.session.delete(db_prestamo)
            self.session.commit()
            return True
        else:
            return False  # O lanza una excepción, según tu manejo de errores


db = GestorPrestamos()