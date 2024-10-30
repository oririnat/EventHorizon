import sys
sys.path.insert(0, '../services_utils')
from consumer import Consumer
from apscheduler.schedulers.blocking import BlockingScheduler
from models import Base
from db import engine


if __name__ == "__main__":
    print("Starting Event Processor Service.")

    # Create tables if they don't exist
    Base.metadata.create_all(bind=engine)
    print("Database tables created or verified existing.")

    consumer = Consumer()

    try:
        consumer.start_consuming()
    except KeyboardInterrupt:
        print("Stopping Event Processor Service.")
        consumer.close()
        exit(0)
