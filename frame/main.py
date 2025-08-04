import time
import requests
import urllib.request

from .download import download
from .config import NTFY_URL, UPDATE_INTERVAL
from .scheduler import Scheduler

def check_internet():
    """Return True if an Internet connection is available."""
    try:
        urllib.request.urlopen('https://www.google.com/', timeout=5)
        return True
    except Exception:
        return False

def listen_ntfy() -> None:
    """Listen to the ntfy topic and trigger downloads on demand."""
    while True:
        try:
            with requests.get(f"{NTFY_URL}/raw", stream=True, timeout=60) as resp:
                for line in resp.iter_lines():
                    if line:
                        data_str = line.decode("utf-8").strip("\"")
                        if data_str == "NewOne":
                            download()
        except KeyboardInterrupt:
            print("Stopping listener")
            break
        except requests.RequestException as exc:
            print(f"Connection error: {exc}. Retrying in 5s...")
            time.sleep(5)


def start_scheduler() -> Scheduler | None:
    """Start periodic downloads if configured."""
    if UPDATE_INTERVAL and UPDATE_INTERVAL > 0:
        sched = Scheduler(UPDATE_INTERVAL, download)
        sched.start()
        return sched
    return None

if __name__ == "__main__":
    while not check_internet():
        print("CHECKING FOR INTERNET...")
        time.sleep(60)
    scheduler = start_scheduler()
    try:
        listen_ntfy()
    finally:
        if scheduler:
            scheduler.stop()
