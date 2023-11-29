from requests_mock import Mocker
from rest_framework import status
from rest_framework.test import APITestCase

from apps.core.models import City, WeatherForecast
from apps.core.tests.factories import ForecastPartFactory, WeatherForecastFactory


class WeatherForecastViewTestCase(APITestCase):
    path = "/core/weather-forecast"

    @staticmethod
    def get_expected_data(weather_forecast):
        forecast_parts = weather_forecast.forecast_parts.all()

        return {
            "city_name": weather_forecast.city.name,
            "forecast_date": weather_forecast.date,
            "forecast_parts": [
                {
                    "part_name": forecast_parts[number_part].part_name,
                    "temp_min": forecast_parts[number_part].temp_min,
                    "temp_max": forecast_parts[number_part].temp_max,
                    "temp_avg": forecast_parts[number_part].temp_avg,
                    "feels_like": forecast_parts[number_part].feels_like,
                    "condition": forecast_parts[number_part].condition,
                    "wind_speed": forecast_parts[number_part].wind_speed,
                    "pressure_mm": forecast_parts[number_part].pressure_mm,
                    "humidity": forecast_parts[number_part].humidity,
                }
                for number_part in range(4)
            ],
        }

    def test_city_not_found(self):
        city_name = "Moscow"

        response = self.client.get(f"{self.path}?city={city_name}")

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data, f"{city_name} not found")

    @Mocker()
    def test_without_saved_forecast(self, request_mock):
        city = City.objects.first()
        lat, lon = city.coords.values()

        expected_json_data = {
            "forecasts": [
                {
                    "date": "2023-11-29",
                    "date_ts": 1701260647,
                    "parts": {
                        key: {
                            "temp_min": 5,
                            "temp_max": 10,
                            "temp_avg": 7,
                            "feels_like": 10,
                            "condition": "clear",
                            "wind_speed": 2.5,
                            "pressure_mm": 800,
                            "humidity": 30,
                        }
                        for key in ("night", "morning", "day", "evening")
                    },
                }
            ]
        }

        request_mock.get(
            f"https://api.weather.yandex.ru/v2/forecast?lat={lat}&lon={lon}",
            json=expected_json_data,
        )

        response = self.client.get(f"{self.path}?city={city.name}")

        weather_forecast = WeatherForecast.objects.get()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertDictEqual(response.json(), self.get_expected_data(weather_forecast))

    def test_with_saved_forecast(self):
        weather_forecast = WeatherForecastFactory()
        ForecastPartFactory.create_batch(size=4, weather_forecast=weather_forecast)

        response = self.client.get(f"{self.path}?city={weather_forecast.city.name}")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertDictEqual(response.json(), self.get_expected_data(weather_forecast))
