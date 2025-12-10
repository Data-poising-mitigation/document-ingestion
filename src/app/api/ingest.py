from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.ingestion.basic import BasicIngestion
from app.schemas.ingest import IngestRequest, IngestResponse

router = APIRouter(prefix="/ingest", tags=["ingest"])
ingestor = BasicIngestion()

@router.post("", response_model=IngestResponse, status_code=201)
def ingest_document(payload: IngestRequest, db: Session = Depends(get_db)):
    return ingestor.ingest(db, payload)
