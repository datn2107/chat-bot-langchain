FROM python:3.11-alpine3.17

COPY requirements.txt /app
WORKDIR /app

RUN pip install -r requirements.txt
