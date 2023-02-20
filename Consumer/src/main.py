import csv
import json
import logging
import logging.config
import os
import sys
import time

import pandas as pd
import pika
import yaml

sleepTime = 20
print(' [*] Sleeping for ', sleepTime, ' seconds.')
time.sleep(sleepTime)


def init_log() -> None:
    """
    Load Logging Configuration
    :return:
    """

    print("Initiating Consumer Logger")
    try:
        with open('./Consumer/src/logging.yaml', 'r') as f:
            config = yaml.safe_load(f.read())
            logging.config.dictConfig(config)
            print("Logger initiation successful")
    except Exception as e:
        print('Error initiating Consumer log', sys.exc_info())


def write_to_csv(footages: list[dict]) -> bool:
    """
    Write many footage data into csv
    :param footages: list[dict]
    :return:
    """
    pass


def write_to_csv(footage: dict) -> bool:
    """
    Write footage data into csv
    :param footage: dict
    :return:
    """

    logger.info("Writing footage data into csv")
    headers, datas = footage["data"]["preds"][0].keys(), footage["data"]["preds"]
    logger.debug(f"headers is: \n{headers}\n\n")
    logger.debug(f"datas is: \n{datas}\n\n")

    try:
        is_header_necessary = not os.path.isfile("output.csv")
        if os.path.isfile("output.csv"):
            df = pd.read_csv("output.csv")
            is_header_necessary = len(df.index) == 0

        with open("output.csv", "a", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=headers)
            if is_header_necessary:
                print("csv is empty")
                writer.writeheader()

            writer.writerows(datas)

    except Exception as e:
        logger.exception("Fail to write into csv")

    logger.info("Successfully written footage data into csv")
    return True


def callback(ch, method, properties, body: bytes):
    """
    Will be triggered upon availability of messages in footage_queue

    Will get the body, turn it into object for CSV-Creation purpose
    :param ch:
    :param method:
    :param properties:
    :param body: bytes
    :return:
    """
    logger.info("Message received from pika")
    logger.debug(f"Message received from pika:\n{body}")
    footage_str = body.decode()
    footage: dict = json.loads(footage_str)

    write_to_csv(footage)

    ch.basic_ack(delivery_tag=method.delivery_tag)


def create_mq_channel() -> None:
    """
    Establish MQ connection and channel to listen to
    :return:
    """

    try:
        logger.info("Initiating listening to Footage Queue channel")
        with pika.BlockingConnection(pika.ConnectionParameters(
                host='queue', credentials=pika.PlainCredentials("myuser", "mypassword"))) as connection:
            channel = connection.channel()
            channel.queue_declare(queue='footage_queue', durable=True)

            logger.info(' [*] Waiting for messages.')

            channel.basic_qos(prefetch_count=1)
            channel.basic_consume(queue='footage_queue', on_message_callback=callback)
            channel.start_consuming()

        logger.debug("Listening to Footage Queue channel")
    except Exception as e:
        logger.exception("Error creating Consumer Pika channel")


def main() -> None:
    logger.info("Connecting to Consumer")
    create_mq_channel()


init_log()
log_path = os.environ["LOG"]
logger = logging.getLogger(log_path)

if __name__ == '__main__':
    main()
