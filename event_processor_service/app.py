import logging
from consumer import Consumer
from models import Base
from db import engine
from config import DATABASE_NAME

if __name__ == "__main__":
    logging.basicConfig(
        filename='event_processor.log',
        level=logging.INFO,
        format='%(asctime)s:%(levelname)s:%(name)s:%(message)s'
    )
    logging.info("Starting Event Processor Service.")

    # Create tables if they don't exist
    Base.metadata.create_all(bind=engine)
    logging.info("Database tables created or verified existing.")
    
    consumer = Consumer()
    try:
        consumer.start_consuming()
    except KeyboardInterrupt:
        logging.info("Stopping Event Processor Service.")
        consumer.close()
