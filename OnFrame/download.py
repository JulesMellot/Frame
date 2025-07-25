from deviantart import deviantart
from fixed_download import fixed_download
from plex import plex
from display import display
import json
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
WEB_DIR = os.path.join(BASE_DIR, "OnWeb")

def download():
    destination = os.path.join(WEB_DIR, "function.json")

    if not os.path.exists(destination):
        print("function.json not found")
        return False

    with open(destination) as f:
        data = json.load(f)
    print(data["function"])

    #Download at the right spot depending on the file
    if data["function"] == "DeviantArt":
        deviantart()
        display()
    elif data["function"] == "plex":
        plex()
        display()
    elif data["function"] == "fixed":
        fixed_download()
        display()
    else:
        print("NOT DOWNLOADED")



