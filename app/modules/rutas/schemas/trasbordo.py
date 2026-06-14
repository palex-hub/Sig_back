from pydantic import BaseModel, ConfigDict


class TrasbordoResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    punto_id: int
    linea_origen_id: int
    linea_destino_id: int
    penalizacion_min: float
