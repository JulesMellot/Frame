import requests
import random
import shutil
import json
import urllib.request
import os
from PIL import Image
from datetime import datetime


def deviantart():
    # Your client ID and your client secret
    client_id = "Your client id"
    client_secret = "Your client secret"

    # The DeviantArt OAuth API URL
    url = "https://www.deviantart.com/oauth2/token"

    # Access request parameters
    data = {
        "grant_type": "client_credentials",
        "client_id": client_id,
        "client_secret": client_secret
    }

    # Submit DeviantArt OAuth API access request
    response = requests.post(url, data=data)

    # Retrieving access token from API response
    access_token = response.json()["access_token"]

    ban_url_tag = "OnWeb.com/tags.json"
    destination = "tags.json"

    # Delete the old file if it exists
    if os.path.exists(destination):
        os.remove(destination)

    # Download JSON file and save to specified destination
    try:
        urllib.request.urlretrieve("OnWeb.com/tags.json", "tags.json")
        # print("Téléchargement réussi!")
    except Exception as e:
        print("Error downloading tags.json : ", e)

    # Load tags from tags.json file
    with open('tags.json', 'r') as f:
        json_tag = json.load(f)['tag']
        convert_json_tag = [item['name'] for item in json_tag]
    tag = random.choice(convert_json_tag)


    ban_url_tag = "OnWeb.com/bantag.json"
    destination = "bantag.json"

    # Delete the old file if it exists
    if os.path.exists(destination):
        os.remove(destination)

    # Download JSON file and save to specified destination
    try:
        urllib.request.urlretrieve("OnWeb.com/bantag.json", "bantag.json")
    except Exception as e:
        print("Error downloading bantag.json : ", e)

    # Load forbidden tags from bantag.json file
    with open('bantag.json', 'r') as f:
        json_exclude_tag = json.load(f)['ban']
        convert_json_exclude_tag = [item['name'] for item in json_exclude_tag]
    exclude_tag = ", ".join(convert_json_exclude_tag)
    # print(exclude_tag)

    # The maximum number of results you want to retrieve
    limit = 50

    # Initialize the variable that indicates if a satisfactory image was found
    image_found = False

    # Repeat the API request until you find a satisfactory image
    while not image_found:
        # Randomly choose an image from the search results
        url = f"https://www.deviantart.com/api/v1/oauth2/browse/tags?tag={tag}&limit={limit}&exclude={exclude_tag}&access_token={access_token}&mature_content=false"
        response = requests.get(url)
        if response.status_code != 200:
            print("An error occurred while retrieving data")
            return False
        data = response.json()
        results = data.get("results")
        if not results:
            print("No results found for the specified tag : "  + tag)
            return False
        image_info = random.choice(results)
        width = image_info.get("content", {}).get("width")
        height = image_info.get("content", {}).get("height")
        if height and width and height > width:
            if height >= 750:
                img_url = image_info["content"]["src"]
                img_src = image_info["url"]
                response = requests.get(img_url, stream=True)
                if response.status_code == 200:
                    response.raw.decode_content = True
                    # Data to add
                    data = {
                        "date": datetime.now().strftime("%Y-%m-%d"),
                        "heure": datetime.now().strftime("%H:%M:%S"),
                        "url": img_src,
                        "tag" : tag
                    }

                    # JSON file location
                    file_path = "history.json"

                    # Reading the existing JSON file
                    with open(file_path, "r") as f:
                        existing_data = json.load(f)

                    # Add new data
                    existing_data.append(data)

                    # Write updated data
                    with open(file_path, "w") as f:
                        json.dump(existing_data, f)

                    print("Data successfully added to history.json")

                    with open("img.png", "wb") as f:
                        print("Still's URL : " + img_src)
                        shutil.copyfileobj(response.raw, f)
                        print("Still had been downloaded with tag : " + tag)

                        requests.post("https://ntfy.sh/YOURNTFY",
                        data="Frame had been updated with tag :" + tag,
                        headers={
                            "Title": "Update on Frame",
                            "Click": img_url,
                            "Tags": "framed_picture"
                        })

                        image_found = True
                        return True
                else:
                    print("Unable to download Still :/")
                    return False
            else:
                print("Still dont have a good resolution, Frame had your convert and retry :)")
        else:
            print("The image must be in portrait mode (height > width)")
            
