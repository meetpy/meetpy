FROM python:3.13

RUN mkdir /opt/meetpy

WORKDIR /opt/meetpy

ADD requirements.txt /opt/meetpy/requirement.txt

RUN pip install --no-cache-dir --requirement requirements.txt

ADD meetpy/ /opt/meetpy/meetpy

RUN cd meetpy && python manage.py collectstatic --no-input

WORKDIR /opt/meetpy/meetpy

CMD ["gunicorn", "-t", "30", "meetpy.wsgi", "-b", "127.0.0.1:8000"]
