import os
from dotenv import load_dotenv

# Déterminer quel fichier .env charger
env_file = os.getenv("ENV_FILE", ".env")
load_dotenv(env_file)

API_TOKEN = os.getenv("API_TOKEN")
PLEX_URL = os.getenv("PLEX_URL")
PLEX_TOKEN = os.getenv("PLEX_TOKEN")
PLEX_LIBRARY = os.getenv("PLEX_LIBRARY")
DEVIANTART_CLIENT_ID = os.getenv("DEVIANTART_CLIENT_ID")
DEVIANTART_CLIENT_SECRET = os.getenv("DEVIANTART_CLIENT_SECRET")
UPDATE_INTERVAL = int(os.getenv("UPDATE_INTERVAL", "0"))
