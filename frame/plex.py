import random
import requests
from PIL import Image
from plexapi.server import PlexServer
from io import BytesIO
from .config import PLEX_URL, PLEX_TOKEN, PLEX_LIBRARY
from .plugins import register_plugin


def plex():
    # Plex API Setup
    plex = PlexServer(PLEX_URL, PLEX_TOKEN)

    # Connecting to the Plex Server
    plex = PlexServer(PLEX_URL, PLEX_TOKEN)

    # Retrieving list of all movies
    movies = plex.library.section(PLEX_LIBRARY).all()


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
    return True
 

register_plugin("plex", plex)
