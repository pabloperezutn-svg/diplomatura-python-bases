from app.core.database import SessionLocal
from app.models.libros import Libro
from app.schemas.libros import LibroCreate


class GestorLibros:
    def __init__(self):
        self.session = SessionLocal()

    def get_libro(self, libro_id: int):
        """Obtiene un libro por su ID."""
        return self.session.query(Libro).filter(Libro.libro_id == libro_id).first()

    def get_libros(self, skip: int = 0, limit: int = 100):
        """Obtiene una lista de libros con paginación."""
        return self.session.query(Libro).offset(skip).limit(limit).all()

    def create_libro(self, libro: LibroCreate):
        """Crea un nuevo libro en la base de datos."""
        db_libro = Libro(**libro.dict())
        self.session.add(db_libro)
        self.session.commit()
        self.session.refresh(db_libro)
        return db_libro

    def update_libro(self, libro_id: int, libro: LibroCreate):
        """Actualiza un libro existente."""
        db_libro = self.get_libro(libro_id=libro_id)
        if db_libro:
            for var, value in vars(libro).items():
                setattr(db_libro, var, value) if value else None
            self.session.commit()
            self.session.refresh(db_libro)
            return db_libro
        else:
            return None  # O lanza una excepción, según tu manejo de errores

    def delete_libro(self, libro_id: int):
        """Elimina un libro de la base de datos."""
        db_libro = self.get_libro(libro_id=libro_id)
        if db_libro:
            self.session.delete(db_libro)
            self.session.commit()
            return True
        else:
            return False  # O lanza una excepción, según tu manejo de errores


db = GestorLibros()