from deviantart import deviantart
from fixed_download import fixed_download
from plex import plex
from display import display
import requests
import urllib.request
import time
import json
import os

def download():
    destination = "function.json"

    # Delete the old file if it exists
    if os.path.exists(destination):
        os.remove(destination)

    # Download JSON file and save to specified destination
    try:
        urllib.request.urlretrieve("OnWeb.com/function.json", "function.json")
    except Exception as e:
        print("Erreur lors du téléchargement function.json : ", e)


    with open("function.json") as f:
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



