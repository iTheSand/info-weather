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
