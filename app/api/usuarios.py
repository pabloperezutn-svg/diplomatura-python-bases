from typing import List
from fastapi import Depends, APIRouter, HTTPException, Form
from fastapi.responses import RedirectResponse
from starlette.status import HTTP_303_SEE_OTHER
from datetime import date

from sqlalchemy.orm import Session

from app.core import usuarios as crud
from app.schemas import usuarios as schemas
from app.core.database import get_db

router = APIRouter()


@router.post("/usuarios/", response_model=schemas.Usuario)
def create_usuario(
    dni: str = Form(...),
    nombre: str = Form(...),
    apellido: str = Form(...),
    direccion: str = Form(None),
    telefono: str = Form(None),
    email: str = Form(...),
    fecha_nacimiento: date = Form(None),
    rol_id: int = Form(None),
    estado_id: int = Form(None),
    db: Session = Depends(get_db)
):
    """Crea un nuevo usuario."""
    usuario_data = {
        "dni": dni,
        "nombre": nombre,
        "apellido": apellido,
        "direccion": direccion,
        "telefono": telefono,
        "email": email,
        "fecha_nacimiento": fecha_nacimiento,
        "rol_id": rol_id,
        "estado_id": estado_id,
    }
    try:
        usuario = crud.create_usuario(db=db, usuario=schemas.UsuarioCreate(**usuario_data))
        return RedirectResponse(url="/usuarios", status_code=HTTP_303_SEE_OTHER)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/usuarios/{usuario_id}/update", response_model=schemas.Usuario)
def update_usuario(
    usuario_id: int,
    dni: str = Form(...),
    nombre: str = Form(...),
    apellido: str = Form(...),
    direccion: str = Form(None),
    telefono: str = Form(None),
    email: str = Form(...),
    fecha_nacimiento: date = Form(None),
    rol_id: int = Form(None),
    estado_id: int = Form(None),
    db: Session = Depends(get_db)
):
    """Actualiza un usuario existente."""
    usuario_data = {
        "dni": dni,
        "nombre": nombre,
        "apellido": apellido,
        "direccion": direccion,
        "telefono": telefono,
        "email": email,
        "fecha_nacimiento": fecha_nacimiento,
        "rol_id": rol_id,
        "estado_id": estado_id,
    }
    try:
        usuario = crud.update_usuario(db=db, usuario_id=usuario_id, usuario=schemas.UsuarioCreate(**usuario_data))
        if not usuario:
            raise HTTPException(status_code=404, detail="Usuario no encontrado")
        return RedirectResponse(url="/usuarios", status_code=HTTP_303_SEE_OTHER)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


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


@router.delete("/usuarios/{usuario_id}", response_model=bool)
def delete_usuario(usuario_id: int, db: Session = Depends(get_db)):
    """Elimina un usuario."""
    if not crud.delete_usuario(db, usuario_id=usuario_id):
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return True