from typing import Type
from sqlalchemy.engine.base import Engine
from sqlalchemy.orm.decl_api import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy import create_engine
from ..config import settings

engine: Engine = create_engine(
    settings.DATABASE_URL, echo=settings.DATABASE_ECHO, future=settings.DATABASE_FUTURE
)

SessionLocal: sessionmaker = sessionmaker(
    autocommit=settings.DATABASE_AUTOCOMMIT,
    autoflush=settings.DATABASE_AUTOFLUSH,
    bind=engine,
)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
