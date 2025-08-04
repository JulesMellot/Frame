import requests
from .config import NTFY_URL


def send_notification():
    requests.post(
        NTFY_URL,
        data="NewOne",
    )


if __name__ == "__main__":
    send_notification()
