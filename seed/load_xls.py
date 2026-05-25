import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import xlrd
from sqlalchemy import select

from app.core.database import SessionLocal, engine
from app.core.database import Base
from app.modules.rutas.models import Color, Linea, LineaPunto, LineaRuta, Punto, Ruta

XLS_PATH = Path(__file__).resolve().parent.parent / "DatosLineas.xls"


def read_xls():
    wb = xlrd.open_workbook(str(XLS_PATH))
    return wb


def recreate_tables():
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
    print("Tablas recreadas correctamente.")


def seed_colores(wb, db):
    sheet = wb.sheet_by_name("Lineas")
    colores_vistos: dict[str, tuple[str, str]] = {}
    for row in range(1, sheet.nrows):
        cod_hex = sheet.cell(row, 2).value.strip()
        if cod_hex not in colores_vistos:
            colores_vistos[cod_hex] = (cod_hex, cod_hex)

    for cod_hex, (nombre, _) in colores_vistos.items():
        color = Color(nombre=nombre, cod_hex=cod_hex)
        db.add(color)
    db.commit()

    result = db.execute(select(Color))
    return {c.cod_hex: c.id for c in result.scalars().all()}


def seed_puntos(wb, db):
    sheet = wb.sheet_by_name("Puntos")
    for row in range(1, sheet.nrows):
        punto = Punto(
            id=int(sheet.cell(row, 0).value),
            latitud=sheet.cell(row, 1).value,
            longitud=sheet.cell(row, 2).value,
            descripcion=sheet.cell(row, 3).value.strip(),
        )
        db.add(punto)
    db.commit()
    print(f"Puntos insertados: {sheet.nrows - 1}")


def seed_rutas(db):
    ruta1 = Ruta(id=1, descripcion="Salida")
    ruta2 = Ruta(id=2, descripcion="Retorno")
    db.add_all([ruta1, ruta2])
    db.commit()
    print("Rutas insertadas: 2")


def seed_lineas(wb, db, color_map):
    sheet = wb.sheet_by_name("Lineas")
    for row in range(1, sheet.nrows):
        cod_hex = sheet.cell(row, 2).value.strip()
        fecha_excel = sheet.cell(row, 4).value
        fecha = xlrd.xldate_as_datetime(fecha_excel, wb.datemode)
        linea = Linea(
            id=int(sheet.cell(row, 0).value),
            nombre=sheet.cell(row, 1).value.strip(),
            imagen_url=sheet.cell(row, 3).value.strip(),
            fecha_creada=fecha,
            color_id=color_map[cod_hex],
        )
        db.add(linea)
    db.commit()
    print(f"Líneas insertadas: {sheet.nrows - 1}")


def seed_lineas_rutas(wb, db):
    sheet = wb.sheet_by_name("LineaRuta")
    for row in range(1, sheet.nrows):
        lr = LineaRuta(
            id=int(sheet.cell(row, 0).value),
            linea_id=int(sheet.cell(row, 1).value),
            ruta_id=int(sheet.cell(row, 2).value),
            distancia=sheet.cell(row, 4).value,
            tiempo=sheet.cell(row, 5).value,
        )
        db.add(lr)
    db.commit()
    print(f"LineaRuta insertadas: {sheet.nrows - 1}")


def seed_lineas_puntos(wb, db):
    sheet = wb.sheet_by_name("LineasPuntos")
    batch = []
    BATCH_SIZE = 200
    total = 0
    for row in range(1, sheet.nrows):
        lp = LineaPunto(
            id=int(sheet.cell(row, 0).value),
            linea_ruta_id=int(sheet.cell(row, 1).value),
            punto_id=int(sheet.cell(row, 2).value),
            orden=int(sheet.cell(row, 3).value),
            latitud=sheet.cell(row, 4).value,
            longitud=sheet.cell(row, 5).value,
            distancia=sheet.cell(row, 6).value,
            tiempo=sheet.cell(row, 7).value,
        )
        batch.append(lp)
        if len(batch) >= BATCH_SIZE:
            db.add_all(batch)
            db.commit()
            total += len(batch)
            batch = []
    if batch:
        db.add_all(batch)
        db.commit()
        total += len(batch)
    print(f"LineasPuntos insertados: {total}")


def main():
    wb = read_xls()
    recreate_tables()

    with SessionLocal() as db:
        color_map = seed_colores(wb, db)
        seed_rutas(db)
        seed_puntos(wb, db)
        seed_lineas(wb, db, color_map)
        seed_lineas_rutas(wb, db)
        seed_lineas_puntos(wb, db)

    print("¡Seed completado exitosamente!")


if __name__ == "__main__":
    main()
