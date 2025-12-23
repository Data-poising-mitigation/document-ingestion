from fastapi import FastAPI
import logging
import os

from app.api import ingest as ingest_api

logger = logging.getLogger(__name__)


def create_app() -> FastAPI:
    app = FastAPI(title="Document Ingestion Service")

    def init_db() -> None:
        """
        Initialize the database (e.g. create tables if they don't exist).

        Import DB bits lazily so tests can import the app without needing
        DATABASE_URL set.
        """
        try:
            from sqlalchemy.exc import OperationalError
            from app.db import models  # ensure models are imported so metadata is ready
            from app.db.session import engine

            models.Base.metadata.create_all(bind=engine)
            logger.info("Database tables created or already exist.")
        except Exception as exc:
            # Don't crash the app on startup (Cloud Run friendliness)
            logger.warning("Database initialization failed: %s", exc)

    @app.on_event("startup")
    def on_startup() -> None:
        # Optional: allow disabling DB init in CI/tests
        if os.getenv("AUTO_INIT_DB", "true").lower() == "true":
            init_db()

        # Optional connectivity check (also lazy import)
        try:
            from app.db.session import check_db_connection

            ok = check_db_connection(raise_on_error=False)
            if ok:
                logger.info("Database connection check succeeded on startup.")
            else:
                logger.warning("Database connection check failed on startup.")
        except Exception as exc:
            logger.warning("Unexpected error during DB startup check: %s", exc)

    # Routers
    app.include_router(ingest_api.router)

    @app.get("/healthz")
    def healthz():
        """
        Basic health endpoint with optional DB check.
        """
        try:
            from app.db.session import check_db_connection

            db_ok = check_db_connection(raise_on_error=False)
        except Exception:
            db_ok = False

        return {"status": "ok", "db_ok": db_ok}

    return app


app = create_app()
