import sys
from sqlalchemy import inspect  # Import the inspector to check table existence

sys.path.insert(0, '../services_utils')
from consumer import Consumer
from apscheduler.schedulers.blocking import BlockingScheduler
from models import Base
from db import engine

if __name__ == "__main__":
    print("Starting Event Processor Service.")

    # Check if tables exist before creating them
    inspector = inspect(engine)
    if not inspector.has_table("events"):  # Replace "events" with the name of any table to check
        print("Creating missing tables...")
        Base.metadata.create_all(bind=engine)
        print("Database tables created.")
    else:
        print("Database tables already exist. Skipping creation.")

    consumer = Consumer()

    try:
        consumer.start_consuming()
    except KeyboardInterrupt:
        print("Stopping Event Processor Service.")
        consumer.close()
        exit(0)
