from fastapi import APIRouter, Request, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from app.core.autores import db
from app.core.nacionalidades import db as db_nacionalidades
from app.models.nacionalidades import Nacionalidad

router = APIRouter(tags=["Frontend Autores"])
templates = Jinja2Templates(directory="templates")

@router.get("/autores", response_class=HTMLResponse)
async def list_autores(request: Request):
    autores = db.get_todos()
    return templates.TemplateResponse("autores/list.html", {"request": request, "autores": autores})

@router.get("/autores/create", response_class=HTMLResponse)
async def mostrar_formulario_creacion(request: Request):
    nacionalidades = db_nacionalidades.get_todos(order_by=Nacionalidad.sdes)
    return templates.TemplateResponse("autores/create.html", {
        "request": request,
        "nacionalidades": nacionalidades
    })

@router.get("/autores/{autor_id}", response_class=HTMLResponse)
async def detail_autor_html(
    request: Request,
    autor_id: str
):
    try:
        autor_id_int = int(autor_id)
        if autor_id_int <= 0:
            raise ValueError
    except ValueError:
        print(f"[ERROR] ID no es número válido: {autor_id}")
        raise HTTPException(
            status_code=422,
            detail=f"El ID debe ser un número entero positivo. Se recibió: {autor_id}"
        )
    
    autor = db.get_por_id(autor_id_int)
    
    if not autor:
        raise HTTPException(
            status_code=404,
            detail=f"Autor con ID {autor_id_int} no encontrado"
        )
    
    nacionalidades = db_nacionalidades.get_todos(order_by=Nacionalidad.sdes)

    return templates.TemplateResponse("autores/detail.html", {
        "request": request,
        "autor": autor,  # Pasamos el objeto completo
        "autor_id": autor_id_int,
        "nacionalidades": nacionalidades
    })