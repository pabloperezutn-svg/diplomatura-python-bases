from typing import List
from fastapi import Depends, Request, APIRouter, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from sqlalchemy.orm import Session
from fastapi.templating import Jinja2Templates
from starlette.status import HTTP_303_SEE_OTHER

from app.core import libros as crud
from app.schemas import libros as schemas
from app.core.database import get_db
from app.core import libros as crud

router = APIRouter(tags=["Frontend Libros"])
templates = Jinja2Templates(directory="templates")

API_BASE_URL = "http://127.0.0.1:8000/libros"  # URL

@router.get("/libros", response_class=HTMLResponse)
async def list_libros(request: Request, db: Session = Depends(get_db)):
    """Shows all libros."""
    libros = crud.get_libros(db)
    return templates.TemplateResponse("libros/list.html", {"request": request, "libros": libros})


@router.get("/libros/create", response_class=HTMLResponse)
async def show_create_form(request: Request):
    """Shows the form to create a new libro."""
    return templates.TemplateResponse("libros/create.html", {"request": request})


@router.post("/libros/create", response_class=HTMLResponse)
async def create_libro(request: Request,
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
    """Adds a new libro and redirects to the list."""
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
        crud.create_libro(db, libro=schemas.LibroCreate(**libro_data))
        return RedirectResponse("/libros", status_code=HTTP_303_SEE_OTHER)
    except Exception as e:
        return templates.TemplateResponse("libros/create.html", {"request": request, "error": f"Failed to create libro: {e}"})