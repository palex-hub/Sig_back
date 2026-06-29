from pydantic import BaseModel


class PuntoRecorrido(BaseModel):
    punto_destino: int | None = None
    orden: int
    stop: bool
    lat: float
    lng: float


