from pydantic import BaseModel
from typing import Optional
from datetime import date,datetime
from enum import Enum


class AutorBase(BaseModel):
    nombre: str
    apellido: str
    fecha_nacimiento: Optional[date] = None
    nacionalidad_id: Optional[int] = None
    biografia: Optional[str] = None

class Autor(AutorBase):
    autor_id: int

    model_config = {
        "from_attributes": True
    }

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

class PrestamoBase(BaseModel):
    libro_id: int
    usuario_id: int
    fecha_inicio: date
    fecha_fin: date
    fecha_devolucion: Optional[date] = None
    devuelto: bool = False

class PrestamoCreate(PrestamoBase):
    pass  # Puedes agregar validaciones específicas aquí

class Prestamo(PrestamoBase):
    id: int

    class Config:
        orm_mode = True

class EstadoPrestamo(str, Enum):
    activo = "activo"
    completado = "completado"
    atrasado = "atrasado"
    perdido = "perdido"

class PrestamoBase(BaseModel):
    libro_id: int
    usuario_id: int
    fecha_devolucion_esperada: datetime
    fecha_devolucion_real: Optional[datetime] = None
    estado: EstadoPrestamo = EstadoPrestamo.activo
    multa: float = 0.0
    notas: Optional[str] = None

class PrestamoCreate(PrestamoBase):
    pass  # Puedes agregar validaciones específicas aquí

class Prestamo(PrestamoBase):
    prestamo_id: int
    fecha_prestamo: datetime

    class Config:
        orm_mode = True


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
