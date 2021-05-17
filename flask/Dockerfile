# syntax=docker/dockerfile:1

FROM python:3.8

WORKDIR /app

ADD . /app

RUN pip install -r requirements.txt

CMD ["uwsgi", "app.ini"]

