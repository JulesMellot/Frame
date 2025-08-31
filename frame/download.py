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
    print("Starting download function")
    destination = os.path.join(WEB_DIR, "function.json")
    print(f"Looking for function file: {destination}")

    if not os.path.exists(destination):
        print("function.json not found")
        return False

    with open(destination) as f:
        data = json.load(f)
    print(f"Function data: {data}")
    
    if "function" not in data:
        print("No function specified in function.json")
        return False
        
    print(f"Selected function: {data['function']}")

    plugin = get_plugin(data["function"])
    if not plugin:
        print(f"Plugin {data['function']} not found")
        return False
    print(f"Plugin found: {data['function']}")
    
    if plugin():
        print("Plugin executed successfully, calling display()")
        display()
        return True
    else:
        print("Plugin execution failed")
        return False



