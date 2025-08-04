import os
from dotenv import load_dotenv

load_dotenv()

API_TOKEN = os.getenv("API_TOKEN")
NTFY_URL = os.getenv("NTFY_URL")
PLEX_URL = os.getenv("PLEX_URL")
PLEX_TOKEN = os.getenv("PLEX_TOKEN")
PLEX_LIBRARY = os.getenv("PLEX_LIBRARY")
DEVIANTART_CLIENT_ID = os.getenv("DEVIANTART_CLIENT_ID")
DEVIANTART_CLIENT_SECRET = os.getenv("DEVIANTART_CLIENT_SECRET")
UPDATE_INTERVAL = int(os.getenv("UPDATE_INTERVAL", "0"))
