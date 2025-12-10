import uuid
from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)

def test_ingest_creates_document(monkeypatch):
    # In a real test, use a transactional test DB; here we just hit the live app.
    payload = {
        "source_type": "pdf",
        "source_uri": "s3://bucket/doc.pdf",
        "title": "Test Doc",
        "raw_content": "Hello world",
        "metadata": {"foo": "bar"},
    }
    resp = client.post("/ingest", json=payload)
    assert resp.status_code == 201
    body = resp.json()
    assert "document_id" in body
    assert uuid.UUID(body["document_id"])
