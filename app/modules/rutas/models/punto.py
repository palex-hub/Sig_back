from sqlalchemy import Boolean, Float, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base


class Punto(Base):
    __tablename__ = "puntos"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    latitud: Mapped[float] = mapped_column(Float, nullable=False)
    longitud: Mapped[float] = mapped_column(Float, nullable=False)
    descripcion: Mapped[str] = mapped_column(String(100), nullable=True)
    stop: Mapped[bool] = mapped_column(Boolean, default=False)

    lineas_puntos: Mapped[list["LineaPunto"]] = relationship(
        "LineaPunto", back_populates="punto", foreign_keys="LineaPunto.punto_id"
    )
