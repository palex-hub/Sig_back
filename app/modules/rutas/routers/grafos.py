from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.modules.rutas.schemas.grafo import GrafoResponse
from app.modules.rutas.services.grafo_service import obtener_grafo

router = APIRouter()


@router.get("", response_model=GrafoResponse)
def get_grafo(
    db: Session = Depends(get_db),
    ml: bool = Query(False, description="Incluir predicción ML de tiempos"),
    hora: int = Query(12, ge=0, le=23, description="Hora actual (0-23)"),
    dia_semana: int = Query(0, ge=0, le=6, description="Día de la semana (0=lunes, 6=domingo)"),
):
    return obtener_grafo(db, usar_ml=ml, hora=hora, dia_semana=dia_semana)
