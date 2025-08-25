from fastapi import APIRouter, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
import httpx
from datetime import date

# Configuración de Jinja2
templates = Jinja2Templates(directory="app/templates")

# Router para los endpoints de usuarios
router = APIRouter()

# URL base de la API backend
API_BASE_URL = "http://127.0.0.1:8000/usurios"  # Ajusta esto según tu configuración


@router.get("/usuarios/create", response_class=HTMLResponse)
async def create_usuario_form(request: Request):
    """Muestra el formulario de creación de usuarios."""
    return templates.TemplateResponse("usuarios/create.html", {"request": request})


@router.post("/usuarios/create", response_class=HTMLResponse)
async def create_usuario(request: Request,
                           dni: str = Form(...),
                           nombre: str = Form(...),
                           apellido: str = Form(...),
                           direccion: str = Form(None),
                           telefono: str = Form(None),
                           email: str = Form(...),
                           fecha_nacimiento: str = Form(None),
                           rol_id: int = Form(None),
                           estado_id: int = Form(None)):
    """Crea un nuevo usuario y redirige a la lista de usuarios."""

    usuario_data = {
        "dni": dni,
        "nombre": nombre,
        "apellido": apellido,
        "direccion": direccion,
        "telefono": telefono,
        "email": email,
        "fecha_nacimiento": fecha_nacimiento,
        "rol_id": rol_id,
        "estado_id": estado_id,
    }

    async with httpx.AsyncClient() as client:
        response = await client.post(f"{API_BASE_URL}/usuarios/", json=usuario_data)
        if response.status_code != 200:
            # Manejar el error (mostrar un mensaje al usuario, etc.)
            return templates.TemplateResponse("usuarios/create.html",
                                              {"request": request, "error": "Error al crear el usuario"})

    return RedirectResponse("/usuarios", status_code=303)  # Redirige con código 303 (ver otros)