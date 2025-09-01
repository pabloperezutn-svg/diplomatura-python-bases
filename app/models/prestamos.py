from sqlalchemy import Column, Integer, Date, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from app.core.database import Base

class Prestamo(Base):
    __tablename__ = "prestamos"

    id = Column(Integer, primary_key=True, index=True)
    libro_id = Column(Integer, ForeignKey("libros.libro_id"))
    usuario_id = Column(Integer, ForeignKey("usuarios.id"))
    fecha_inicio = Column(Date, nullable=False)
    fecha_fin = Column(Date, nullable=False)
    fecha_devolucion = Column(Date, nullable=True)
    devuelto = Column(Boolean, default=False) # Indica si el libro fue devuelto o no

    # Relaciones
    libro = relationship("Libro", back_populates="prestamos")
    usuario = relationship("Usuario", back_populates="prestamos")

    def __repr__(self):
        return f"<Prestamo(id={self.id}, libro_id={self.libro_id}, usuario_id={self.usuario_id})>"