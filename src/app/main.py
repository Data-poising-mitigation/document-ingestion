from fastapi import FastAPI
import logging

from sqlalchemy.exc import OperationalError

from app.api import ingest as ingest_api
from app.db import models  # ensure models are imported so metadata is ready
from app.db.session import engine, check_db_connection

logger = logging.getLogger(__name__)

app = FastAPI(title="Document Ingestion Service")


def init_db() -> None:
    """
    Initialize the database (e.g. create tables if they don't exist).

    This is called on startup instead of at import time so that
    the container can still start even if the DB is temporarily
    unavailable.
    """
    try:
        models.Base.metadata.create_all(bind=engine)
        logger.info("Database tables created or already exist.")
    except OperationalError as exc:
        # Log the error but *do not* crash the process, so Cloud Run
        # can still start the container and report useful logs.
        logger.warning("Database initialization failed: %s", exc)


@app.on_event("startup")
def on_startup() -> None:
    # Try to initialize the DB schema
    init_db()

    # Optional: run a lightweight connectivity check and just log the result.
    try:
        ok = check_db_connection(raise_on_error=False)
        if ok:
            logger.info("Database connection check succeeded on startup.")
        else:
            logger.warning("Database connection check failed on startup.")
    except Exception as exc:  # very defensive, don't kill the app on startup
        logger.warning("Unexpected error during DB startup check: %s", exc)


# Routers
app.include_router(ingest_api.router)


@app.get("/healthz")
def healthz():
    """
    Basic health endpoint.

    Optionally includes DB status without crashing the service if the DB
    is down.
    """
    db_ok = False
    try:
        db_ok = check_db_connection(raise_on_error=False)
    except Exception:
        db_ok = False

    return {
        "status": "ok",
        "db_ok": db_ok,
    }
