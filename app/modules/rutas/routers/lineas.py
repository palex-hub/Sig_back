from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import SessionLocal
from app.modules.rutas.schemas.linea import LineaDetalleResponse, LineaListResponse
from app.modules.rutas.services.linea_service import (
    get_all_lineas,
    get_linea_detalle,
    get_mapa_lineas,
)

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("", response_model=list[LineaListResponse])
def listar_lineas(db: Session = Depends(get_db)):
    return get_all_lineas(db)


@router.get("/{linea_id}", response_model=LineaDetalleResponse)
def obtener_linea(linea_id: int, db: Session = Depends(get_db)):
    linea = get_linea_detalle(linea_id, db)
    if not linea:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Línea no encontrada")
    return linea


@router.get("/mapa/todo", response_model=list[LineaDetalleResponse])
def mapa_todas_lineas(db: Session = Depends(get_db)):
    return get_mapa_lineas(db)
