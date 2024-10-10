import pika
from pika.exceptions import AMQPError
from config.config import Config
import logging


def setup_logging():
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s - %(levelname)s - %(message)s')
    logging.info("Logging is set up.")


def send_log_to_rabbitmq(log_message):
    rabbitmq_host = Config.RABBITMQ_URI

    connection = None
    try:
        connection = pika.BlockingConnection(
            pika.ConnectionParameters(rabbitmq_host)
        )
        channel = connection.channel()
        channel.queue_declare(queue='log_queue')
        channel.basic_publish(
            exchange='',
            routing_key='log_queue',
            body=log_message
        )
        print("Log sent to RabbitMQ successfully.")
    except AMQPError as e:
        print(f"Error in RabbitMQ connection or publication: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")
    finally:
        if connection:
            try:
                connection.close()
            except AMQPError as e:
                print(f"Error closing RabbitMQ connection: {e}")
