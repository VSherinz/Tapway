import logging
import logging.config
import os
import sys

import pika
import yaml
from fastapi import FastAPI

from Producer.src.models.FootageBody import Footage

app = FastAPI()


def init_log() -> None:
    """
    Load Logging Configuration
    :return:
    """

    print("Initiating Producer Logger")
    try:
        with open('Producer/src/logging.yaml', 'rt') as f:
            config = yaml.safe_load(f.read())
            logging.config.dictConfig(config)
            print("Logger initiation successful")
    except Exception as e:
        print('Error initiating Producer log', sys.exc_info())


@app.post("/push")
async def push_footage(footage: Footage):
    """
    Validate Footage data via Pydantic.
    On success, proceed form the desired input
    for Queue to be consumed by Consumer
    :param footage:
    :return:
    """

    logger.info("Push Message Received")
    for predicate in footage.data.preds:
        if predicate.prob < 0.25:
            predicate.tags.append("low_prob")

    await create_mq_channel(footage.json())

    return {"message": "Ok"}


async def create_mq_channel(body: str | bytes):
    """
    Responsible for creation/initiation of MQ Channel via Pika library
    :param body:
    :return:
    """

    logger.debug(f"Sending message to channel:\n{body}")
    try:
        with pika.BlockingConnection(pika.ConnectionParameters(
                host='queue', credentials=pika.PlainCredentials("myuser", "mypassword"))) as connection:
            channel = connection.channel()
            channel.queue_declare(queue='footage_queue', durable=True)
            channel.basic_publish(
                exchange='',
                routing_key='footage_queue',
                body=body,
                properties=pika.BasicProperties(
                    delivery_mode=2,  # make message persistent
                ))

            logger.info("Message sent")
    except Exception as e:
        logger.exception("Error creating Producer Pika channel")

    return " [x] Sent: %s" % body


init_log()
log_path = os.environ["LOG"]
logger = logging.getLogger(log_path)
