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

Make migrations:

```
python manage.py makemigrations
python manage.py migrate
```


## Launching telegram bot:

A project implements a telegram bot (t.me/iforecaster_bot), 
which can issue a weather forecast for the selected city.

Instructions for local startup:

```
docker-compose run --rm django_app /bin/bash
```

```
python manage.py iforecaster_bot
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
