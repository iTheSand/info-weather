# info-weather
A project to get weather conditions for a certain city

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
