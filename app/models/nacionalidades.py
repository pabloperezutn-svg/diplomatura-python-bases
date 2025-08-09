from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.core.database import Base

class Nacionalidad(Base):
    __tablename__ = 'nacionalidad'
    nacionalidad_id = Column(Integer, primary_key=True)
    sdes = Column(String)

    autores = relationship("Autor", back_populates="nacionalidad")

    def __repr__(self):
        return self.sdes
