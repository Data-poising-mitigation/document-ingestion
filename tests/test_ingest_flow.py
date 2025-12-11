import uuid
from fastapi.testclient import TestClient
from unittest.mock import MagicMock

from app.main import app
from app.api import ingest as ingest_api
from app.ingestion.basic import BasicIngestion
from app.schemas.ingest import IngestRequest, IngestResponse


def test_ingest_route_uses_stubbed_ingestor(monkeypatch):
    # Stub ingestor and DB dependency so no real DB is touched.
    stub_ingestor = MagicMock()
    stub_ingestor.ingest.return_value = IngestResponse(document_id="123")

    def fake_db():
        yield MagicMock()

    # Override dependencies
    monkeypatch.setattr(ingest_api, "ingestor", stub_ingestor)
    app.dependency_overrides[ingest_api.get_db] = fake_db  # type: ignore[attr-defined]

    client = TestClient(app)
    payload = {
        "source_type": "pdf",
        "source_uri": "s3://bucket/doc.pdf",
        "title": "Test Doc",
        "raw_content": "Hello world",
        "metadata": {"foo": "bar"},
    }

    resp = client.post("/ingest", json=payload)
    assert resp.status_code == 201
    assert resp.json() == {"document_id": "123"}
    stub_ingestor.ingest.assert_called_once()


def test_basic_ingestion_calls_db_and_returns_uuid():
    fake_session = MagicMock()
    fake_uuid = uuid.uuid4()

    def fake_refresh(obj):
        obj.id = fake_uuid  # simulate DB assigning PK

    fake_session.refresh.side_effect = fake_refresh

    ingestion = BasicIngestion()
    request = IngestRequest(
        source_type="pdf",
        source_uri="s3://bucket/doc.pdf",
        title="Test Doc",
        raw_content="Hello world",
        metadata={"foo": "bar"},
    )

    response = ingestion.ingest(fake_session, request)

    fake_session.add.assert_called_once()
    fake_session.commit.assert_called_once()
    fake_session.refresh.assert_called_once()
    assert response.document_id == str(fake_uuid)
    uuid.UUID(response.document_id)
