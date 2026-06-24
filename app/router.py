from fastapi import APIRouter

from app.modules.rutas.routers.grafos import router as grafos_router
from app.modules.rutas.routers.lineas import router as lineas_router

api_router = APIRouter()
api_router.include_router(grafos_router, prefix="/grafo", tags=["Grafo"])
api_router.include_router(lineas_router, prefix="/lineas", tags=["Líneas"])
