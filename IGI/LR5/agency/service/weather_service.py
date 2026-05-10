import requests
import logging
from django.conf import settings

logger = logging.getLogger(__name__)

class WeatherService:
    """Service to handle OpenWeatherMap API"""

    @staticmethod
    def get_current_weather(location_name: str) -> dict:
        """
        Fetches current weather for a specific location
        Returns a dictionary with temperature and description.
        """
        if not settings.WEATHER_API_KEY or not settings.WEATHER_API_URL:
            logger.error("Weather API configuration is missing in environment variables")
            return {"error": "Weather API not configured"}

        params = {
            "q": location_name,
            "appid": settings.WEATHER_API_KEY,
            "units": "metric",
            "lang": "en",
        }

        try:
            response = requests.get(settings.WEATHER_API_URL, params=params, timeout=5)
            response.raise_for_status()
            data = response.json()

            return {
                "temp": data["main"]["temp"],
                "description": data["weather"][0]["description"].capitalize()
            }
        except requests.RequestException as e:
            logger.error(f"Failed to fetch weather for {location_name}: {e}")
            return {"error": "Could not fetch weather data"}