# info-weather
A project to get weather conditions for a certain city.  
Stack: Python, Django, DRF, PostgeSQL, Docker, Linters&formatter.


## Start a new project:

Image for the django_app container is build from Dockerfile.

Containers up:

```
docker-compose up -d
```

Get in to the django_app container Shell:

```
docker-compose run --rm django_app /bin/bash
```

Add to .env file your yandex-weather api key (test tariff):

```
sed -i '' 's/YANDEX_KEY = "fake-yandex-api-key"/YANDEX_KEY = "your-yandex-api-key"/g' .env
```

Make migrations:

```
python manage.py makemigrations
python manage.py migrate
```

A project is self-documented, 
to view all the endpoints and their descriptions, go to the url:

```
http://localhost:8080/core/swagger/
```

## Launching telegram bot:

A project implements a telegram bot (t.me/iforecaster_bot), 
which can issue a weather forecast for the selected city.


Add to .env file your telegram api key (test tariff):

```
sed -i '' 's/TELEGRAM_TOKEN = "fake-tg-bot-token"/TELEGRAM_TOKEN = "your-tg-bot-token"/g' .env
```

Instructions for local startup:
```
docker-compose run --rm django_app /bin/bash
```

```
python manage.py telegram_bot
```


## The project uses utilities to verify compliance with standards and code quality requirements:

Instructions for local startup:

```
docker-compose run --rm django_app /bin/bash
```

Running a check using isort, black, flake8 and pylint:
```
python -m nox
```

Running auto-formatting using isort and black:
```
python -m nox -k format_task
```
