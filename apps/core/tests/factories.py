# pylint: disable=consider-using-f-string

from django.utils import timezone
from factory import Sequence, SubFactory
from factory.django import DjangoModelFactory

from apps.core.models import City, ForecastPart, WeatherFact, WeatherForecast


class CityFactory(DjangoModelFactory):
    class Meta:
        model = City

    name = Sequence("Test_city_{}".format)
    coords = {"lat": "59.56667", "lon": "150.8"}
    district = Sequence("test_district_{}".format)
    subject = Sequence("test_subject_{}".format)
    population = Sequence(lambda n: 90000 + 900 * n)


class WeatherFactFactory(DjangoModelFactory):
    class Meta:
        model = WeatherFact

    city = SubFactory(CityFactory)
    temp = Sequence(lambda n: 10 + n)
    pressure_mm = Sequence(lambda n: 900 + 10 * n)
    wind_speed = Sequence(lambda n: 5 + n)


class WeatherForecastFactory(DjangoModelFactory):
    class Meta:
        model = WeatherForecast

    city = SubFactory(CityFactory)
    date = timezone.now()
    data_ts = timezone.now().timestamp()


class ForecastPartFactory(DjangoModelFactory):
    class Meta:
        model = ForecastPart

    part_name = Sequence("test_part_name_{}".format)
    temp_min = Sequence(lambda n: 6 + n)
    temp_max = Sequence(lambda n: 12 + n)
    temp_avg = Sequence(lambda n: 9 + n)
    feels_like = Sequence(lambda n: 10 + n)
    condition = Sequence("test_condition_{}".format)
    wind_speed = Sequence(lambda n: 5 + n)
    pressure_mm = Sequence(lambda n: 900 + 10 * n)
    humidity = Sequence(lambda n: 30 + n)
