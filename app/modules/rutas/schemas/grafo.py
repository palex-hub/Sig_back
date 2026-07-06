from pydantic import BaseModel


class PuntoGrafo(BaseModel):
    id: int
    lat: float
    lng: float
    stop: bool
    descripcion: str | None


class SegmentoGrafo(BaseModel):
    punto_id: int
    punto_destino_id: int
    linea_ruta_id: int
    orden: int
    tiempo: float
    tiempo_ml: float | None = None
    distancia: float


class TrasbordoGrafo(BaseModel):
    punto_id: int
    linea_origen_id: int
    linea_destino_id: int
    penalizacion_min: float


class LineaGrafo(BaseModel):
    id: int
    nombre: str
    cod_hex: str


class LineaRutaGrafo(BaseModel):
    id: int
    linea_id: int
    ruta_id: int
    tipo: str


class GrafoResponse(BaseModel):
    puntos: list[PuntoGrafo]
    segmentos: list[SegmentoGrafo]
    trasbordos: list[TrasbordoGrafo]
    lineas: list[LineaGrafo]
    lineas_rutas: list[LineaRutaGrafo]
