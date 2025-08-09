from pydantic import BaseModel
from typing import Optional
from datetime import date

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