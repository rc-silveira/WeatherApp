from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session

from database import get_db
from models import Weather, City

app = FastAPI(title="Weather API")


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
    db.commit()
    db.refresh(city)
    return city


@app.delete("/cities/{city_name}")
def delete_city(city_name: str, db: Session = Depends(get_db)):
    city = db.query(City).filter(City.name.ilike(city_name)).first()
    if not city:
        return {"message": "City not found"}, 404
    db.delete(city)
    db.commit()
    return {"status": "deleted", "city": city_name}
