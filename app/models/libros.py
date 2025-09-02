# app/models/libros.py

from sqlalchemy import Column, Integer, String, ForeignKey, Text, LargeBinary, TIMESTAMP, Identity
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base

class Libro(Base):
    __tablename__ = "libros"

    libro_id = Column(Integer, Identity(), primary_key=True, index=True)  # Autoincremental
    titulo = Column(String, nullable=False)
    autor_id = Column(Integer, ForeignKey("autores.id"), nullable=False)
    editorial_id = Column(Integer, ForeignKey("editoriales.id"))  # Tabla "editoriales"
    isbn = Column(Integer)
    anio_publicacion = Column(Integer)
    edicion = Column(String)
    categoria_id = Column(Integer)
    cantidad_ejemplares = Column(Integer, default=1)
    ejemplares_disponibles = Column(Integer, default=1)
    resumen = Column(Text)
    portada = Column(LargeBinary)  # BLOB para la portada
    fecha_creacion = Column(TIMESTAMP(timezone=True), server_default=func.now()) # Fecha de creación automática
    ubicacion_id = Column(Integer)

    # Relaciones
    autor = relationship("Autor", back_populates="libros")  # Relación con el modelo Autor
    editorial = relationship("Editorial", back_populates="libros") # Relación con el modelo Editorial 
    prestamos = relationship("Prestamo", back_populates="libro") # Relación con el modelo Prestamo

    def __repr__(self):
        return f"<Libro(titulo='{self.titulo}')>"