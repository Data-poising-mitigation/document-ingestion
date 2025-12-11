import os
from pydantic import BaseModel
from dotenv import load_dotenv
load_dotenv()

class Settings(BaseModel):
    # Common settings
    db_name: str = os.getenv("DB_NAME", "ragdb")
    db_user: str = os.getenv("DB_USER", "postgres")
    db_password: str = os.getenv("DB_PASSWORD", "postgres")
    db_port: int = int(os.getenv("DB_PORT", "5432"))

    # For local TCP connection
    db_host: str | None = os.getenv("DB_HOST")

    # For Cloud Run → Cloud SQL via Unix socket
    instance_connection_name: str | None = os.getenv("INSTANCE_CONNECTION_NAME")

    @property
    def sqlalchemy_url(self) -> str:
        """
        Build a SQLAlchemy URL that works either:
        - locally via TCP (DB_HOST set)
        - on Cloud Run via Unix socket (/cloudsql/INSTANCE_CONNECTION_NAME)
        """
        if self.db_host:
            # Local dev: TCP host (e.g. 127.0.0.1 or Cloud SQL public IP)
            return (
                f"postgresql+psycopg://{self.db_user}:{self.db_password}"
                f"@{self.db_host}:{self.db_port}/{self.db_name}"
            )

        if self.instance_connection_name:
            # Cloud Run: Unix socket
            socket_path = f"/cloudsql/{self.instance_connection_name}"
            return (
                f"postgresql+psycopg://{self.db_user}:{self.db_password}"
                f"@/{self.db_name}?host={socket_path}"
            )

        # Fallback (e.g. everything local)
        return (
            f"postgresql+psycopg://{self.db_user}:{self.db_password}"
            f"@localhost:{self.db_port}/{self.db_name}"
        )

settings = Settings()
