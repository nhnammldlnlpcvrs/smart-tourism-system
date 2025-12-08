# backend/app/db/session.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.ext.declarative import declarative_base
from fastapi import Depends

DATABASE_URL = "postgresql://postgres:abc123@localhost:5432/tourismdb"

# Engine
engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True
)

# SessionLocal
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

# Base class cho models
Base = declarative_base()


# Dependency cho FastAPI
def get_db():
    db: Session = SessionLocal()
    try:
        yield db
    finally:
        db.close()