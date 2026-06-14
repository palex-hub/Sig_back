from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

from app.core.config import DATABASE_URL, DEBUG


class Base(DeclarativeBase):
    pass


engine = create_engine(DATABASE_URL, echo=DEBUG, pool_pre_ping=True, pool_recycle=300)
SessionLocal = sessionmaker(engine, expire_on_commit=False)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
