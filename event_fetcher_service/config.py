import os
from dotenv import load_dotenv

load_dotenv()

GITHUB_API_URL = "https://api.github.com/events"
GITHUB_AUTH_TOKEN = os.getenv("GITHUB_AUTH_TOKEN")
GITHUB_ACCEPT = os.getenv("GITHUB_ACCEPT", "application/vnd.github+json")
GITHUB_API_VERSION = os.getenv("GITHUB_API_VERSION", "2022-11-28")
POLL_INTERVAL_SECONDS = int(os.getenv("POLL_INTERVAL_SECONDS", 2))
RABBITMQ_HOST = os.getenv("RABBITMQ_HOST", "localhost")
RABBITMQ_PORT = int(os.getenv("RABBITMQ_PORT", 5672))
RABBITMQ_QUEUE = os.getenv("RABBITMQ_QUEUE", "github_events")
RABBITMQ_USER = os.getenv("RABBITMQ_USER", "user")
RABBITMQ_PASSWORD = os.getenv("RABBITMQ_PASSWORD", "password")
LAST_EVENT_ID_FILE = os.getenv("LAST_EVENT_ID_FILE", "last_event_id.txt")