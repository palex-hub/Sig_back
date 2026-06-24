from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.modules.rutas.schemas.grafo import GrafoResponse
from app.modules.rutas.services.grafo_service import obtener_grafo

router = APIRouter()


@router.get("", response_model=GrafoResponse)
def get_grafo(db: Session = Depends(get_db)):
    return obtener_grafo(db)
