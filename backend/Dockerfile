FROM python:3.10-slim-buster

WORKDIR /app

RUN apt-get update \
    && apt-get install -y libpq-dev \
    && apt-get install -y gcc

COPY ./requirements.txt .

RUN pip install -r requirements.txt

COPY . .

RUN chmod +x docker-entrypoint.sh

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV COLUMNS=164
