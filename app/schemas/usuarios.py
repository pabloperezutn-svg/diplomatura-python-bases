from pydantic import BaseModel
from typing import Optional
from datetime import date,datetime
from enum import Enum

class UsuarioBase(BaseModel):
    dni: str
    nombre: str
    apellido: str
    direccion: Optional[str] = None
    telefono: Optional[str] = None
    email: str
    fecha_nacimiento: Optional[date] = None
    rol_id: Optional[int] = None
    estado_id: Optional[int] = None


class UsuarioCreate(UsuarioBase):
    pass  # Puedes agregar validaciones específicas aquí


class Usuario(UsuarioBase):
    usuario_id: int
    fecha_registro: datetime

    class Config:
        orm_mode = True    
