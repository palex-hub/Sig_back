from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class Linea(Base):
    __tablename__ = "lineas"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    nombre: Mapped[str] = mapped_column(String(50), nullable=False, unique=True)
    imagen_url: Mapped[str] = mapped_column(String(255), nullable=True)
    fecha_creada: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    color_id: Mapped[int] = mapped_column(ForeignKey("colores.id"), nullable=False)

    color: Mapped["Color"] = relationship("Color", back_populates="lineas")
    lineas_rutas: Mapped[list["LineaRuta"]] = relationship("LineaRuta", back_populates="linea")
