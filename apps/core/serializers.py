from rest_framework import serializers

from apps.core.models import City, WeatherFact


class CitySerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = ("name", "coords", "district", "subject", "population")


class WeatherFactSerializer(serializers.ModelSerializer):
    city = CitySerializer()

    class Meta:
        model = WeatherFact
        fields = ("city", "temp", "pressure_mm", "wind_speed")
