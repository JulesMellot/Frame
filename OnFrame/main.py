from download import download
import requests
import urllib.request
import time


# Function that checks if an Internet connection is available
def check_internet():
    try:
        urllib.request.urlopen('https://www.google.com/')
        return True
    except:
        return False

# Wait until an internet connection is available
while not check_internet():
    print("CHECKING FOR INTERNET...")
    time.sleep(60)




while True:
    resp = requests.get("https://ntfy.sh/YOURNTFY/raw", stream=True)
    for line in resp.iter_lines():
        if line:
            # Convert line to string and remove quotes
            data_str = line.decode('utf-8').strip('"')
            if data_str == "NewOne":
                download()
