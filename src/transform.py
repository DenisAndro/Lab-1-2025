from __future__ import annotations
from datetime import datetime, timezone
import pandas as pd

def normalize_hourly(payload: dict) -> pd.DataFrame:
    meta = payload["_meta"]
    city = meta["city"]
    h = payload["hourly"]

    df = pd.DataFrame({
        "city": city,
        "ts": pd.to_datetime(h["time"]),
        "temperature": h["temperature_2m"],
        "precipitation": h["precipitation"],
        "wind_speed": h["windspeed_10m"],
        "wind_direction": h["winddirection_10m"],
        "ingested_at": datetime.now(timezone.utc),
    })

    df = df.dropna(subset=["ts"])
    return df[
        ["city", "ts", "temperature", "precipitation", "wind_speed", "wind_direction", "ingested_at"]
    ]


def aggregate_daily(hourly_df: pd.DataFrame) -> pd.DataFrame:
    row = {
        "city": hourly_df["city"].iloc[0],
        "date": hourly_df["ts"].dt.date.iloc[0],
        "temp_min_c": float(hourly_df["temperature"].astype(float).min()),
        "temp_max_c": float(hourly_df["temperature"].astype(float).max()),
        "temp_avg_c": float(hourly_df["temperature"].astype(float).mean()),
        "precipitation_sum_mm": float(hourly_df["precipitation"].astype(float).sum()),
        "wind_speed_max_ms": float(hourly_df["wind_speed"].astype(float).max()),
        "ingested_at": datetime.now(timezone.utc),
    }
    return pd.DataFrame([row])
