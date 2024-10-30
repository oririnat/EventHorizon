import os
from dotenv import load_dotenv

load_dotenv()

RABBITMQ_HOST = os.getenv("RABBITMQ_HOST", "localhost")
RABBITMQ_PORT = int(os.getenv("RABBITMQ_PORT", 5672))
RABBITMQ_QUEUE = os.getenv("RABBITMQ_QUEUE", "github_events")
RABBITMQ_USER = os.getenv("RABBITMQ_USER", "user")
RABBITMQ_PASSWORD = os.getenv("RABBITMQ_PASSWORD", "password")

DATABASE_URL = os.getenv("DATABASE_URL")
