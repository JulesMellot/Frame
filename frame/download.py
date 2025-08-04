from .display import display
from .plugins import get_plugin
import json
import os

# ensure built-in plugins are registered
from . import deviantart  # noqa: F401
from . import plex  # noqa: F401
from . import fixed_download  # noqa: F401

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

    plugin = get_plugin(data["function"])
    if not plugin:
        print("NOT DOWNLOADED")
        return False
    if plugin():
        display()
        return True
    return False



