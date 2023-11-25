from django.utils import timezone
from requests_mock import Mocker
from rest_framework import status
from rest_framework.test import APITestCase

from apps.core.models import City, WeatherFact
from apps.core.tests.factories import WeatherFactFactory


class WeatherFactViewTestCase(APITestCase):
    path = "/core/weather"

    @staticmethod
    def get_expected_data(city, weather_fact):
        return {
            "city": {
                "name": city.name,
                "coords": city.coords,
                "district": city.district,
                "subject": city.subject,
                "population": city.population,
            },
            "temp": weather_fact.temp,
            "pressure_mm": weather_fact.pressure_mm,
            "wind_speed": weather_fact.wind_speed,
        }

    def test_city_not_found(self):
        city_name = "Moscow"

        response = self.client.get(f"{self.path}?city={city_name}")

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data, f"{city_name} not found")

    @Mocker()
    def test_no_weather_fact(self, request_mock):
        city = City.objects.first()
        lat, lon = city.coords.values()

        expected_json_data = {"fact": {"temp": 10, "pressure_mm": 890, "wind_speed": 5}}
        request_mock.get(
            f"https://api.weather.yandex.ru/v2/forecast?lat={lat}&lon={lon}",
            json=expected_json_data,
        )

        response = self.client.get(f"{self.path}?city={city.name}")

        weather_fact = WeatherFact.objects.get()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertDictEqual(
            response.json(), self.get_expected_data(city, weather_fact)
        )

    @Mocker()
    def test_not_actual_weather_fact(self, request_mock):
        weather_fact = WeatherFactFactory()
        city = weather_fact.city
        lat, lon = city.coords.values()

        past_time = timezone.now() - timezone.timedelta(minutes=40)
        WeatherFact.objects.filter(id=weather_fact.id).update(updated_at=past_time)
        weather_fact.refresh_from_db()

        expected_json_data = {"fact": {"temp": 1, "pressure_mm": 890, "wind_speed": 5}}
        request_mock.get(
            f"https://api.weather.yandex.ru/v2/forecast?lat={lat}&lon={lon}",
            json=expected_json_data,
        )

        response = self.client.get(f"{self.path}?city={city.name}")
        weather_fact.refresh_from_db()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertNotEqual(weather_fact.updated_at, past_time)
        self.assertDictEqual(
            {
                "fact": {
                    "temp": weather_fact.temp,
                    "pressure_mm": weather_fact.pressure_mm,
                    "wind_speed": weather_fact.wind_speed,
                }
            },
            expected_json_data,
        )
        self.assertDictEqual(
            response.json(), self.get_expected_data(city, weather_fact)
        )

    def test_actual_weather_fact(self):
        weather_fact = WeatherFactFactory()
        city = weather_fact.city

        response = self.client.get(f"{self.path}?city={city.name}")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertDictEqual(
            response.json(), self.get_expected_data(city, weather_fact)
        )
