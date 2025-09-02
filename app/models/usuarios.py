from sqlalchemy import Column, Integer, String, Date, Identity, TIMESTAMP
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from sqlalchemy import ForeignKey
from app.core.database import Base

class Usuario(Base):
    __tablename__ = "usuarios"

    usuario_id = Column(Integer, Identity(), primary_key=True, index=True)  # Autoincremental
    dni = Column(String, unique=True, nullable=False)
    nombre = Column(String, nullable=False)
    apellido = Column(String, nullable=False)
    direccion = Column(String)
    telefono = Column(String)
    email = Column(String, unique=True, nullable=False)
    fecha_nacimiento = Column(Date)
    fecha_registro = Column(TIMESTAMP(timezone=True), server_default=func.now())
    rol_id = Column(Integer, ForeignKey("roles.id"))  # Asumo que tienes una tabla "roles"
    estado_id = Column(Integer)

    # Relación con el modelo Prestamo (un usuario puede tener varios prestamos)
    prestamos = relationship("Prestamo", back_populates="usuario")

    def __repr__(self):
        return f"<Usuario(nombre='{self.nombre}', apellido='{self.apellido}')>"