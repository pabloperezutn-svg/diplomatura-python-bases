from app.core.database import SessionLocal
from app.models.usuarios import Usuario
from app.schemas.usuarios import UsuarioCreate


class GestorUsuarios:
    def __init__(self):
        self.session = SessionLocal()

    def get_usuario(self, usuario_id: int):
        """Obtiene un usuario por su ID."""
        return self.session.query(Usuario).filter(Usuario.usuario_id == usuario_id).first()

    def get_usuarios(self, skip: int = 0, limit: int = 100):
        """Obtiene una lista de usuarios con paginación."""
        return self.session.query(Usuario).offset(skip).limit(limit).all()

    def create_usuario(self, usuario: UsuarioCreate):
        """Crea un nuevo usuario en la base de datos."""
        db_usuario = Usuario(**usuario.dict())
        self.session.add(db_usuario)
        self.session.commit()
        self.session.refresh(db_usuario)
        return db_usuario

    def update_usuario(self, usuario_id: int, usuario: UsuarioCreate):
        """Actualiza un usuario existente."""
        db_usuario = self.get_usuario(usuario_id=usuario_id)
        if db_usuario:
            for var, value in vars(usuario).items():
                setattr(db_usuario, var, value) if value else None
            self.session.commit()
            self.session.refresh(db_usuario)
            return db_usuario
        else:
            return None  # O lanza una excepción, según tu manejo de errores

    def delete_usuario(self, usuario_id: int):
        """Elimina un usuario de la base de datos."""
        db_usuario = self.get_usuario(usuario_id=usuario_id)
        if db_usuario:
            self.session.delete(db_usuario)
            self.session.commit()
            return True
        else:
            return False  # O lanza una excepción, según tu manejo de errores


db = GestorUsuarios()