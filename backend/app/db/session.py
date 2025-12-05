# app/db/session.py (Phiên bản Đồng bộ)
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# ❌ Không dùng postgresql+asyncpg
# ✅ Dùng postgresql://...
DATABASE_URL = "postgresql://postgres:1234@localhost:5432/tourismdb"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)