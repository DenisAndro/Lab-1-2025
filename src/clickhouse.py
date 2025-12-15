from clickhouse_driver import Client
from config import settings


def get_client():
    return Client(
        host=settings.clickhouse_host,
        port=9000,
        user=settings.clickhouse_user,
        password=settings.clickhouse_password,  
        database=settings.clickhouse_db,
    )


def insert_hourly(df):
    client = get_client()
    client.execute(
        """
        INSERT INTO weather.weather_hourly
        (city, ts, temperature, precipitation, wind_speed, wind_direction, ingested_at)
        VALUES
        """,
        df.to_dict("records"),
    )


def insert_daily(df):
    client = get_client()
    client.execute(
        """
        INSERT INTO weather.weather_daily
        (city, date, temp_min_c, temp_max_c, temp_avg_c,
         precipitation_sum_mm, wind_speed_max_ms, ingested_at)
        VALUES
        """,
        df.to_dict("records"),
    )
