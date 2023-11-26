from django.contrib import admin

from apps.core.models import City, ForecastPart, WeatherFact, WeatherForecast


class FirstLetterFilter(admin.SimpleListFilter):
    title = "First letter"
    parameter_name = "first_letter"

    def lookups(self, request, model_admin):
        russian_alphabet = [chr(i) for i in range(ord("А"), ord("Я") + 1)]
        return [(letter, letter) for letter in russian_alphabet]

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(name__istartswith=self.value())
        return queryset


@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    list_display = ("name", "coords", "district", "subject", "population")
    ordering = ("name",)
    readonly_fields = ("created_at", "updated_at")
    list_filter = (FirstLetterFilter,)


@admin.register(WeatherFact)
class WeatherFactAdmin(admin.ModelAdmin):
    list_display = (
        "city",
        "temp",
        "pressure_mm",
        "wind_speed",
        "created_at",
        "updated_at",
    )
    ordering = ("city",)
    readonly_fields = ("created_at", "updated_at")


@admin.register(WeatherForecast)
class WeatherForecastAdmin(admin.ModelAdmin):
    list_display = ("city", "date", "created_at", "updated_at")
    ordering = ("city", "date")
    readonly_fields = ("created_at", "updated_at")


@admin.register(ForecastPart)
class ForecastPartAdmin(admin.ModelAdmin):
    list_display = (
        "part_name",
        "temp_max",
        "temp_avg",
        "feels_like",
        "condition",
        "wind_speed",
        "pressure_mm",
        "weather_forecast",
    )
    ordering = ("weather_forecast",)
    list_filter = ("weather_forecast__date",)
    readonly_fields = ("created_at", "updated_at")
