import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URI = os.getenv("DATABASE_URI")
GITHUB_AUTH_TOKEN = os.getenv("GITHUB_AUTH_TOKEN")
