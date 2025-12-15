import os
from dataclasses import dataclass
from dotenv import load_dotenv

load_dotenv()

@dataclass(frozen=True)
class Settings:
    clickhouse_host: str = os.getenv("CLICKHOUSE_HOST", "localhost")
    clickhouse_port: int = int(os.getenv("CLICKHOUSE_PORT", "9000"))
    clickhouse_db: str = os.getenv("CLICKHOUSE_DB", "weather")
    clickhouse_user: str = os.getenv("CLICKHOUSE_USER", "default")
    clickhouse_password: str = os.getenv("CLICKHOUSE_PASSWORD", "")

    minio_endpoint: str = os.getenv("MINIO_ENDPOINT", "localhost:9002")
    minio_access_key: str = os.getenv("MINIO_ACCESS_KEY", "minioadmin")
    minio_secret_key: str = os.getenv("MINIO_SECRET_KEY", "minioadmin123")
    minio_bucket: str = os.getenv("MINIO_BUCKET", "weather-raw")
    minio_secure: bool = os.getenv("MINIO_SECURE", "false").lower() == "true"

    telegram_bot_token: str = os.getenv("TELEGRAM_BOT_TOKEN", "")
    telegram_chat_id: str = os.getenv("TELEGRAM_CHAT_ID", "")

settings = Settings()