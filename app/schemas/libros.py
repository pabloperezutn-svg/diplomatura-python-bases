from pydantic import BaseModel
from typing import Optional
from datetime import date,datetime
from enum import Enum


class LibroBase(BaseModel):
    titulo: str
    autor_id: int
    editorial_id: Optional[int] = None
    isbn: Optional[int] = None
    anio_publicacion: Optional[int] = None
    edicion: Optional[str] = None
    categoria_id: Optional[int] = None
    cantidad_ejemplares: Optional[int] = 1
    ejemplares_disponibles: Optional[int] = 1
    resumen: Optional[str] = None
    portada: Optional[bytes] = None
    ubicacion_id: Optional[int] = None


class LibroCreate(LibroBase):
    pass  # agregar validaciones específicas aquí


class Libro(LibroBase):
    libro_id: int
    fecha_creacion: datetime  # Usa el datetime importado

    class Config:
        orm_mode = True  # Permite crear un Libro desde un objeto SQLAlchemy