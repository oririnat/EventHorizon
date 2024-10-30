import pika
import json
from config import (
    RABBITMQ_HOST,
    RABBITMQ_PORT,
    RABBITMQ_QUEUE,
    RABBITMQ_USER,
    RABBITMQ_PASSWORD
)

import sys
sys.path.insert(0, '../services_utils')
from db import SessionLocal
from models import Event, Actor, Repository
from sqlalchemy.exc import IntegrityError
from datetime import datetime
import time
from datetime import datetime
import threading
import requests

curr_number_of_events_processed = 0
curr_number_of_events_already_exists = 0

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

        # Declare the queue if not exists
        self.channel.queue_declare(queue=RABBITMQ_QUEUE, durable=True)

        # Set up prefetch to handle one message at a time
        self.channel.basic_qos(prefetch_count=1)

        threading.Thread(target=log_curr_number_of_events_processed).start()


    def start_consuming(self):
        self.channel.basic_consume(
            queue=RABBITMQ_QUEUE,
            on_message_callback=self.callback
        )
        print("Started consuming from the queue.")
        self.channel.start_consuming()

    def callback(self, ch, method, properties, body):
        global curr_number_of_events_processed

        session = SessionLocal()
        try:
            event_data = json.loads(body)
            self.process_message(session, event_data)
            session.commit()
            ch.basic_ack(delivery_tag=method.delivery_tag)
        
            curr_number_of_events_processed += 1

        except IntegrityError as e: 
            ch.basic_nack(delivery_tag=method.delivery_tag, requeue=False)
        except Exception as e:
            print(f"Error processing message.\n{e}")
            session.rollback()
            ch.basic_nack(delivery_tag=method.delivery_tag, requeue=False)
        finally:
            session.close()

    def process_message(self, session, event_data):
        global curr_number_of_events_already_exists
        # Check if event already exists
        existing_event = session.query(Event).filter_by(id=event_data['id']).first()
        if existing_event:
            curr_number_of_events_already_exists += 1
            return

        # Get or create actor
        actor = session.query(Actor).filter_by(id=event_data['actor_id']).first()
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
                # num_of_stars=self.fetch_repo_stars(event_data['repo_name'])
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

    def close(self):
        self.connection.close()

def log_curr_number_of_events_processed():
    global curr_number_of_events_processed
    global curr_number_of_events_already_exists
    
    while True:
        curr_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"{curr_time} - {curr_number_of_events_processed} events processed.")
        print(f"{curr_time} - {curr_number_of_events_already_exists} events already exist.")
        curr_number_of_events_processed = 0
        curr_number_of_events_already_exists = 0
        time.sleep(5)

