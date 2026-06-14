from pydantic import BaseModel, ConfigDict


class LineaRutaResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    linea_id: int
    ruta_id: int
    descripcion: str | None
    distancia: float
    tiempo: float
