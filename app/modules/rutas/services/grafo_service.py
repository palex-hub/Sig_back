from sqlalchemy import text
from sqlalchemy.orm import Session

from app.modules.rutas.schemas.grafo import (
    GrafoResponse,
    LineaGrafo,
    LineaRutaGrafo,
    PuntoGrafo,
    SegmentoGrafo,
    TrasbordoGrafo,
)


def obtener_grafo(db: Session) -> GrafoResponse:
    puntos = db.execute(
        text("SELECT id, latitud, longitud, stop, descripcion FROM puntos ORDER BY id")
    ).all()

    segmentos = db.execute(
        text("""
            SELECT lp.punto_id, lp.punto_destino_id, lp.linea_ruta_id,
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
        segmentos=[
            SegmentoGrafo(
                punto_id=s.punto_id,
                punto_destino_id=s.punto_destino_id,
                linea_ruta_id=s.linea_ruta_id,
                orden=s.orden,
                tiempo=float(s.tiempo),
                distancia=float(s.distancia),
            )
            for s in segmentos
        ],
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
