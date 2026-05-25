from pydantic import BaseModel, ConfigDict


class PuntoResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    latitud: float
    longitud: float
    descripcion: str | None
