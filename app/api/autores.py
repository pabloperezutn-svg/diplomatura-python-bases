from fastapi import APIRouter, HTTPException
from app.schemas.autores import Autor
from app.core.autores import db
from fastapi import Form
from fastapi.responses import RedirectResponse
from starlette.status import HTTP_303_SEE_OTHER
from datetime import datetime

router = APIRouter(tags=["Autores API"])

@router.get("/autores/", response_model=list[Autor])
def listar_autores():
    return db.get_todos()

@router.get("/autores/{autor_id}", response_model=Autor)
def obtener_autor(autor_id: int):
    autor = db.get_por_id(autor_id)
    if not autor:
        raise HTTPException(status_code=404, detail="Autor no encontrado")
    return autor

@router.post("/autores/", response_model=Autor)
def crear_autor(     
    nombre : str = Form(...),
    apellido : str = Form(...),
    fecha_nacimiento : datetime = Form(...),
    nacionalidad_id : int = Form(...),
    biografia : str = Form(...)
    ):
    autor = {
        "nombre": nombre,
        "apellido": apellido,
        "fecha_nacimiento": fecha_nacimiento,
        "nacionalidad_id": nacionalidad_id,
        "biografia": biografia
    }
    try:
        autor = db.crear(autor)
        return RedirectResponse(url="/autores", status_code=HTTP_303_SEE_OTHER)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/autores/{autor_id}/update", response_model=Autor)
def actualizar_autor(
    autor_id: int, 
    nombre: str = Form(...),
    apellido: str = Form(...),
    fecha_nacimiento: datetime = Form(...),
    nacionalidad_id: int = Form(...),
    biografia: str = Form(...)
):
    datos = {
        "autor_id":autor_id,
        "nombre":nombre,
        "apellido":apellido,
        "fecha_nacimiento":fecha_nacimiento,
        "nacionalidad_id":nacionalidad_id,
        "biografia":biografia
    }
    autor = db.actualizar(autor_id, datos)
    if not autor:
        raise HTTPException(status_code=404, detail="Autor no encontrado")
    return RedirectResponse(url="/autores", status_code=HTTP_303_SEE_OTHER)

@router.post("/autores/{autor_id}/eliminar", response_model=Autor)
def eliminar_autor(autor_id: int):
    autor = db.eliminar(autor_id)
    if not autor:
        raise HTTPException(status_code=404, detail="Autor no encontrado")
    return RedirectResponse(url="/autores", status_code=HTTP_303_SEE_OTHER) 