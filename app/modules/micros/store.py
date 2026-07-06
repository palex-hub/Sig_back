"""
Almacén en memoria de micros activos.

Se usa un dict simple (thread-safe para lectura en asyncio) en lugar de Redis
para mantener la complejidad baja. Cada micro tiene un TTL de 30 segundos:
si no envía ubicación en ese tiempo se considera inactivo.
"""

import time
from dataclasses import dataclass, field


@dataclass
class MicroActivo:
    micro_id: int
    nombre: str          # nombre del micrero
    linea_ruta_id: int
    linea_nombre: str
    lat: float
    lng: float
    ultima_actualizacion: float = field(default_factory=time.time)


# micro_id -> MicroActivo
_store: dict[int, MicroActivo] = {}

# Tiempo máximo sin actualizar para considerar inactivo (segundos)
TTL_SEGUNDOS = 30


def registrar_o_actualizar_micro(
    micro_id: int,
    nombre: str,
    linea_ruta_id: int,
    linea_nombre: str,
    lat: float,
    lng: float,
) -> MicroActivo:
    micro = MicroActivo(
        micro_id=micro_id,
        nombre=nombre,
        linea_ruta_id=linea_ruta_id,
        linea_nombre=linea_nombre,
        lat=lat,
        lng=lng,
        ultima_actualizacion=time.time(),
    )
    _store[micro_id] = micro
    return micro


def actualizar_ubicacion(micro_id: int, lat: float, lng: float) -> MicroActivo | None:
    micro = _store.get(micro_id)
    if micro is None:
        return None
    micro.lat = lat
    micro.lng = lng
    micro.ultima_actualizacion = time.time()
    return micro


def get_micros_activos() -> list[MicroActivo]:
    ahora = time.time()
    return [m for m in _store.values() if (ahora - m.ultima_actualizacion) <= TTL_SEGUNDOS]


def get_micros_activos_por_linea(linea_ruta_id: int) -> list[MicroActivo]:
    return [m for m in get_micros_activos() if m.linea_ruta_id == linea_ruta_id]


def desactivar_micro(micro_id: int) -> bool:
    return _store.pop(micro_id, None) is not None
