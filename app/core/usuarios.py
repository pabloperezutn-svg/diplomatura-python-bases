from sqlalchemy.orm import Session
from app.models.usuarios import Usuario
from app.schemas.usuarios import UsuarioCreate

def get_usuario(db: Session, usuario_id: int):
    """Obtiene un usuario por su ID."""
    return db.query(Usuario).filter(Usuario.usuario_id == usuario_id).first()


def get_usuarios(db: Session, skip: int = 0, limit: int = 100):
    """Obtiene una lista de usuarios con paginación."""
    return db.query(Usuario).offset(skip).limit(limit).all()


def create_usuario(db: Session, usuario: UsuarioCreate):
    """Crea un nuevo usuario en la base de datos."""
    db_usuario = Usuario(**usuario.dict())
    db.add(db_usuario)
    db.commit()
    db.refresh(db_usuario)
    return db_usuario


def update_usuario(db: Session, usuario_id: int, usuario: UsuarioCreate):
    """Actualiza un usuario existente."""
    db_usuario = get_usuario(db, usuario_id=usuario_id)
    if db_usuario:
        for var, value in vars(usuario).items():
            setattr(db_usuario, var, value) if value else None
        db.commit()
        db.refresh(db_usuario)
        return db_usuario
    else:
        return None  # O lanza una excepción, según tu manejo de errores


def delete_usuario(db: Session, usuario_id: int):
    """Elimina un usuario de la base de datos."""
    db_usuario = get_usuario(db, usuario_id=usuario_id)
    if db_usuario:
        db.delete(db_usuario)
        db.commit()
        return True
    else:
        return False  # O lanza una excepción, según tu manejo de errores