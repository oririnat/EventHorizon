import pika
import json
from config import (
    RABBITMQ_HOST,
    RABBITMQ_PORT,
    RABBITMQ_QUEUE,
    RABBITMQ_USER,
    RABBITMQ_PASSWORD,
)

class Publisher:
    def __init__(self):
        # Create credentials object
        credentials = pika.PlainCredentials(RABBITMQ_USER, RABBITMQ_PASSWORD)

        # Establish connection parameters to RabbitMQ, including credentials
        connection_params = pika.ConnectionParameters(
            host=RABBITMQ_HOST,
            port=RABBITMQ_PORT,
            credentials=credentials
        )

        self.connection = pika.BlockingConnection(connection_params)
        self.channel = self.connection.channel()

        # Declare the queue
        self.channel.queue_declare(queue=RABBITMQ_QUEUE, durable=True)

    def publish_events(self, events):
        for event in events:
            self.channel.basic_publish(
                exchange='',
                routing_key=RABBITMQ_QUEUE,
                body=json.dumps(event),
                properties=pika.BasicProperties(
                    delivery_mode=2,  # 2 is the code for persistent means messages are lost on RabbitMQ restart. 1 is non-persistent.
                )
            )

    def close(self):
        self.connection.close()
