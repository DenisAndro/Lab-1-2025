from __future__ import annotations
import requests

from config import settings

def send_message(text: str) -> None:
    if not settings.telegram_bot_token or not settings.telegram_chat_id:
        # чтобы лабораторка не падала, если токены не заданы
        return
    url = f"https://api.telegram.org/bot{settings.telegram_bot_token}/sendMessage"
    payload = {"chat_id": settings.telegram_chat_id, "text": text}
    r = requests.post(url, json=payload, timeout=20)
    r.raise_for_status()

def build_summary(city: str, daily_row: dict) -> str:
    w = daily_row["wind_speed_max_ms"]
    p = daily_row["precipitation_sum_mm"]

    warn = []
    if w >= 12:
        warn.append("⚠️ Сильный ветер")
    if p >= 10:
        warn.append("⚠️ Сильные осадки")

    warn_txt = ("\n" + " ".join(warn)) if warn else ""
    return (
        f"Прогноз на завтра: {city}\n"
        f"🌡 min: {daily_row['temp_min_c']:.1f}°C, max: {daily_row['temp_max_c']:.1f}°C, avg: {daily_row['temp_avg_c']:.1f}°C\n"
        f"🌧 осадки: {daily_row['precipitation_sum_mm']:.1f} мм\n"
        f"💨 ветер (max): {daily_row['wind_speed_max_ms']:.1f} м/с"
        f"{warn_txt}"
    )
