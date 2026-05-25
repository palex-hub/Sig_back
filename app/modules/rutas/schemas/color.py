from pydantic import BaseModel, ConfigDict


class ColorResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    nombre: str
    cod_hex: str
