from django.db import models


class City(models.Model):
    name = models.CharField(verbose_name="Name", max_length=255)
    coords = models.JSONField(verbose_name="Coords", default=dict)
    district = models.CharField(verbose_name="District", max_length=255)
    subject = models.CharField(verbose_name="Subject", max_length=255)
    population = models.IntegerField(verbose_name="Population")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "City"
        verbose_name_plural = "Cities"
        unique_together = ("name", "subject")


class WeatherFact(models.Model):
    city = models.OneToOneField(
        City, verbose_name="City", related_name="weather_fact", on_delete=models.CASCADE
    )

    temp = models.SmallIntegerField(verbose_name="Temperature (C°)")
    pressure_mm = models.SmallIntegerField(verbose_name="Pressure (mm Hg)")
    wind_speed = models.SmallIntegerField(verbose_name="Wind speed (m/s)")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Fact for {self.city} updated: {self.updated_at}"

    class Meta:
        verbose_name = "Weather fact"
        verbose_name_plural = "Weather facts"


class WeatherForecast(models.Model):
    city = models.ForeignKey(
        City,
        verbose_name="City",
        related_name="weather_forecasts",
        on_delete=models.CASCADE,
    )

    date = models.CharField(verbose_name="Date", max_length=100)
    date_ts = models.IntegerField(verbose_name="Date TS")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Forecast for {self.city} updated: {self.updated_at}"

    class Meta:
        verbose_name = "Weather forecast"
        verbose_name_plural = "Weather forecasts"


class ForecastPart(models.Model):
    weather_forecast = models.ForeignKey(
        WeatherForecast,
        verbose_name="Weather forecast",
        related_name="forecast_parts",
        on_delete=models.CASCADE,
    )

    part_name = models.CharField(verbose_name="Part name", max_length=100)
    temp_min = models.SmallIntegerField(verbose_name="Temperature min (C°)")
    temp_max = models.SmallIntegerField(verbose_name="Temperature max (C°)")
    temp_avg = models.SmallIntegerField(verbose_name="Temperature avg (C°)")
    feels_like = models.SmallIntegerField(verbose_name="Feels like (C°)")
    condition = models.CharField(verbose_name="Condition", max_length=100)
    wind_speed = models.SmallIntegerField(verbose_name="Wind speed (m/s)")
    pressure_mm = models.SmallIntegerField(verbose_name="Pressure (mm Hg)")
    humidity = models.SmallIntegerField(verbose_name="Humidity (%)")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.weather_forecast.date} - {self.part_name}"

    class Meta:
        verbose_name = "Forecast part"
        verbose_name_plural = "Forecast parts"
