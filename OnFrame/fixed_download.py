import urllib.request
import requests
#connect to OnWeb(your server) and download still
def fixed_download():
    url = "OnWeb.com/img.png"
    filename = "img.png"

    urllib.request.urlretrieve(url, filename)
    print("FIXED DOWNLOADED")
    return True
