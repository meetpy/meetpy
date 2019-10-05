FROM python:3.7.4


RUN mkdir /opt/meetpy
RUN mkdir /etc/supervisor
RUN mkdir /var/log/supervisor
RUN mkdir /var/run/supervisor

WORKDIR /opt/meetpy

ADD requirements/ /opt/meetpy/requirements
RUN ls /opt/meetpy

RUN pip install --no-cache-dir --requirement requirements/production.txt

ADD meetpy/ /opt/meetpy/meetpy
COPY ./deploy/supervisord/meetpy.ini /etc/supervisor/supervisord.d/meetpy.ini
COPY ./deploy/supervisord/supervisord.conf /etc/supervisor/supervisord.conf

CMD ["supervisord"]
