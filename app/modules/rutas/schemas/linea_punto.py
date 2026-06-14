from pydantic import BaseModel


class PuntoRecorrido(BaseModel):
    punto_destino: int | None = None
    orden: int
    lat: float
    lng: float


