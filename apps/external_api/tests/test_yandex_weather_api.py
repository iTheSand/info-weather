from django.test import TestCase
from requests_mock import Mocker

from apps.core.models import City
from apps.external_api.weather_yandex import get_weather


class YandexWeatherApiTestCase(TestCase):
    @Mocker()
    def test_success(self, request_mock):
        city = City.objects.first()
        lat, lon = city.coords.values()

        expected_json_data = {"fact": {"temp": 10, "pressure_mm": 890, "wind_speed": 5}}
        request_mock.get(
            f"https://api.weather.yandex.ru/v2/forecast?lat={lat}&lon={lon}",
            json=expected_json_data,
        )

        self.assertDictEqual(expected_json_data, get_weather(lat=lat, lon=lon))
