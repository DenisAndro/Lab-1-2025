from __future__ import annotations
import json
from minio import Minio
from minio.error import S3Error
from datetime import datetime
from io import BytesIO

from config import settings

def get_minio_client() -> Minio:
    return Minio(
        settings.minio_endpoint,
        access_key=settings.minio_access_key,
        secret_key=settings.minio_secret_key,
        secure=settings.minio_secure,
    )

def ensure_bucket(client: Minio, bucket: str) -> None:
    found = client.bucket_exists(bucket)
    if not found:
        client.make_bucket(bucket)

def put_raw_json(client: Minio, bucket: str, city: str, forecast_date: str, payload: dict) -> str:
    key = f"open-meteo/{city}/{forecast_date}/raw_{datetime.utcnow().strftime('%Y%m%dT%H%M%SZ')}.json"
    b = json.dumps(payload, ensure_ascii=False).encode("utf-8")
    client.put_object(
        bucket,
        key,
        data=BytesIO(b),
        length=len(b),
        content_type="application/json",
    )
    return key
