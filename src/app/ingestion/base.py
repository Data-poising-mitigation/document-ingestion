## Base ingestion strategy

from abc import ABC, abstractmethod
from sqlalchemy.orm import Session

from app.schemas.ingest import IngestRequest, IngestResponse

class IngestionStrategy(ABC):
    @abstractmethod
    def ingest(self, db: Session, request: IngestRequest) -> IngestResponse:
        ...
