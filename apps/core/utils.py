from drf_yasg.generators import OpenAPISchemaGenerator


class BothHttpAndHttpsSchemaGenerator(OpenAPISchemaGenerator):
    def get_schema(self, request=None, public=False):
        schema = super().get_schema(request, public)
        schema.schemes = ["http", "https"]
        return schema


def convert_condition(condition):
    conditions = {
        "clear": "ясно",
        "partly-cloudy": "малооблачно",
        "cloudy": "облачно с прояснениями",
        "overcast": "пасмурно",
        "light-rain": "небольшой дождь",
        "rain": "дождь",
        "heavy-rain": "сильный дождь",
        "showers": "ливень",
        "wet-snow": "дождь со снегом",
        "light-snow": "небольшой снег",
        "snow": "снег",
        "snow-showers": "снегопад",
        "hail": "град",
        "thunderstorm": "гроза",
        "thunderstorm-with-rain": "дождь с грозой",
        "thunderstorm-with-hail": "гроза с градом",
    }

    return conditions.get(condition, "неопределены")


def convert_time_of_day(time_of_day):
    times_of_day = {
        "night": "Ночью",
        "morning": "Утром",
        "day": "Днем",
        "evening": "Вечером",
    }

    return times_of_day.get(time_of_day)


def convert_json_to_str(data):
    return (
        f"Прогноз погоды для города {data['city_name']} на {data['forecast_date']}:\n\n"
        + "\n".join(
            [
                f"{convert_time_of_day(part['part_name'])}: "
                f"Температура: от {part['temp_min']}°C до {part['temp_max']}°C, "
                f"Ощущается как: {part['feels_like']}°C, "
                f"Погодные условия: {convert_condition(part['condition'])}, "
                f"Скорость ветра: {part['wind_speed']} м/с, "
                f"Давление: {part['pressure_mm']} мм рт. ст., "
                f"Влажность: {part['humidity']}%\n"
                for part in data["forecast_parts"]
            ]
        )
    )
