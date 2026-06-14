from sqlalchemy import Float, ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base


class LineaPunto(Base):
    __tablename__ = "lineas_puntos"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    linea_ruta_id: Mapped[int] = mapped_column(ForeignKey("lineas_rutas.id"), nullable=False)
    punto_id: Mapped[int] = mapped_column(ForeignKey("puntos.id"), nullable=False)
    punto_destino_id: Mapped[int] = mapped_column(ForeignKey("puntos.id"),nullable=True)
    orden: Mapped[int] = mapped_column(Integer, nullable=False)
    distancia: Mapped[float] = mapped_column(Float, nullable=False)
    tiempo: Mapped[float] = mapped_column(Float, nullable=False)

    linea_ruta: Mapped["LineaRuta"] = relationship("LineaRuta", back_populates="lineas_puntos")
    punto: Mapped["Punto"] = relationship("Punto", back_populates="lineas_puntos", foreign_keys=[punto_id])
