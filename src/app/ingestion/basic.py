## Basic ingestion strategy

from sqlalchemy.orm import Session

from app.db import models
from app.schemas.ingest import IngestRequest, IngestResponse

class BasicIngestion(IngestionStrategy := object):  # keeps it simple; could also subclass IngestionStrategy
    def ingest(self, db: Session, request: IngestRequest) -> IngestResponse:
        doc = models.Document(
            source_type=request.source_type,
            source_uri=request.source_uri,
            title=request.title,
            raw_content=request.raw_content,
            metadata_json=request.metadata,
        )
        db.add(doc)
        db.commit()
        db.refresh(doc)
        return IngestResponse(document_id=str(doc.id))
