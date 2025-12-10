## Engine and session setup for DB interactions

from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import OperationalError
from app.config import settings

# Create SQLAlchemy engine
engine = create_engine(
    settings.sqlalchemy_url,
    pool_pre_ping=True,
    future=True,
    connect_args={"connect_timeout": 3},
)

# Fail fast if the database is unreachable on startup/import
try:
    with engine.connect() as conn:
        conn.execute(text("SELECT 1"))
except OperationalError as exc:
    raise RuntimeError(f"Database unreachable at {settings.sqlalchemy_url}") from exc

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
