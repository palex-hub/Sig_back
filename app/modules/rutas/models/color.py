from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class Color(Base):
    __tablename__ = "colores"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    nombre: Mapped[str] = mapped_column(String(100), nullable=False)
    cod_hex: Mapped[str] = mapped_column(String(7), nullable=False)

    lineas: Mapped[list["Linea"]] = relationship("Linea", back_populates="color")
