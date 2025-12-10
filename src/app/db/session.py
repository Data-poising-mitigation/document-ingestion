## Engine and session setup for DB interactions

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.config import settings

# Create SQLAlchemy engine
engine = create_engine(
    settings.sqlalchemy_url,
    pool_pre_ping=True,
    future=True,
)

# Session factory
SessionLocal = sessionmaker(
    bind=engine,
    autocommit=False,
    autoflush=False,
    future=True,
)


# FastAPI dependency to get a DB session
def get_db():
    """
    Get the database session
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
