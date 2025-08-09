from app.core.database import SessionLocal
from app.models.nacionalidades import Nacionalidad

class GestorNacionalidades:
    def __init__(self):
        self.session = SessionLocal()

    def get_todos(self, order_by: Nacionalidad = Nacionalidad.nacionalidad_id, desc: bool = False):
        if desc:
            return self.session.query(Nacionalidad).order_by(order_by.desc()).all()
        return self.session.query(Nacionalidad).order_by(order_by).all()

    def get_por_id(self, nacionalidad_id: int):
        return self.session.query(Nacionalidad).get(nacionalidad_id)

    def crear(self, datos_nacionalidad: dict):
        nuevo = Nacionalidad(**datos_nacionalidad)
        try:
            self.session.add(nuevo)
            self.session.commit()
            self.session.refresh(nuevo)
        except Exception as e:
            self.session.rollback()
            print(f"Error: {e}")
        return nuevo

    def actualizar(self, nacionalidad_id: int, actualizacion: dict):
        nacionalidad = self.session.query(Nacionalidad).get(nacionalidad_id)
        if not nacionalidad:
            return None
        for campo, valor in actualizacion.items():
            setattr(nacionalidad, campo, valor)
        try:
            self.session.commit()
            self.session.refresh(nacionalidad)
        except Exception as e:
            self.session.rollback()
            print(f"Error: {e}")
        return nacionalidad

    def eliminar(self, nacionalidad_id: int):
        nacionalidad = self.session.query(Nacionalidad).get(nacionalidad_id)
        if not nacionalidad:
            return None
        try:
            self.session.delete(nacionalidad)
            self.session.commit()
        except Exception as e:
            self.session.rollback()
            print(f"Error: {e}")
        return nacionalidad

db = GestorNacionalidades()
