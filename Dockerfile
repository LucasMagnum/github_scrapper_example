FROM python:3.8-alpine

ENV PYTHONBUFFERED 1

RUN apk update \
  && apk add --virtual build-deps build-base gcc python3-dev musl-dev \
  && apk add libffi-dev py-cffi

COPY requirements.txt ./
RUN pip install -r requirements.txt

ENV PYTHONPATH "${PYTHONPATH}:/app/src/"
WORKDIR /app
