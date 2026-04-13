import os

from database import SessionLocal
from models import City
from services import fetch_weather
from dotenv import load_dotenv
load_dotenv()

def run_task():
    db = SessionLocal()
    cities = db.query(City).all()
    db.close()

    for city in cities:
        fetch_weather(city.name)

if __name__ == "__main__":
    run_task()