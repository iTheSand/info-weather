from rest_framework import serializers

from apps.core.models import City, ForecastPart, WeatherFact, WeatherForecast


class CitySerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = ("name", "coords", "district", "subject", "population")


class WeatherFactSerializer(serializers.ModelSerializer):
    city = CitySerializer()

    class Meta:
        model = WeatherFact
        fields = ("city", "temp", "pressure_mm", "wind_speed")


class WeatherForecastSerializer(serializers.ModelSerializer):
    class Meta:
        model = WeatherForecast
        fields = ("date", "date_ts")


class ForecastPartSerializer(serializers.ModelSerializer):
    wind_speed = serializers.FloatField()

    class Meta:
        model = ForecastPart
        fields = (
            "part_name",
            "temp_min",
            "temp_max",
            "temp_avg",
            "feels_like",
            "condition",
            "wind_speed",
            "pressure_mm",
            "humidity",
        )


class ForecastPartsSerializer(serializers.ModelSerializer):
    city = serializers.SerializerMethodField()
    weather_forecast = serializers.SerializerMethodField()
    forecast_parts = ForecastPartSerializer(many=True)

    @staticmethod
    def get_city(obj):
        return obj.city.name

    @staticmethod
    def get_weather_forecast(obj):
        return WeatherForecastSerializer(obj).data

    class Meta:
        model = WeatherForecast
        fields = ("city", "weather_forecast", "forecast_parts")
