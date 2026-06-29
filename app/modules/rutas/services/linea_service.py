from sqlalchemy import select
from sqlalchemy.orm import Session, joinedload

from app.modules.rutas.models import Color, Linea, LineaRuta, LineaPunto
from app.modules.rutas.schemas.color import ColorResponse
from app.modules.rutas.schemas.linea import LineaDetalleResponse, LineaListResponse
from app.modules.rutas.schemas.linea_punto import PuntoRecorrido
from app.modules.rutas.schemas.ruta import RutaConPuntos


def get_all_lineas(db: Session) -> list[LineaListResponse]:
    result = db.execute(
        select(Linea).options(joinedload(Linea.color)).order_by(Linea.id)
    )
    lineas = result.unique().scalars().all()

    return [
        LineaListResponse(
            id=l.id,
            nombre=l.nombre.strip(),
            imagen_url=l.imagen_url,
            color=ColorResponse(id=l.color.id, nombre=l.color.nombre, cod_hex=l.color.cod_hex),
        )
        for l in lineas
    ]


def get_linea_detalle(linea_id: int, db: Session) -> LineaDetalleResponse | None:
    result = db.execute(
        select(Linea)
        .options(joinedload(Linea.color))
        .where(Linea.id == linea_id)
    )
    linea = result.unique().scalar_one_or_none()
    if not linea:
        return None

    result_rutas = db.execute(
        select(LineaRuta)
        .options(joinedload(LineaRuta.ruta))
        .where(LineaRuta.linea_id == linea_id)
    )
    lineas_rutas = result_rutas.unique().scalars().all()

    rutas_con_puntos: list[RutaConPuntos] = []
    for lr in lineas_rutas:
        result_puntos = db.execute(
            select(LineaPunto)
            .options(joinedload(LineaPunto.punto))
            .where(LineaPunto.linea_ruta_id == lr.id)
            .order_by(LineaPunto.orden)
        )
        puntos_db = result_puntos.unique().scalars().all()

        puntos = [
            PuntoRecorrido(
                punto_destino=p.punto_destino_id,
                orden=p.orden,
                stop=p.punto.stop,
                lat=p.punto.latitud,
                lng=p.punto.longitud,
            )
            for p in puntos_db
        ]

        tipo = "ida" if lr.ruta_id == 1 else "vuelta"

        rutas_con_puntos.append(
            RutaConPuntos(
                id=lr.id,
                tipo=tipo,
                descripcion=lr.ruta.descripcion if lr.ruta else ("Salida" if tipo == "ida" else "Retorno"),
                distancia_km=lr.distancia,
                tiempo_min=lr.tiempo,
                puntos=puntos,
            )
        )

    return LineaDetalleResponse(
        id=linea.id,
        nombre=linea.nombre.strip(),
        imagen_url=linea.imagen_url,
        color=ColorResponse(id=linea.color.id, nombre=linea.color.nombre, cod_hex=linea.color.cod_hex),
        rutas=rutas_con_puntos,
    )


def get_mapa_lineas(db: Session) -> list[LineaDetalleResponse]:
    result = db.execute(
        select(Linea).options(joinedload(Linea.color)).order_by(Linea.id)
    )
    lineas = result.unique().scalars().all()

    resultado = []
    for linea in lineas:
        detalle = get_linea_detalle(linea.id, db)
        if detalle:
            resultado.append(detalle)

    return resultado
