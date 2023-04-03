import random
import requests
from PIL import Image
from plexapi.server import PlexServer
from io import BytesIO


def plex():
    # Plex API Setup
    PLEX_URL = 'YOUR PLEX SERVER'
    PLEX_TOKEN = 'YOUR PLEX TOKEN'
    plex = PlexServer(PLEX_URL, PLEX_TOKEN)

    # Connecting to the Plex Server
    plex = PlexServer(PLEX_URL, PLEX_TOKEN)

    # Retrieving list of all movies
    movies = plex.library.section('YOUR LIBRARY').all()

    # Choice of a random movie
    movie = random.choice(movies)

    # Viewing movie information
    print('Title :', movie.title)
    print('Years :', movie.year)
    print('Gender :', ', '.join([g.tag for g in movie.genres]))
    print('Director :', ', '.join([d.tag for d in movie.directors]))
    print('Actors :', ', '.join([a.tag for a in movie.actors]))
    print('Synopsis :', movie.summary)
    print(movie.guid)
    # Fetch movie poster url
    poster_url = '{}{}?X-Plex-Token={}'.format(PLEX_URL, movie.thumb, PLEX_TOKEN)

    # Download the poster and save as "poster.jpg"
    response = requests.get(poster_url)
    image = Image.open(BytesIO(response.content)) 
    image.save('img.png')
    requests.post("https://ntfy.sh/YOURNTFY",
        data="Frame have been updated with :" + movie.title + " poster",
            headers={
                "Title": "Update on Frame",
                "Click": movie.guid,
                "Tags": "framed_picture"
            })
    return True
