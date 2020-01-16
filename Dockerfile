FROM python:3.8-alpine

RUN apk add --no-cache --virtual .build-deps gcc postgresql-dev musl-dev python3-dev

COPY requirements.txt /tmp/
RUN pip install -r /tmp/requirements.txt

RUN mkdir -p /src
COPY . /src/

WORKDIR /src
