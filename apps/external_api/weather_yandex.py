import logging

from django.conf import settings
from requests import request

logger = logging.getLogger("django")


def get_weather(lat=None, lon=None):
    response = request(
        "GET",
        f"https://api.weather.yandex.ru/v2/forecast?lat={lat}&lon={lon}",
        headers={"X-Yandex-API-Key": settings.YANDEX_KEY},
    )
    response_body = response.json()

    logger.info(
        {
            "Get weather request": {
                "response_status_code": response.status_code,
                "response_body": response_body,
            }
        }
    )

    return response_body
