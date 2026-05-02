import os
from unittest.mock import patch

os.environ["AI_PROVIDER"] = "groq"
os.environ["AI_MODEL"] = "llama3.2"
os.environ["GROQ_API_KEY"] = "fake-key"
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from api import app
from database import get_db
from models import Base, Weather

from datetime import datetime

SQLALCHEMY_TEST_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(SQLALCHEMY_TEST_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db


@pytest.fixture(autouse=True)
def setup_database():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)

client = TestClient(app)


def test_get_all_weather_empty():
    response = client.get("/weather")
    assert response.status_code == 200
    assert response.json() == []


def test_add_city():
    response = client.post("/cities?name=Lisbon")
    assert response.status_code == 200
    assert response.json()["name"] == "Lisbon"


def test_get_cities():
    client.post("/cities?name=Lisbon")
    response = client.get("/cities")
    assert response.status_code == 200
    assert len(response.json()) == 1


def test_delete_city():
    client.post("/cities?name=Lisbon")
    response = client.delete("/cities/Lisbon")
    assert response.status_code == 200
    assert response.json()["status"] == "deleted"


def test_add_duplicate_city():
    client.post("/cities?name=Lisbon")
    response = client.post("/cities?name=Lisbon")
    assert response.status_code == 400

def test_get_weather_by_city():
    db = TestingSessionLocal()
    record = Weather(city="Lisbon", temperature=20.0, description="céu limpo", humidity=60, forecast_datetime=datetime.now(), created_at= datetime.now())
    db.add(record)
    db.commit()
    db.close()

    response = client.get("/weather/Lisbon")
    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]["city"] == "Lisbon"


def test_delete_city_not_found():
    response = client.delete("/cities/CidadeInexistente")
    assert response.status_code == 404

def test_ask_ai():
    with patch("api.analyze_weather_with_ai", return_value="It will be sunny in Lisbon."):
        response = client.post("/ai/ask?question=What is the weather like?")
        assert response.status_code == 200