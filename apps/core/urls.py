from django.conf.urls import url
from django.urls import path

from apps.core.swagger import SchemaView
from apps.core.views import WeatherFactView

app_name = "core"

urlpatterns = [path("weather/", WeatherFactView.as_view(), name="weather")]

urlpatterns.extend(
    [
        url(
            r"^swagger(?P<format>\.json|\.yaml)$",
            SchemaView.without_ui(cache_timeout=0),
            name="schema-json",
        ),
        url(
            r"^swagger/$",
            SchemaView.with_ui("swagger", cache_timeout=0),
            name="schema-swagger-ui",
        ),
        url(
            r"^doc/$", SchemaView.with_ui("redoc", cache_timeout=0), name="schema-redoc"
        ),
    ]
)
