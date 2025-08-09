from fastapi import APIRouter, HTTPException
import requests
from app.core.autores import db
from fastapi.responses import RedirectResponse
from starlette.status import HTTP_303_SEE_OTHER
from fastapi import Form
from datetime import datetime

router = APIRouter(tags=["Wikipedia Integration"])

@router.post("/autores/bio/{autor_id}")
def actualizar_biografia(    
    autor_id: int, 
    nombre: str = Form(...),
    apellido: str = Form(...),
    fecha_nacimiento: datetime = Form(...),
    nacionalidad_id: int = Form(...)
    ):
    autor = db.get_por_id(autor_id)
    if not autor:
        raise HTTPException(status_code=404, detail="Autor no encontrado")
    
    nombre_completo = f"{autor.nombre} {autor.apellido}"
    url = f"https://es.wikipedia.org/api/rest_v1/page/summary/{nombre_completo.replace(' ', '_')}"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        if 'extract' in data:
            datos = {
                'nombre': nombre,
                'apellido': apellido,
                'fecha_nacimiento': fecha_nacimiento,
                'nacionalidad_id': nacionalidad_id,
                'biografia': data['extract']
            }
            db.actualizar(autor_id, datos)
            return RedirectResponse(url="/autores", status_code=HTTP_303_SEE_OTHER)
        raise HTTPException(status_code=404, detail="No se encontró biografía")
    raise HTTPException(status_code=response.status_code, detail="Error al consultar Wikipedia")