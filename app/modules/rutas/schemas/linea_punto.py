from pydantic import BaseModel


class PuntoRecorrido(BaseModel):
    punto_destino: int
    orden: int
    lat: float
    lng: float


