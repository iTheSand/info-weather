from rest_framework import serializers

from apps.core.models import City


class CitySerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = ("id", "name", "coords", "district", "subject", "population")
