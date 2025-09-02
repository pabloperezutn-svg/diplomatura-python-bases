from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from app.api.libros import router as libros_router
from app.api.autores import router as autores_router
from app.api.prestamos import router as prestamos_router
from app.api.usuarios import router as usuarios_router
from app.api.wikipedia import router as wikipedia_router
from app.frontend.autores import router as frontend_autores_router
from app.frontend.prestamos import router as frontend_prestamos_router
from app.frontend.usuarios import router as frontend_usuarios_router
app = FastAPI(title="Open Biblioteca API", version="1.0.1")

# Montar archivos estáticos
app.mount("/static", StaticFiles(directory="static"), name="static")

# Incluir routers
app.include_router(autores_router, prefix="/api")
app.include_router(wikipedia_router, prefix="/api")
app.include_router(libros_router, prefix="/api")
app.include_router(prestamos_router, prefix="/api")
app.include_router(usuarios_router, prefix="/api")
app.include_router(frontend_autores_router)
app.include_router(frontend_prestamos_router)
app.include_router(frontend_usuarios_router)
app.include_router(frontend_usuarios_router)