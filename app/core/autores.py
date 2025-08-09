from app.core.database import SessionLocal
from app.models.autores import Autor

class GestorAutores:
    def __init__(self):
        self.session = SessionLocal()

    def get_todos(self):
        return self.session.query(Autor).order_by(Autor.autor_id).all()

    def get_por_id(self, autor_id: int):
        return self.session.query(Autor).get(autor_id)

    def crear(self, datos_autor: dict):
        nuevo = Autor(**datos_autor)
        try:
            self.session.add(nuevo)
            self.session.commit()
            self.session.refresh(nuevo)
        except Exception as e:
            self.session.rollback()  # Revertir la transacción fallida
            print(f"Error: {e}")
        return nuevo

    def actualizar(self, autor_id: int, actualizacion: dict):
        autor = self.session.query(Autor).get(autor_id)
        if not autor:
            return None
        for campo, valor in actualizacion.items():
            setattr(autor, campo, valor)
        try:
            self.session.commit()
            self.session.refresh(autor)
        except Exception as e:
            self.session.rollback()
            print(f"Error: {e}")
        return autor

    def eliminar(self, autor_id: int):
        autor = self.session.query(Autor).get(autor_id)
        if not autor:
            return None
        try:
            self.session.delete(autor)
            self.session.commit()
        except Exception as e:
            self.session.rollback()
            print(f"Error: {e}")
        return autor

db = GestorAutores()
