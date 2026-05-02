import os

from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from database import get_db
from llm_factory import create_llm_client
from models import Weather, City
from services import analyze_weather_with_ai

app = FastAPI(title="Weather API")

adapter = create_llm_client()
model = os.environ.get("AI_MODEL")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/weather/{city_name}")
def get_weather_by_city(city_name: str, db: Session = Depends(get_db)):
    results = db.query(Weather).filter(Weather.city.ilike(city_name)).all()
    return results


@app.get("/weather")
def get_all_weather(db: Session = Depends(get_db)):
    return db.query(Weather).order_by(Weather.forecast_datetime.desc()).all()


@app.get("/cities")
def get_all_cities(db: Session = Depends(get_db)):
    return db.query(City).all()


@app.post("/cities")
def add_city(name: str, db: Session = Depends(get_db)):
    city = City(name=name)
    db.add(city)
    try:
        db.commit()
        db.refresh(city)
        return city
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="City already exists")


@app.delete("/cities/{city_name}")
def delete_city(city_name: str, db: Session = Depends(get_db)):
    city = db.query(City).filter(City.name.ilike(city_name)).first()
    if not city:
        raise HTTPException(status_code=404, detail="City not found")
    db.delete(city)
    db.commit()
    return {"status": "deleted", "city": city_name}


@app.post("/ai/ask")
def ask_ai(question: str, db: Session = Depends(get_db)):
    if not model:
        raise HTTPException(status_code=500, detail="AI_MODEL environment variable not set")
    return {"answer": analyze_weather_with_ai(question, adapter, model, db)}