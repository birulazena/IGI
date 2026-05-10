import pytest
from unittest.mock import patch, MagicMock
from datetime import date, timedelta
from django.contrib.auth.models import User
from agency.models import Profile, Order, Tour, Hotel, Country
from agency.service.statistics_service import StatisticsService
import requests
from agency.service.weather_service import WeatherService
from agency.service.currency_service import CurrencyService



@pytest.mark.django_db
class TestStatisticsService:

    def test_sales_stats_empty(self):
        stats = StatisticsService.get_sales_stats()
        assert stats == {"mean": 0, "median": 0, "mode": 0}

    def test_sales_stats_with_data(self):
        country = Country.objects.create(name="TestCountry", climate_summer="Hot", climate_winter="Cold")
        hotel = Hotel.objects.create(name="TestHotel", country=country, stars=5)

        tour1 = Tour.objects.create(title="Tour A", hotel=hotel, duration_weeks=1, price=100)
        tour2 = Tour.objects.create(title="Tour B", hotel=hotel, duration_weeks=1, price=200)

        user = User.objects.create(username="client1")
        client = Profile.objects.create(
            user=user, role='client', address='City A', phone='12345', birth_date=date(2000, 1, 1)
        )

        o1 = Order.objects.create(client=client, departure_date=date.today())
        o1.tours.add(tour1)

        o2 = Order.objects.create(client=client, departure_date=date.today())
        o2.tours.add(tour1, tour2)

        o3 = Order.objects.create(client=client, departure_date=date.today())
        o3.tours.add(tour1)

        stats = StatisticsService.get_sales_stats()
        assert stats["mean"] == 166.67
        assert stats["median"] == 100.0
        assert stats["mode"] == 100.0

    @patch('statistics.mode')
    def test_sales_stats_mode_exception(self, mock_mode):
        mock_mode.side_effect = Exception("Artificial Error")

        user = User.objects.create(username="client2")
        client = Profile.objects.create(user=user, role='client', address='City B', phone='67890',
                                        birth_date=date(2000, 1, 1))
        order = Order.objects.create(client=client, departure_date=date.today())
        country = Country.objects.create(name="TestCountry2", climate_summer="Hot", climate_winter="Cold")
        hotel = Hotel.objects.create(name="TestHotel2", country=country, stars=5)
        tour = Tour.objects.create(title="Tour C", hotel=hotel, duration_weeks=1, price=100)
        order.tours.add(tour)

        stats = StatisticsService.get_sales_stats()
        assert stats["mode"] == "No unique mode"

    def test_age_stats_empty(self):
        stats = StatisticsService.get_clients_age_stats()
        assert stats == {"mean": 0, "median": 0}

    def test_age_stats_with_data(self):
        today = date.today()

        u1 = User.objects.create(username="c1")
        Profile.objects.create(
            user=u1, role='client', address='A', phone='1',
            birth_date=date(today.year - 20, 1, 1)
        )

        u2 = User.objects.create(username="c2")
        Profile.objects.create(
            user=u2, role='client', address='B', phone='2',
            birth_date=date(today.year - 30, 1, 1)
        )

        stats = StatisticsService.get_clients_age_stats()
        assert stats["mean"] == 25.0
        assert stats["median"] == 25.0


class TestWeatherService:

    @patch('agency.service.weather_service.settings')
    def test_weather_missing_config(self, mock_settings):
        mock_settings.WEATHER_API_KEY = ''
        mock_settings.WEATHER_API_URL = ''

        result = WeatherService.get_current_weather("Minsk")

        assert result == {"error": "Weather API not configured"}

    @patch('agency.service.weather_service.requests.get')
    def test_weather_success(self, mock_get):
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "main": {"temp": 22.5},
            "weather": [{"description": "clear sky"}]
        }
        mock_get.return_value = mock_response

        result = WeatherService.get_current_weather("Minsk")

        assert result["temp"] == 22.5
        assert result["description"] == "Clear sky"
        mock_get.assert_called_once()

    @patch('agency.service.weather_service.requests.get')
    def test_weather_request_exception(self, mock_get):
        mock_get.side_effect = requests.RequestException("Connection error")

        result = WeatherService.get_current_weather("Minsk")

        assert result == {"error": "Could not fetch weather data"}
        mock_get.assert_called_once()


class TestCurrencyService:

    @patch('agency.service.currency_service.requests.get')
    def test_currency_success(self, mock_get):
        mock_response = MagicMock()
        mock_response.json.return_value = {'Cur_OfficialRate': 3.25}
        mock_get.return_value = mock_response

        result = CurrencyService.get_usd_rate()

        assert result == 3.25
        mock_get.assert_called_once()

    @patch('agency.service.currency_service.requests.get')
    def test_currency_request_exception(self, mock_get):
        mock_get.side_effect = requests.RequestException("NBRB API Down")

        result = CurrencyService.get_usd_rate()

        assert result == 0.0
        mock_get.assert_called_once()