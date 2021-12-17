FROM python:3.8

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN pip install --upgrade pip

COPY ./requirements.txt .

RUN pip install --default-timeout=100 -r requirements.txt

COPY . /app


WORKDIR /app

