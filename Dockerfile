FROM ghcr.io/binkhq/python:3.10 AS build

WORKDIR /app

ADD . .

RUN pip install poetry==1.2.0b3
RUN poetry config virtualenvs.create false

RUN poetry install && apt-get update

CMD ["python", "app.py"]