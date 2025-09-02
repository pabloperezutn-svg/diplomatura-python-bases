from typing import List
from fastapi import Depends, APIRouter, HTTPException, Form
from fastapi.responses import RedirectResponse
from starlette.status import HTTP_303_SEE_OTHER

from sqlalchemy.orm import Session

from app.core import libros as crud
from app.schemas import libros as schemas
from app.core.database import get_db

router = APIRouter(tags=["Libros API"])


@router.post("/libros/", response_model=schemas.Libro)
def create_libro(
    titulo: str = Form(...),
    autor_id: int = Form(...),
    editorial_id: int = Form(None),
    isbn: int = Form(None),
    anio_publicacion: int = Form(None),
    edicion: str = Form(None),
    categoria_id: int = Form(None),
    cantidad_ejemplares: int = Form(1),
    ejemplares_disponibles: int = Form(1),
    resumen: str = Form(None),
    portada: bytes = Form(None),
    ubicacion_id: int = Form(None),
    db: Session = Depends(get_db)
):
    """Crea un nuevo libro."""
    libro_data = {
        "titulo": titulo,
        "autor_id": autor_id,
        "editorial_id": editorial_id,
        "isbn": isbn,
        "anio_publicacion": anio_publicacion,
        "edicion": edicion,
        "categoria_id": categoria_id,
        "cantidad_ejemplares": cantidad_ejemplares,
        "ejemplares_disponibles": ejemplares_disponibles,
        "resumen": resumen,
        "portada": portada,
        "ubicacion_id": ubicacion_id,
    }
    try:
        libro = crud.create_libro(db=db, libro=schemas.LibroCreate(**libro_data))
        return RedirectResponse(url="/libros", status_code=HTTP_303_SEE_OTHER)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/libros/{libro_id}/update", response_model=schemas.Libro)
def update_libro(
    libro_id: int,
    titulo: str = Form(...),
    autor_id: int = Form(...),
    editorial_id: int = Form(None),
    isbn: int = Form(None),
    anio_publicacion: int = Form(None),
    edicion: str = Form(None),
    categoria_id: int = Form(None),
    cantidad_ejemplares: int = Form(1),
    ejemplares_disponibles: int = Form(1),
    resumen: str = Form(None),
    portada: bytes = Form(None),
    ubicacion_id: int = Form(None),
    db: Session = Depends(get_db)
):
    """Actualiza un libro existente."""
    libro_data = {
        "titulo": titulo,
        "autor_id": autor_id,
        "editorial_id": editorial_id,
        "isbn": isbn,
        "anio_publicacion": anio_publicacion,
        "edicion": edicion,
        "categoria_id": categoria_id,
        "cantidad_ejemplares": cantidad_ejemplares,
        "ejemplares_disponibles": ejemplares_disponibles,
        "resumen": resumen,
        "portada": portada,
        "ubicacion_id": ubicacion_id,
    }
    try:
        libro = crud.update_libro(db=db, libro_id=libro_id, libro=schemas.LibroCreate(**libro_data))
        if not libro:
            raise HTTPException(status_code=404, detail="Libro no encontrado")
        return RedirectResponse(url="/libros", status_code=HTTP_303_SEE_OTHER)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/libros/", response_model=List[schemas.Libro])
def read_libros(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Obtiene una lista de libros."""
    libros = crud.get_libros(db, skip=skip, limit=limit)
    return libros


@router.get("/libros/{libro_id}", response_model=schemas.Libro)
def read_libro(libro_id: int, db: Session = Depends(get_db)):
    """Obtiene un libro por su ID."""
    db_libro = crud.get_libro(db, libro_id=libro_id)
    if db_libro is None:
        raise HTTPException(status_code=404, detail="Libro no encontrado")
    return db_libro


@router.delete("/libros/{libro_id}", response_model=bool)
def delete_libro(libro_id: int, db: Session = Depends(get_db)):
    """Elimina un libro."""
    if not crud.delete_libro(db, libro_id=libro_id):
        raise HTTPException(status_code=404, detail="Libro no encontrado")
    return True