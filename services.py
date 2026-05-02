from datetime import datetime
import os
import requests
from dotenv import load_dotenv
from fastapi import Depends
from sqlalchemy.orm import Session

from database import SessionLocal, get_db
from llm_integration import LlmIntegration
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


def analyze_weather_with_ai(question: str, llm_client: LlmIntegration, ai_model: str, db: Session = Depends(get_db)):
    data = db.query(Weather).order_by(Weather.forecast_datetime.desc()).limit(20).all()
    lines = []
    for item in data:
        lines.append(f"{item.city}: {item.temperature}ºC, {item.description}, {item.forecast_datetime}")
    context = "\n".join(lines)
    message = [
        {"role": "system", "content": "Answer concisely and directly, maximum 2 sentences."},
        {"role": "user", "content": f"{context}\n\nQuestion: {question}"}
    ]
    return llm_client.client_communication(message, ai_model)
