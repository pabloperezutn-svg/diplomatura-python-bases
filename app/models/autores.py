from sqlalchemy import Column, Integer, String, Date, Text, ForeignKey
from sqlalchemy.orm import relationship
from app.core.database import Base

class Autor(Base):
    __tablename__ = 'autores'
    autor_id = Column(Integer, primary_key=True)
    nombre = Column(String)
    apellido = Column(String)
    fecha_nacimiento = Column(Date, nullable=True)
    nacionalidad_id = Column(Integer, ForeignKey('nacionalidad.nacionalidad_id'))
    biografia = Column(Text, nullable=True)

    nacionalidad = relationship("Nacionalidad", back_populates="autores")
    #libros = relationship("Libro", back_populates="autor")

    def __repr__(self):
        return f"{self.apellido}, {self.nombre}"
