FROM python:3.8-alpine

RUN apk add --no-cache --virtual .build-deps gcc musl-dev

COPY requirements.txt /tmp/
RUN pip install -r /tmp/requirements.txt

RUN apk del --no-cache .build-deps

COPY run_flask.py /srv/run_flask.py
RUN mkdir -p /src
COPY src/ /src/
RUN pip install -e /src
COPY tests/ /tests

WORKDIR /srv
