from drf_yasg import openapi
from drf_yasg.openapi import Parameter
from drf_yasg.utils import swagger_auto_schema

WEATHER_FACT_OR_FORECAST_VIEW_GET_SCHEMA = swagger_auto_schema(
    manual_parameters=[
        Parameter("city", required=True, in_=openapi.IN_QUERY, type=openapi.TYPE_STRING)
    ]
)
