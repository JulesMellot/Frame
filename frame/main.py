import time
import urllib.request

from .download import download
from .config import UPDATE_INTERVAL
from .scheduler import Scheduler

def check_internet():
    """Return True if an Internet connection is available."""
    try:
        urllib.request.urlopen('https://www.google.com/', timeout=5)
        return True
    except Exception:
        return False

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
    # Boucle infinie pour garder le programme en cours d'exécution
    try:
        while True:
            time.sleep(60)
    except KeyboardInterrupt:
        print("Stopping...")
    finally:
        if scheduler:
            scheduler.stop()
