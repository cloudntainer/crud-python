import pika
from config.config import Config

def parse_rabbitmq_url():
    url = Config.RABBITMQ_URI

    connection_params = pika.URLParameters(url)
    
    connection = pika.BlockingConnection(connection_params)
    channel = connection.channel()
    
    return url
