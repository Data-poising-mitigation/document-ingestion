# document-ingestion
Service to upload documents to corpus

set PYTHONPATH=%cd%\src
python -m uvicorn app.main:app --reload --app-dir src