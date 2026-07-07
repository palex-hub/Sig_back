from pydantic import BaseModel, Field


# ── Request schemas ────────────────────────────────────────────────────────────

class RegistroMicroRequest(BaseModel):
    nombre: str = Field(..., min_length=2, max_length=80, description="Nombre del micrero")
    linea_ruta_id: int = Field(..., gt=0, description="ID de la linea-ruta que opera")


class UbicacionRequest(BaseModel):
    lat: float = Field(..., ge=-90, le=90)
    lng: float = Field(..., ge=-180, le=180)


# ── Response schemas ───────────────────────────────────────────────────────────

class RegistroMicroResponse(BaseModel):
    micro_id: int
    nombre: str
    linea_ruta_id: int
    linea_nombre: str
    mensaje: str = "Micro registrado correctamente"


class UbicacionResponse(BaseModel):
    micro_id: int
    lat: float
    lng: float
    ok: bool = True


class MicroActivoResponse(BaseModel):
    micro_id: int
    nombre: str
    linea_ruta_id: int
    linea_nombre: str
    lat: float
    lng: float
    ultima_actualizacion: float  # epoch seconds
