import logging

from django.utils import timezone
from django.utils.decorators import method_decorator
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_404_NOT_FOUND
from rest_framework.views import APIView

from apps.core import docs
from apps.core.models import City, WeatherFact
from apps.core.serializers import WeatherFactSerializer
from apps.external_api.weather_yandex import get_weather

logger = logging.getLogger("django")


@method_decorator(name="get", decorator=docs.WEATHER_FACT_VIEW_GET_SCHEMA)
class WeatherFactView(APIView):
    model = WeatherFact
    serializer_class = WeatherFactSerializer

    def get(self, request):
        city_name = request.query_params.get("city").capitalize()
        city = City.objects.filter(name=city_name).first()

        if not city:
            data = f"{city_name} not found"
            logger.error(
                {
                    "Get weather fact request": {
                        "response_status_code": HTTP_404_NOT_FOUND,
                        "response_body": data,
                    }
                }
            )
            return Response(data, status=HTTP_404_NOT_FOUND)

        weather_fact = WeatherFact.objects.filter(
            city=city, updated_at__gte=timezone.now() - timezone.timedelta(minutes=30)
        ).first()

        if not weather_fact:
            fact_data = get_weather(**city.coords).get("fact")
            weather_fact, _ = WeatherFact.objects.update_or_create(
                city=city,
                defaults={
                    "temp": fact_data["temp"],
                    "pressure_mm": fact_data["pressure_mm"],
                    "wind_speed": fact_data["wind_speed"],
                },
            )

        return Response(self.serializer_class(weather_fact).data, status=HTTP_200_OK)
