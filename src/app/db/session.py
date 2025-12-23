## Engine and session setup for DB interactions

from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import OperationalError
from sqlalchemy.pool import NullPool  # NEW
from app.config import settings
import logging

logger = logging.getLogger(__name__)

# Create SQLAlchemy engine
engine = create_engine(
    settings.database_url,
    pool_pre_ping=True,
    future=True,
    connect_args={"connect_timeout": 3},
    poolclass=NullPool,
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

def check_db_connection(raise_on_error: bool = False) -> bool:
    """
    Optional DB health check.

    Returns True if the DB is reachable, False otherwise.
    If raise_on_error is True, re-raises the OperationalError.
    """ 
    try:
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        return True
    except OperationalError as exc:
        logger.warning(
            "Database unreachable at %s: %s",
            settings.database_url,
            exc,
        )
        if raise_on_error:
            raise
        return False
