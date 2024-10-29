import pika
import json
from config import (
    RABBITMQ_HOST,
    RABBITMQ_PORT,
    RABBITMQ_QUEUE,
    RABBITMQ_USER,
    RABBITMQ_PASSWORD
)
from db import SessionLocal
from models import Event, Actor, Repository
from sqlalchemy.exc import IntegrityError
import logging
from datetime import datetime

class Consumer:
    def __init__(self):
        credentials = pika.PlainCredentials(RABBITMQ_USER, RABBITMQ_PASSWORD)
        connection_params = pika.ConnectionParameters(
            host=RABBITMQ_HOST,
            port=RABBITMQ_PORT,
            credentials=credentials
        )
        self.connection = pika.BlockingConnection(connection_params)
        self.channel = self.connection.channel()

        # Declare the queue
        self.channel.queue_declare(queue=RABBITMQ_QUEUE, durable=True)

        # Set up prefetch to handle one message at a time
        self.channel.basic_qos(prefetch_count=1)

    def start_consuming(self):
        self.channel.basic_consume(
            queue=RABBITMQ_QUEUE,
            on_message_callback=self.callback
        )
        logging.info("Started consuming from the queue.")
        self.channel.start_consuming()

    def callback(self, ch, method, properties, body):
        session = SessionLocal()
        try:
            event_data = json.loads(body)
            print(f"Received message: {event_data}")
            self.process_message(session, event_data)
            session.commit()
            ch.basic_ack(delivery_tag=method.delivery_tag)
        except Exception as e:
            logging.exception("Error processing message.")
            session.rollback()
            ch.basic_nack(delivery_tag=method.delivery_tag, requeue=False)
        finally:
            session.close()

    def process_message(self, session, event_data):
        # Check if event already exists
        existing_event = session.query(Event).filter_by(id=event_data['id']).first()
        if existing_event:
            logging.info(f"Event {event_data['id']} already exists. Skipping.")
            return

        # Get or create actor
        actor = session.query(Actor).filter_by(login=event_data['actor_login']).first()
        if not actor:
            actor = Actor(
                id=event_data['actor_id'],
                login=event_data['actor_login'],
                avatar_url=event_data.get('actor_avatar_url')
            )
            session.add(actor)

        # Get or create repository
        repository = session.query(Repository).filter_by(id=event_data['repo_id']).first()
        if not repository:
            repository = Repository(
                id=event_data['repo_id'],
                name=event_data['repo_name'],
            )
            session.add(repository)

        # Create event
        event = Event(
            id=event_data['id'],
            type=event_data['type'],
            actor=actor,
            repository=repository,
            created_at=datetime.strptime(event_data['created_at'], '%Y-%m-%dT%H:%M:%SZ')
        )
        session.add(event)
        logging.info(f"Inserted event {event_data['id']} into the database.")

    def close(self):
        self.connection.close()
