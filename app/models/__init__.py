from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

from .autores import Autor
from .nacionalidades import Nacionalidad
from .libros import Libro
from .usuarios import Usuario  
from .prestamos import Prestamo  