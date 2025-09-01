from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from enum import Enum

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