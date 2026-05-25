from pydantic import BaseModel, ConfigDict

from app.modules.rutas.schemas.color import ColorResponse
from app.modules.rutas.schemas.ruta import RutaConPuntos


class LineaListResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    nombre: str
    imagen_url: str | None
    color: ColorResponse


class LineaDetalleResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    nombre: str
    imagen_url: str | None
    color: ColorResponse
    rutas: list[RutaConPuntos]
