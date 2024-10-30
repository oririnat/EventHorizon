import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
GITHUB_AUTH_TOKEN = os.getenv("GITHUB_AUTH_TOKEN")
