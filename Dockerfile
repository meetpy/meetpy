FROM python:3.6

WORKDIR /usr/src/app
COPY requirements/ /usr/src/app/requirements/

RUN pip install --no-cache-dir --requirement requirements/production.txt

ENV DJANGO_SETTINGS_MODULE="meetpy.settings.docker"

EXPOSE 8000

COPY . /usr/src/app/
WORKDIR meetpy
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
