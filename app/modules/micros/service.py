"""
Lógica de negocio para el módulo de micros.
Valida que la linea_ruta_id exista en la base de datos antes de registrar.
"""

import hashlib
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import select

from app.modules.rutas.models.linea_ruta import LineaRuta
from app.modules.rutas.models.linea import Linea
from . import store
from .schemas import RegistroMicroResponse, MicroActivoResponse


def _generar_micro_id(nombre: str, linea_ruta_id: int) -> int:
    """
    Genera un ID determinístico basado en nombre + linea_ruta_id.
    Así el mismo micrero siempre obtiene el mismo ID sin base de datos.
    """
    raw = f"{nombre.strip().lower()}:{linea_ruta_id}"
    return int(hashlib.sha256(raw.encode()).hexdigest()[:8], 16) % 1_000_000


def registrar_micro(
    nombre: str,
    linea_ruta_id: int,
    db: Session,
) -> RegistroMicroResponse:
    # Verificar que la linea_ruta existe
    result = db.execute(
        select(LineaRuta)
        .options(joinedload(LineaRuta.linea))
        .where(LineaRuta.id == linea_ruta_id)
    )
    lr = result.scalar_one_or_none()
    if lr is None:
        raise ValueError(f"linea_ruta_id {linea_ruta_id} no existe")

    linea_nombre = lr.linea.nombre.strip() if lr.linea else f"Línea {lr.linea_id}"

    micro_id = _generar_micro_id(nombre, linea_ruta_id)
    store.registrar_o_actualizar_micro(
        micro_id=micro_id,
        nombre=nombre.strip(),
        linea_ruta_id=linea_ruta_id,
        linea_nombre=linea_nombre,
        lat=0.0,
        lng=0.0,
    )

    return RegistroMicroResponse(
        micro_id=micro_id,
        nombre=nombre.strip(),
        linea_ruta_id=linea_ruta_id,
        linea_nombre=linea_nombre,
    )


def actualizar_ubicacion(micro_id: int, lat: float, lng: float):
    micro = store.actualizar_ubicacion(micro_id, lat, lng)
    if micro is None:
        raise ValueError(f"micro_id {micro_id} no está registrado o expiró")
    return micro


def listar_activos() -> list[MicroActivoResponse]:
    return [
        MicroActivoResponse(
            micro_id=m.micro_id,
            nombre=m.nombre,
            linea_ruta_id=m.linea_ruta_id,
            linea_nombre=m.linea_nombre,
            lat=m.lat,
            lng=m.lng,
            ultima_actualizacion=m.ultima_actualizacion,
        )
        for m in store.get_micros_activos()
    ]


def listar_activos_por_linea(linea_ruta_id: int) -> list[MicroActivoResponse]:
    return [
        MicroActivoResponse(
            micro_id=m.micro_id,
            nombre=m.nombre,
            linea_ruta_id=m.linea_ruta_id,
            linea_nombre=m.linea_nombre,
            lat=m.lat,
            lng=m.lng,
            ultima_actualizacion=m.ultima_actualizacion,
        )
        for m in store.get_micros_activos_por_linea(linea_ruta_id)
    ]


def desactivar(micro_id: int) -> bool:
    return store.desactivar_micro(micro_id)
