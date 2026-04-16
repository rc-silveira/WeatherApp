from datetime import datetime
import os
import requests
from dotenv import load_dotenv

from database import SessionLocal
from models import Weather

load_dotenv()


def fetch_weather(city):
    api_key = os.getenv("WEATHER_API_KEY")
    url = "https://api.openweathermap.org/data/2.5/weather"

    params = {
        "q": city,
        "appid": api_key,
        "units": "metric",
        "lang": "pt"
    }

    response = requests.get(url, params=params)

    if response.status_code != 200:
        print(f"{response.status_code}")
        return None

    data = response.json()

    weather_info = {
        "city": data["name"],
        "temperature": data["main"]["temp"],
        "description": data["weather"][0]["description"],
        "forecast_datetime": datetime.fromtimestamp(data["dt"]),
        "humidity": data["main"]["humidity"]
    }

    db = SessionLocal()

    existing = db.query(Weather).filter(
        Weather.city == weather_info["city"],
        Weather.forecast_datetime == weather_info["forecast_datetime"]
    ).first()

    if existing:
        db.close()
        return weather_info

    new_record = Weather(**weather_info)
    db.add(new_record)
    db.commit()
    db.refresh(new_record)
    db.close()

    return weather_info
