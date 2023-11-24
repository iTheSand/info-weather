from django.contrib import admin

from apps.core.models import City


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
