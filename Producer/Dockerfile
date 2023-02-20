# syntax=docker/dockerfile:1

FROM python:3.11-slim-buster

RUN mkdir -p app/Producer/src
RUN mkdir tmp/Producer
WORKDIR /app

ENV PATH="${PATH}:/root/.local/bin"
ENV PYTHONPATH=.

COPY requirements.txt .

RUN pip3 install -r requirements.txt

COPY ./src/ ./Producer/src