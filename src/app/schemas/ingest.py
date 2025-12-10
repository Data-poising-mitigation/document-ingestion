from typing import Optional, Dict, Any
from pydantic import BaseModel, Field


class IngestRequest(BaseModel):
    source_type: str = Field(..., description="e.g. 'pdf', 'web', 'manual'")
    source_uri: Optional[str] = Field(
        default=None,
        description="Optional file path or URL of the source",
    )
    title: Optional[str] = None
    raw_content: str = Field(..., description="Full text of the document")
    metadata: Dict[str, Any] = Field(
        default_factory=dict,
        description="Arbitrary metadata to store as JSONB",
    )


class IngestResponse(BaseModel):
    document_id: str
