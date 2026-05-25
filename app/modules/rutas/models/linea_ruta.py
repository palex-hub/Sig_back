from sqlalchemy import Float, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class LineaRuta(Base):
    __tablename__ = "lineas_rutas"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    linea_id: Mapped[int] = mapped_column(ForeignKey("lineas.id"), nullable=False)
    ruta_id: Mapped[int] = mapped_column(ForeignKey("rutas.id"), nullable=False)
    distancia: Mapped[float] = mapped_column(Float, nullable=False)
    tiempo: Mapped[float] = mapped_column(Float, nullable=False)

    linea: Mapped["Linea"] = relationship("Linea", back_populates="lineas_rutas")
    ruta: Mapped["Ruta"] = relationship("Ruta", back_populates="lineas_rutas")
    lineas_puntos: Mapped[list["LineaPunto"]] = relationship("LineaPunto", back_populates="linea_ruta")
