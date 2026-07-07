from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from .schemas import (
    RegistroMicroRequest,
    RegistroMicroResponse,
    UbicacionRequest,
    UbicacionResponse,
    MicroActivoResponse,
)
from . import service

router = APIRouter()


@router.post(
    "/registrar",
    response_model=RegistroMicroResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Registrar o re-registrar un micrero",
)
def registrar_micro(body: RegistroMicroRequest, db: Session = Depends(get_db)):
    """
    El micrero envía su nombre y la linea_ruta_id que va a operar.
    Retorna un micro_id que deberá usar para enviar su ubicación.
    Si el mismo nombre + linea_ruta_id ya estaba registrado, se renueva.
    """
    try:
        return service.registrar_micro(body.nombre, body.linea_ruta_id, db)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.post(
    "/{micro_id}/ubicacion",
    response_model=UbicacionResponse,
    summary="Actualizar ubicación del micro (llamar cada ~3 s)",
)
def actualizar_ubicacion(micro_id: int, body: UbicacionRequest):
    """
    El micrero envía su posición GPS actual.
    Si el micro_id no está en memoria (reinicio del servidor) retorna 404
    para que el cliente vuelva a registrarse.
    """
    try:
        micro = service.actualizar_ubicacion(micro_id, body.lat, body.lng)
        return UbicacionResponse(micro_id=micro.micro_id, lat=micro.lat, lng=micro.lng)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.get(
    "/activos",
    response_model=list[MicroActivoResponse],
    summary="Listar todos los micros activos",
)
def listar_activos():
    """Devuelve todos los buses que enviaron ubicación en los últimos 30 s."""
    return service.listar_activos()


@router.get(
    "/activos/{linea_ruta_id}",
    response_model=list[MicroActivoResponse],
    summary="Listar micros activos de una línea-ruta específica",
)
def activos_por_linea(linea_ruta_id: int):
    """Devuelve solo los buses de la linea_ruta_id indicada."""
    return service.listar_activos_por_linea(linea_ruta_id)


@router.delete(
    "/{micro_id}/desactivar",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="El micrero sale de servicio",
)
def desactivar_micro(micro_id: int):
    """El micrero presiona 'Finalizar servicio'. Se elimina del store."""
    service.desactivar(micro_id)
