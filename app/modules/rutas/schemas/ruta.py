from pydantic import BaseModel, ConfigDict

from app.modules.rutas.schemas.linea_punto import PuntoRecorrido


class RutaConPuntos(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    tipo: str
    descripcion: str
    distancia_km: float
    tiempo_min: float
    puntos: list[PuntoRecorrido]
