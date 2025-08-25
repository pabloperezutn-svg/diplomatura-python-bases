from typing import List

from fastapi import Depends, APIRouter, HTTPException
from sqlalchemy.orm import Session

from app.core import usuarios as crud
from app.models import usuarios as models
from app.schemas import usuarios as schemas
from app.core.database import get_db

router = APIRouter()


@router.post("/usuarios/", response_model=schemas.Usuario)
def create_usuario(usuario: schemas.UsuarioCreate, db: Session = Depends(get_db)):
    """Crea un nuevo usuario."""
    return crud.create_usuario(db=db, usuario=usuario)


@router.get("/usuarios/", response_model=List[schemas.Usuario])
def read_usuarios(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Obtiene una lista de usuarios."""
    usuarios = crud.get_usuarios(db, skip=skip, limit=limit)
    return usuarios


@router.get("/usuarios/{usuario_id}", response_model=schemas.Usuario)
def read_usuario(usuario_id: int, db: Session = Depends(get_db)):
    """Obtiene un usuario por su ID."""
    db_usuario = crud.get_usuario(db, usuario_id=usuario_id)
    if db_usuario is None:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return db_usuario


@router.put("/usuarios/{usuario_id}", response_model=schemas.Usuario)
def update_usuario(usuario_id: int, usuario: schemas.UsuarioCreate, db: Session = Depends(get_db)):
    """Actualiza un usuario existente."""
    db_usuario = crud.update_usuario(db, usuario_id=usuario_id, usuario=usuario)
    if db_usuario is None:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return db_usuario


@router.delete("/usuarios/{usuario_id}", response_model=bool)
def delete_usuario(usuario_id: int, db: Session = Depends(get_db)):
    """Elimina un usuario."""
    if not crud.delete_usuario(db, usuario_id=usuario_id):
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return True