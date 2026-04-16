from unittest.mock import patch, MagicMock
from services import fetch_weather


def test_fetch_weather_success():
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "name": "Lisbon",
        "main": {"temp": 20.0, "humidity": 60},
        "weather": [{"description": "céu limpo"}],
        "dt": 1700000000
    }

    with patch("services.requests.get", return_value=mock_response), \
            patch("services.SessionLocal") as mock_db:
        mock_session = MagicMock()
        mock_db.return_value = mock_session

        result = fetch_weather("Lisbon")

    assert result is not None
    assert result["city"] == "Lisbon"
    assert result["temperature"] == 20.0
    assert result["humidity"] == 60


def test_fetch_weather_failure():
    mock_response = MagicMock()
    mock_response.status_code = 404

    with patch("services.requests.get", return_value=mock_response):
        result = fetch_weather("Not a city")

    assert result is None
