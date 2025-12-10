from fastapi import FastAPI

from app.api import ingest as ingest_api
from app.db import models  # ensure models are imported so metadata is ready
from app.db.session import engine

# Create tables if they don't exist (optional; for prod use migrations)
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Document Ingestion Service")

app.include_router(ingest_api.router)

@app.get("/healthz")
def healthz():
    return {"status": "ok"}
