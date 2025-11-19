from __future__ import annotations

from contextlib import contextmanager
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, Generator

from sqlalchemy import JSON, Column, DateTime, Float, Integer, String, create_engine
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker

from .utils import ensure_directory, get_path_from_config


class Base(DeclarativeBase):
    pass


class PredictionLog(Base):
    __tablename__ = "prediction_logs"

    id = Column(Integer, primary_key=True, autoincrement=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    bedrooms = Column(Float, nullable=False)
    bathrooms = Column(Float, nullable=False)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    sqft_living = Column(Float, nullable=False)
    predicted_price = Column(Float, nullable=False)
    lower_bound = Column(Float, nullable=True)
    upper_bound = Column(Float, nullable=True)
    shap_contributions = Column(JSON, nullable=True)


def _get_db_path() -> Path:
    db_path = get_path_from_config("paths", "database")
    ensure_directory(db_path.parent)
    return db_path


def get_engine():
    path = _get_db_path()
    return create_engine(f"sqlite:///{path}", future=True)


engine = get_engine()
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False, future=True)


def init_db() -> None:
    Base.metadata.create_all(bind=engine)


@contextmanager
def get_session() -> Generator[Session, None, None]:
    session: Session = SessionLocal()
    try:
        yield session
        session.commit()
    except Exception:  # pragma: no cover - defensive rollback
        session.rollback()
        raise
    finally:
        session.close()


def log_prediction(record: Dict[str, Any]) -> int:
    with get_session() as session:
        log_entry = PredictionLog(**record)
        session.add(log_entry)
        session.flush()
        return log_entry.id
