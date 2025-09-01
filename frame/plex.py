import random
import requests
from PIL import Image
from plexapi.server import PlexServer
from plexapi.exceptions import NotFound
from io import BytesIO
from .config import PLEX_URL, PLEX_TOKEN, PLEX_LIBRARY
from .plugins import register_plugin
import urllib3

# Désactiver les avertissements SSL
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def plex():
    try:
        # Plex API Setup - avec vérification SSL désactivée
        print(f"Connecting to Plex server: {PLEX_URL}")
        session = requests.Session()
        session.verify = False  # Désactiver la vérification SSL
        plex = PlexServer(PLEX_URL, PLEX_TOKEN, session=session)

        # Connecting to the Plex Server
        print("Getting library sections...")
        movies = plex.library.section(PLEX_LIBRARY).all()
        print(f"Found {len(movies)} movies")

        # Choice of a random movie
        if not movies:
            print("No movies found in library")
            return False
            
        movie = random.choice(movies)

        # Viewing movie information
        print('Title:', movie.title)
        print('Years:', movie.year)
        print('Gender:', ', '.join([g.tag for g in movie.genres]) if movie.genres else 'N/A')
        print('Director:', ', '.join([d.tag for d in movie.directors]) if movie.directors else 'N/A')
        print('Actors:', ', '.join([a.tag for a in movie.actors]) if movie.actors else 'N/A')
        print('Synopsis:', movie.summary[:100] + '...' if len(movie.summary) > 100 else movie.summary)
        print('GUID:', movie.guid)
        
        # Fetch movie poster url
        if not movie.thumb:
            print("No poster available for this movie")
            return False
            
        poster_url = f'{PLEX_URL}{movie.thumb}?X-Plex-Token={PLEX_TOKEN}'
        print(f'Poster URL: {poster_url}')

        # Download the poster and save as "img.png"
        response = requests.get(poster_url, verify=False)  # Désactiver la vérification SSL
        if response.status_code != 200:
            print(f"Failed to download poster: {response.status_code}")
            return False
            
        image = Image.open(BytesIO(response.content)) 
        image.save('img.png')
        print("Poster saved successfully")
        return True
        
    except NotFound as e:
        print(f"Plex library not found: {e}")
        return False
    except Exception as e:
        print(f"Error in Plex plugin: {e}")
        import traceback
        traceback.print_exc()
        return False

register_plugin("plex", plex)
