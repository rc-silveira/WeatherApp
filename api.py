from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session

from database import get_db
from models import Weather

app = FastAPI(title="Weather API")


@app.get("/weather/{city_name}")
def get_weather_by_city(city_name: str, db: Session = Depends(get_db)):
    results = db.query(Weather).filter(Weather.city.ilike(city_name)).all()
    return results


@app.get("/weather")
def get_all_weather(db: Session = Depends(get_db)):
    return db.query(Weather).order_by(Weather.forecast_datetime.desc()).all()
