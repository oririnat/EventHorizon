from apscheduler.schedulers.blocking import BlockingScheduler
from fetcher import EventFetcher
from config import POLL_INTERVAL_SECONDS
from transformer import Transformer
from publisher import Publisher
import logging

def job():
    fetcher = EventFetcher()
    transformer = Transformer()
    publisher = Publisher()

    try:
        raw_events = fetcher.run()
        if raw_events:
            transformed_events = transformer.transform(raw_events)
            publisher.publish_events(transformed_events)
            print(f"Published {len(transformed_events)} events to RabbitMQ.")
        else:
            print("No new events to process.")
    except Exception as e:
        logging.exception("Error occurred during event processing.")
    finally:
        publisher.close()

if __name__ == "__main__":
    job()
    # scheduler = BlockingScheduler()
    # scheduler.add_job(job, 'interval', seconds=POLL_INTERVAL_SECONDS)
    # print("Event Fetcher Service started. Press Ctrl+C to exit.")
    # try:
    #     scheduler.start()
    # except (KeyboardInterrupt, SystemExit):
    #     print("Event Fetcher Service stopped.")
