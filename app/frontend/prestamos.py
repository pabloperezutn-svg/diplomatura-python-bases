from fastapi import APIRouter, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
import httpx
from datetime import datetime

# Configuración de Jinja2
templates = Jinja2Templates(directory="app/templates")

# Router para los endpoints de prestamos
router = APIRouter()

# URL base de la API backend
API_BASE_URL = "http://127.0.0.1:8000/prestamos"  # Ajusta esto según tu configuración


@router.get("/prestamos/create", response_class=HTMLResponse)
async def create_prestamo_form(request: Request):
    """Muestra el formulario de creación de préstamos."""
    return templates.TemplateResponse("prestamos/create.html", {"request": request})


@router.post("/prestamos/create", response_class=HTMLResponse)
async def create_prestamo(request: Request,
                           libro_id: int = Form(...),
                           usuario_id: int = Form(...),
                           fecha_devolucion_esperada: str = Form(...),
                           fecha_devolucion_real: str = Form(None),
                           estado: str = Form("activo"),
                           multa: float = Form(0.0),
                           notas: str = Form(None)):
    """Crea un nuevo préstamo y redirige a la lista de préstamos."""

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
            # Manejar el error (mostrar un mensaje al usuario, etc.)
            return templates.TemplateResponse("prestamos/create.html",
                                              {"request": request, "error": "Error al crear el préstamo"})

    return RedirectResponse("/prestamos", status_code=303)  # Redirige con código 303 (ver otros)