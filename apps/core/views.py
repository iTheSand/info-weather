import logging

from django.utils import timezone
from django.utils.decorators import method_decorator
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_404_NOT_FOUND
from rest_framework.views import APIView

from apps.core import docs
from apps.core.models import City, WeatherFact, WeatherForecast
from apps.core.serializers import (
    ForecastPartSerializer,
    ForecastPartsSerializer,
    WeatherFactSerializer,
    WeatherForecastSerializer,
)
from apps.external_api.weather_yandex import get_weather

logger = logging.getLogger("django")


@method_decorator(name="get", decorator=docs.WEATHER_FACT_OR_FORECAST_VIEW_GET_SCHEMA)
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

        weather_fact = self.model.objects.filter(
            city=city, updated_at__gte=timezone.now() - timezone.timedelta(minutes=30)
        ).first()

        if not weather_fact:
            fact_data = get_weather(**city.coords).get("fact")
            weather_fact, _ = self.model.objects.update_or_create(
                city=city,
                defaults={
                    "temp": fact_data["temp"],
                    "pressure_mm": fact_data["pressure_mm"],
                    "wind_speed": fact_data["wind_speed"],
                },
            )

        return Response(self.serializer_class(weather_fact).data, status=HTTP_200_OK)


@method_decorator(name="get", decorator=docs.WEATHER_FACT_OR_FORECAST_VIEW_GET_SCHEMA)
class WeatherForecastView(APIView):
    model = WeatherForecast

    def get(self, request):
        city_name = request.query_params.get("city").capitalize()
        city = City.objects.filter(name=city_name).first()

        if not city:
            data = f"{city_name} not found"
            logger.error(
                {
                    "Get weather forecast request": {
                        "response_status_code": HTTP_404_NOT_FOUND,
                        "response_body": data,
                    }
                }
            )
            return Response(data, status=HTTP_404_NOT_FOUND)

        today_date = timezone.now().strftime("%Y-%m-%d")

        if not self.model.objects.filter(city=city, date=today_date).exists():
            forecasts_data = get_weather(**city.coords).get("forecasts")
            for forecast_data in forecasts_data:
                weather_forecast_serializer = WeatherForecastSerializer(
                    data=forecast_data
                )
                weather_forecast_serializer.is_valid()
                weather_forecast = weather_forecast_serializer.save(city=city)

                forecast_part_serializer = ForecastPartSerializer(
                    data=[
                        {"part_name": key, **forecast_data["parts"][key]}
                        for key in ("night", "morning", "day", "evening")
                    ],
                    many=True,
                )

                forecast_part_serializer.is_valid()
                forecast_part_serializer.save(weather_forecast=weather_forecast)

        weather_forecast = self.model.objects.get(city=city, date=today_date)

        return Response(
            ForecastPartsSerializer(weather_forecast).data, status=HTTP_200_OK
        )
