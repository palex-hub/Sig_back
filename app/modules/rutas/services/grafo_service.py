import json
import time
import warnings
from pathlib import Path
from urllib.request import urlopen

import joblib
import numpy as np
from sqlalchemy import text
from sqlalchemy.orm import Session

warnings.filterwarnings("ignore", message="X does not have valid feature names")

from app.modules.rutas.schemas.grafo import (
    GrafoResponse,
    LineaGrafo,
    LineaRutaGrafo,
    PuntoGrafo,
    SegmentoGrafo,
    TrasbordoGrafo,
)

_MODELO = None
_FEATURES = [
    "segmento_id", "hora", "dia_semana", "es_fin_semana",
    "es_hora_pico", "distancia_km", "clima",
]

_CLIMA_CACHE = {"categoria": None, "timestamp": 0}
_SCZ_LAT = -17.78
_SCZ_LON = -63.18

_ruta_modelo = Path(__file__).resolve().parent.parent.parent.parent.parent / "modelo.pkl"
if _ruta_modelo.exists():
    _MODELO = joblib.load(_ruta_modelo)

_WMO_MAP = {
    0: 0,
    1: 1, 2: 1, 3: 1,
    51: 2, 53: 2, 55: 2, 56: 2, 57: 2,
    61: 2, 63: 2, 65: 2, 66: 2, 67: 2,
    80: 2, 81: 2, 82: 2,
    95: 3, 96: 3, 99: 3,
}


def _obtener_clima() -> int:
    now = time.time()
    if now - _CLIMA_CACHE["timestamp"] < 1800:
        return _CLIMA_CACHE["categoria"]

    try:
        url = (
            f"https://api.open-meteo.com/v1/forecast"
            f"?latitude={_SCZ_LAT}&longitude={_SCZ_LON}&current=weather_code"
        )
        with urlopen(url, timeout=5) as resp:
            data = json.loads(resp.read().decode())
        code = data["current"]["weather_code"]
        cat = _WMO_MAP.get(code, 0)
        _CLIMA_CACHE["categoria"] = cat
        _CLIMA_CACHE["timestamp"] = now
        return cat
    except Exception:
        return 0


def obtener_grafo(
    db: Session,
    usar_ml: bool = False,
    hora: int = 12,
    dia_semana: int = 0,
) -> GrafoResponse:
    puntos = db.execute(
        text("SELECT id, latitud, longitud, stop, descripcion FROM puntos ORDER BY id")
    ).all()

    segmentos = db.execute(
        text("""
            SELECT lp.id, lp.punto_id, lp.punto_destino_id, lp.linea_ruta_id,
                   lp.orden, lp.tiempo, lp.distancia
            FROM lineas_puntos lp
            WHERE lp.punto_destino_id IS NOT NULL
            ORDER BY lp.linea_ruta_id, lp.orden
        """)
    ).all()

    trasbordos = db.execute(
        text("""
            SELECT t.punto_id, t.linea_origen_id, t.linea_destino_id, t.penalizacion_min
            FROM trasbordos t
            ORDER BY t.id
        """)
    ).all()

    lineas = db.execute(
        text("""
            SELECT l.id, l.nombre, c.cod_hex
            FROM lineas l
            JOIN colores c ON c.id = l.color_id
            ORDER BY l.id
        """)
    ).all()

    lineas_rutas = db.execute(
        text("""
            SELECT lr.id, lr.linea_id, lr.ruta_id
            FROM lineas_rutas lr
            ORDER BY lr.id
        """)
    ).all()

    es_fin_semana = 1 if dia_semana >= 5 else 0
    es_hora_pico = 1 if (7 <= hora <= 9 or 12 <= hora <= 14 or 18 <= hora <= 20) else 0
    clima = _obtener_clima()

    seg_result = [
        SegmentoGrafo(
            punto_id=s.punto_id,
            punto_destino_id=s.punto_destino_id,
            linea_ruta_id=s.linea_ruta_id,
            orden=s.orden,
            tiempo=float(s.tiempo),
            distancia=float(s.distancia),
        )
        for s in segmentos
    ]

    if usar_ml and _MODELO is not None:
        features = np.array([
            [s.id, hora, dia_semana, es_fin_semana, es_hora_pico,
             float(s.distancia), clima]
            for s in segmentos
        ])
        preds = _MODELO.predict(features)
        for seg, p in zip(seg_result, preds):
            seg.tiempo_ml = round(float(p), 6)

    return GrafoResponse(
        puntos=[
            PuntoGrafo(
                id=p.id,
                lat=float(p.latitud),
                lng=float(p.longitud),
                stop=bool(p.stop),
                descripcion=p.descripcion,
            )
            for p in puntos
        ],
        segmentos=seg_result,
        trasbordos=[
            TrasbordoGrafo(
                punto_id=t.punto_id,
                linea_origen_id=t.linea_origen_id,
                linea_destino_id=t.linea_destino_id,
                penalizacion_min=float(t.penalizacion_min),
            )
            for t in trasbordos
        ],
        lineas=[
            LineaGrafo(
                id=l.id,
                nombre=l.nombre.strip(),
                cod_hex=l.cod_hex,
            )
            for l in lineas
        ],
        lineas_rutas=[
            LineaRutaGrafo(
                id=lr.id,
                linea_id=lr.linea_id,
                ruta_id=lr.ruta_id,
                tipo="ida" if lr.ruta_id == 1 else "vuelta",
            )
            for lr in lineas_rutas
        ],
    )

