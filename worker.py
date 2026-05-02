from database import SessionLocal
from models import City
from services import fetch_weather
from dotenv import load_dotenv

load_dotenv()

def run_task():
    db = SessionLocal()
    try:
        cities = db.query(City).all()

        for city in cities:
            try:
                fetch_weather(city.name)
            except Exception as e:
                print(f"Error fetching weather for {city.name}: {e}")
    except Exception as e:
        print(e)
    finally:
        db.close()


if __name__ == "__main__":
    run_task()
