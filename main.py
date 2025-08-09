from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from app.api.autores import router as autores_router
from app.api.wikipedia import router as wikipedia_router

from app.frontend.autores import router as frontend_autores_router


app = FastAPI(title="Open Biblioteca API", version="1.0.0")

# Montar archivos estáticos
app.mount("/static", StaticFiles(directory="static"), name="static")

# Incluir routers
app.include_router(autores_router, prefix="/api")
app.include_router(wikipedia_router, prefix="/api")

app.include_router(frontend_autores_router)
