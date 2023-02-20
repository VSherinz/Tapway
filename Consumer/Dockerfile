FROM python:3.11-slim-buster

RUN mkdir -p app/Consumer/src
RUN mkdir tmp/Consumer
WORKDIR /app

ENV PATH="${PATH}:/root/.local/bin"
ENV PYTHONPATH=.

COPY requirements.txt .

RUN pip3 install -r requirements.txt

COPY ./src ./Consumer/src

ENTRYPOINT ["python3"]

CMD ["./Consumer/src/main.py"]
