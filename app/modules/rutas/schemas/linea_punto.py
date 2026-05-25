from pydantic import BaseModel


class PuntoRecorrido(BaseModel):
    orden: int
    lat: float
    lng: float
