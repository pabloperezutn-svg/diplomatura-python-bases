from fastapi import APIRouter, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
import httpx
from datetime import date
from starlette.status import HTTP_303_SEE_OTHER

router = APIRouter(tags=["Frontend Usuarios"])
templates = Jinja2Templates(directory="templates")

API_BASE_URL = "http://127.0.0.1:8000/usuarios"  # url

@router.get("/usuarios", response_class=HTMLResponse)
async def list_usuarios(request: Request):
    """Shows all usuarios."""
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{API_BASE_URL}/usuarios/")
        usuarios = response.json()
    return templates.TemplateResponse("usuarios/list.html", {"request": request, "usuarios": usuarios})


@router.get("/usuarios/create", response_class=HTMLResponse)
async def show_create_form(request: Request):
    """Shows the create form to add a new usuario."""
    return templates.TemplateResponse("usuarios/create.html", {"request": request})


@router.post("/usuarios/create", response_class=HTMLResponse)
async def create_usuario(request: Request,
                           dni: str = Form(...),
                           nombre: str = Form(...),
                           apellido: str = Form(...),
                           direccion: str = Form(None),
                           telefono: str = Form(None),
                           email: str = Form(...),
                           fecha_nacimiento: date = Form(None),
                           rol_id: int = Form(None),
                           estado_id: int = Form(None)):
    """Adds a new usuario and redirects to the list."""

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
            return templates.TemplateResponse("usuarios/create.html",
                                              {"request": request, "error": "Failed to create usuario"})

    return RedirectResponse("/usuarios", status_code=HTTP_303_SEE_OTHER)