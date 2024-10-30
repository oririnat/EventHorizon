from apscheduler.schedulers.blocking import BlockingScheduler
from fetcher import EventFetcher
from config import POLL_INTERVAL_SECONDS
from transformer import Transformer
from publisher import Publisher

# Set to store the IDs of the events that have been processed
# This first try to prevent duplicate events from being published, but it's not foolproof
local_set_of_events_id = set()

fetcher = EventFetcher()
transformer = Transformer()
publisher = Publisher()

def job():
    try:
        raw_events = fetcher.run()
        if raw_events:
            transformed_events = transformer.transform(raw_events)

            # Filter out events that are already in the local set
            transformed_events = [event for event in transformed_events if event["id"] not in local_set_of_events_id]

            publisher.publish_events(transformed_events)
            print(f"Published {len(transformed_events)} events to RabbitMQ.")

        else:
            print("No new events to process.")
    except Exception as e:
        print("Error occurred during event processing.")
        

    
def reset_local_set_of_events_id():
    print("Resetting local set of events ID.")
    local_set_of_events_id.clear()

if __name__ == "__main__":
    scheduler = BlockingScheduler()
    scheduler.add_job(job, 'interval', seconds=POLL_INTERVAL_SECONDS)
    scheduler.add_job(reset_local_set_of_events_id, 'interval', minutes=1)

    print("Event Fetcher Service started. Press Ctrl+C to exit.")
    try:
        scheduler.start()
    except (KeyboardInterrupt, SystemExit):
        print("Event Fetcher Service stopped.")
    finally:
        publisher.close()

