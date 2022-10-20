FROM python:3.10.2-slim

ENV PYTHONUNBUFFERED 1
ENV PYTHONPATH /app

EXPOSE 8000
WORKDIR /app


RUN apt-get update && \
    apt-get install -y --no-install-recommends netcat && \
    rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

COPY pyproject.toml ./
RUN pip install poetry  && poetry install --without dev,test

COPY . ./

CMD poetry run uvicorn --host=0.0.0.0 main:app --reload