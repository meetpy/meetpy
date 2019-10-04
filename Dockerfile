FROM python:3.6

COPY . /usr/src/app/
WORKDIR /usr/src/app

RUN pip install --no-cache-dir --requirement requirements/production.txt

ENV DJANGO_SETTINGS_MODULE="meetpy.settings.docker"

EXPOSE 8000

WORKDIR meetpy
CMD python ./manage.py runserver
