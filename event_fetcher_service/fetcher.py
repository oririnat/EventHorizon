import requests
import time
from config import GITHUB_API_URL, GITHUB_AUTH_TOKEN, GITHUB_API_VERSION, GITHUB_ACCEPT
from rate_limiter import RateLimiter

class EventFetcher:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({"Authorization": f"token {GITHUB_AUTH_TOKEN}"})
        self.session.headers.update({"Accept": GITHUB_ACCEPT})
        self.session.headers.update({"X-GitHub-Api-Version": GITHUB_API_VERSION})

        self.rate_limiter = RateLimiter()
        self.last_event_id = self.load_last_event_id()

    def load_last_event_id(self):
        # Implement loading from persistent storage
        try:
            with open("last_event_id.txt", "r") as f:
                return f.read().strip()
        except FileNotFoundError:
            return None

    def save_last_event_id(self, event_id):
        # Implement saving to persistent storage
        with open("last_event_id.txt", "w") as f:
            f.write(event_id)

    def fetch_events(self):
        events = []
        page = 1
        while True:
            if self.rate_limiter.should_wait():
                wait_time = self.rate_limiter.reset_time - int(time.time()) + 1
                print(f"Rate limit exceeded. Waiting for {wait_time} seconds.")
                time.sleep(wait_time)

            response = self.session.get(GITHUB_API_URL, params={"per_page": 100, "page": page})
            self.rate_limiter.update(response.headers)

            if response.status_code == 422:
                # If we request a page that doesn't exist, we should stop
                break

            if response.status_code != 200:
                print(f"Error fetching events: {response.status_code}")
                break

            page_events = response.json()
            if not page_events:
                break

            for event in page_events:
                if event["id"] == self.last_event_id:
                    # All new events have been collected
                    return events
                events.append(event)

            # If the last event ID was not found, continue to next page
            page += 1

        return events

    def run(self):
        new_events = self.fetch_events()
        if new_events:
            # Update last_event_id with the most recent event
            self.last_event_id = new_events[0]["id"]
            self.save_last_event_id(self.last_event_id)
        return new_events
