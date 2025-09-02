from fastapi import APIRouter, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
import httpx
from datetime import date
from starlette.status import HTTP_303_SEE_OTHER

router = APIRouter(tags=["Frontend Prestamos"])
templates = Jinja2Templates(directory="templates")

API_BASE_URL = "http://127.0.0.1:8000/prestamos"  #  Url

@router.get("/prestamos", response_class=HTMLResponse)
async def list_prestamos(request: Request):
    """Shows all prestamos."""
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{API_BASE_URL}/prestamos/")
        prestamos = response.json()
    return templates.TemplateResponse("prestamos/list.html", {"request": request, "prestamos": prestamos})


@router.get("/prestamos/create", response_class=HTMLResponse)
async def show_create_form(request: Request):
    """Shows the create form to add a new prestamo."""
    return templates.TemplateResponse("prestamos/create.html", {"request": request})


@router.post("/prestamos/create", response_class=HTMLResponse)
async def create_prestamo(request: Request,
                           libro_id: int = Form(...),
                           usuario_id: int = Form(...),
                           fecha_devolucion_esperada: date = Form(...),
                           fecha_devolucion_real: date = Form(None),
                           estado: str = Form("activo"),
                           multa: float = Form(0.0),
                           notas: str = Form(None)):
    """Adds a new prestamo and redirects to the list."""

    prestamo_data = {
        "libro_id": libro_id,
        "usuario_id": usuario_id,
        "fecha_devolucion_esperada": fecha_devolucion_esperada,
        "fecha_devolucion_real": fecha_devolucion_real,
        "estado": estado,
        "multa": multa,
        "notas": notas,
    }

    async with httpx.AsyncClient() as client:
        response = await client.post(f"{API_BASE_URL}/prestamos/", json=prestamo_data)
        if response.status_code != 200:
            return templates.TemplateResponse("prestamos/create.html",
                                              {"request": request, "error": "Failed to create prestamo"})

    return RedirectResponse("/prestamos", status_code=HTTP_303_SEE_OTHER)