# backend/tests/conftest.py
import os
import sys
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from fastapi.testclient import TestClient

# ====== FIX IMPORT PATH ======
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

from app.db.base import Base
from app.api.main import app
from app.db.session import SessionLocal

TEST_DB_URL = "postgresql://postgres:postgres@localhost:5432/smart_tourism_test"


@pytest.fixture(scope="session")
def test_engine():
    engine = create_engine(TEST_DB_URL)
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
    yield engine
    Base.metadata.drop_all(engine)


@pytest.fixture(scope="function")
def db_session(test_engine):
    """Transaction rollback để mỗi test có DB sạch"""
    connection = test_engine.connect()
    transaction = connection.begin()
    Session = sessionmaker(bind=connection)
    session = Session()

    yield session

    session.close()
    transaction.rollback()
    connection.close()


@pytest.fixture
def client(db_session, monkeypatch):
    """Override SessionLocal để API dùng DB test"""
    monkeypatch.setattr(SessionLocal, "__call__", lambda self=db_session: db_session)
    return TestClient(app)
