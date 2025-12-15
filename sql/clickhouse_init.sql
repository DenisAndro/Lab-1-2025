CREATE DATABASE IF NOT EXISTS weather;

CREATE TABLE IF NOT EXISTS weather.weather_hourly
(
  city String,
  ts DateTime,
  temperature Float32,
  precipitation Float32,
  wind_speed Float32,
  wind_direction Float32,
  ingested_at DateTime
)
ENGINE = MergeTree
ORDER BY (city, ts);

CREATE TABLE IF NOT EXISTS weather.weather_daily
(
  city String,
  date Date,
  temp_min_c Float32,
  temp_max_c Float32,
  temp_avg_c Float32,
  precipitation_sum_mm Float32,
  wind_speed_max_ms Float32,
  ingested_at DateTime
)
ENGINE = MergeTree
ORDER BY (city, date);
