import os
from pydantic import BaseModel
from dotenv import load_dotenv

load_dotenv()


class Settings(BaseModel):
    service_name: str = os.getenv("SERVICE_NAME", "document-ingestion")
    port: int = int(os.getenv("PORT", "8080"))

    # Single source of truth for DB access (local + Cloud Run)
    database_url: str = os.getenv("DATABASE_URL", "").strip()

    def __init__(self, **data):
        super().__init__(**data)
        if not self.database_url:
            raise ValueError(
                "DATABASE_URL is not set. "
                "Set it to your Supabase session pooler connection string "
                "and include '?sslmode=require'."
            )


settings = Settings()
