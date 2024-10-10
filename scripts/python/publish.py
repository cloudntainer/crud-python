import pika


def publish_log(
        message
):
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(
            'localhost'
        )
    )
    channel = pika.BlockingConnection(
    )
    channel.exchange_declare(
        exchange='logs', exchange_type='fanout'
    )

    channel.basic_publish(
        exchange='logs', routing_key='', body=message
    )
    connection.close(
    )


publish_log('Publishing Log...')
