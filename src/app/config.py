import os
from pydantic import BaseModel


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
            # Local dev: use TCP host (e.g. Cloud SQL public IP)
            host_part = self.db_host
        elif self.instance_connection_name:
            # Cloud Run: use Unix domain socket path
            host_part = f"/cloudsql/{self.instance_connection_name}"
        else:
            # Fallback for e.g. local Docker compose or default
            host_part = "localhost"

        return (
            f"postgresql+psycopg://{self.db_user}:{self.db_password}"
            f"@{host_part}:{self.db_port}/{self.db_name}"
        )


settings = Settings()
