from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base


class Ruta(Base):
    __tablename__ = "rutas"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    descripcion: Mapped[str] = mapped_column(String(100), nullable=False)

    lineas_rutas: Mapped[list["LineaRuta"]] = relationship("LineaRuta", back_populates="ruta")
