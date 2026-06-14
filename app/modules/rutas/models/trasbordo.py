from sqlalchemy import Float, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base


class Trasbordo(Base):
    __tablename__ = "trasbordos"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=False)
    punto_id: Mapped[int] = mapped_column(ForeignKey("puntos.id"), nullable=False)
    linea_origen_id: Mapped[int] = mapped_column(ForeignKey("lineas.id"), nullable=False)
    linea_destino_id: Mapped[int] = mapped_column(ForeignKey("lineas.id"), nullable=False)
    penalizacion_min: Mapped[float] = mapped_column(Float, nullable=False)

    punto: Mapped["Punto"] = relationship("Punto")
    linea_origen: Mapped["Linea"] = relationship("Linea", foreign_keys=[linea_origen_id])
    linea_destino: Mapped["Linea"] = relationship("Linea", foreign_keys=[linea_destino_id])
