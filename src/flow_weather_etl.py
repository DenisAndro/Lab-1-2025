from __future__ import annotations
from datetime import date, timedelta
from prefect import flow, task, get_run_logger

from open_meteo import fetch_forecast_for_tomorrow, CITIES
from storage_minio import get_minio_client, ensure_bucket, put_raw_json
from transform import normalize_hourly, aggregate_daily
from clickhouse import insert_hourly, insert_daily
from notify_telegram import send_message, build_summary
from config import settings

@task(retries=3, retry_delay_seconds=10)
def extract_city(city: str, tomorrow: date) -> dict:
    return fetch_forecast_for_tomorrow(city, tomorrow)

@task
def save_raw(payload: dict) -> str:
    meta = payload["_meta"]
    client = get_minio_client()
    ensure_bucket(client, settings.minio_bucket)
    return put_raw_json(client, settings.minio_bucket, meta["city"], meta["forecast_date"], payload)

@task
def transform_hourly(payload: dict):
    return normalize_hourly(payload)

@task
def transform_daily(hourly_df):
    return aggregate_daily(hourly_df)

@task(retries=3, retry_delay_seconds=5)
def load_hourly(df):
    insert_hourly(df)

@task(retries=3, retry_delay_seconds=5)
def load_daily(df):
    insert_daily(df)

@task
def notify(daily_df):
    row = daily_df.iloc[0].to_dict()
    text = build_summary(row["city"], row)
    send_message(text)

@flow(name="weather_etl")
def weather_etl():
    logger = get_run_logger()
    tomorrow = date.today() + timedelta(days=1)
    logger.info(f"Forecast date: {tomorrow}")

    for city in CITIES.keys():
        payload = extract_city(city, tomorrow)
        key = save_raw(payload)
        logger.info(f"Saved raw JSON to MinIO: {key}")

        hourly_df = transform_hourly(payload)
        daily_df = transform_daily(hourly_df)

        load_hourly(hourly_df)
        load_daily(daily_df)

        notify(daily_df)

if __name__ == "__main__":
    weather_etl()
