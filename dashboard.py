from flask import Flask, request, send_from_directory, jsonify, redirect, url_for
from functools import wraps
import os
import json
import requests

from frame.download import download
from frame.config import API_TOKEN

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
WEB_DIR = os.path.join(BASE_DIR, 'OnWeb')
ENV_FILE = os.path.join(BASE_DIR, '.env')

app = Flask(__name__, static_folder=WEB_DIR, static_url_path='')

def is_configured():
    """Vérifie si le fichier .env existe"""
    return os.path.exists(ENV_FILE)


def require_auth(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        header = request.headers.get("Authorization", "")
        token = header.split(" ")[-1] if header.startswith("Bearer ") else header
        print(f"API_TOKEN from config: {API_TOKEN}")
        print(f"Token from request: {token}")
        if not API_TOKEN or token != API_TOKEN:
            return "Unauthorized", 401
        return func(*args, **kwargs)
    return wrapper

@app.route('/')
def index():
    if not is_configured():
        return redirect(url_for('setup'))
    return send_from_directory(WEB_DIR, 'index.html')

@app.route('/<path:path>')
def static_proxy(path):
    # Vérifier si le fichier .env existe pour les autres routes
    if not is_configured() and path != 'setup.html' and not path.startswith('api/'):
        return redirect(url_for('setup'))
    return send_from_directory(WEB_DIR, path)

@app.route('/setup')
def setup():
    if is_configured():
        return redirect(url_for('index'))
    return send_from_directory(WEB_DIR, 'setup.html')

@app.route('/api/upload', methods=['POST'])
@require_auth
def upload_image():
    file = request.files.get('image')
    if not file:
        return 'No image uploaded', 400
    file.save(os.path.join(WEB_DIR, 'img.png'))
    return 'Image uploaded to server.'

@app.route('/api/upload_url', methods=['POST'])
@require_auth
def upload_image_from_url():
    data = request.get_json()
    if not data or 'url' not in data:
        return jsonify(success=False, error='URL is required'), 400
    
    image_url = data['url']
    try:
        # Télécharger l'image depuis l'URL
        response = requests.get(image_url)
        response.raise_for_status()
        
        # Vérifier que le contenu est une image
        content_type = response.headers.get('content-type', '').lower()
        if not content_type.startswith('image/'):
            # Essayer de vérifier l'extension du fichier si le content-type n'est pas clair
            import urllib.parse
            parsed_url = urllib.parse.urlparse(image_url)
            path = parsed_url.path.lower()
            image_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp']
            if not any(path.endswith(ext) for ext in image_extensions):
                return jsonify(success=False, error=f'URL does not point to an image (content-type: {content_type})'), 400
        
        # Sauvegarder l'image
        image_path = os.path.join(WEB_DIR, 'img.png')
        with open(image_path, 'wb') as f:
            f.write(response.content)
        
        return jsonify(success=True, message='Image uploaded successfully')
    except requests.RequestException as e:
        return jsonify(success=False, error=f'Failed to download image: {str(e)}'), 400
    except Exception as e:
        return jsonify(success=False, error=f'Failed to save image: {str(e)}'), 500

@app.route('/api/function', methods=['POST'])
@require_auth
def update_function():
    data = request.get_json()
    if data is None:
        return jsonify(success=False), 400
    with open(os.path.join(WEB_DIR, 'function.json'), 'w') as f:
        json.dump(data, f)
    return jsonify(success=True)

@app.route('/api/tags', methods=['POST'])
@require_auth
def update_tags():
    data = request.get_json()
    cleaned, error = _validate_words(data, 'tag')
    if error:
        return jsonify(success=False, error=error), 400
    with open(os.path.join(WEB_DIR, 'tags.json'), 'w') as f:
        json.dump(cleaned, f)
    return jsonify(success=True, message='Tags updated')

@app.route('/api/bantags', methods=['POST'])
@require_auth
def update_bantags():
    data = request.get_json()
    cleaned, error = _validate_words(data, 'ban')
    if error:
        return jsonify(success=False, error=error), 400
    with open(os.path.join(WEB_DIR, 'bantag.json'), 'w') as f:
        json.dump(cleaned, f)
    return jsonify(success=True, message='Banned tags updated')

@app.route('/api/new', methods=['POST'])
@require_auth
def trigger_new():
    """Déclenche le téléchargement et l'affichage d'une nouvelle image"""
    # Vérifier s'il s'agit d'une calibration
    data = request.get_json()
    calibration_mode = data.get('calibration', False) if data else False
    
    print(f"Triggering new image download, calibration_mode: {calibration_mode}")
    from frame.download import download
    result = download(calibration_mode=calibration_mode)
    return jsonify(success=result)

@app.route('/api/calibration', methods=['POST'])
@require_auth
def start_calibration():
    """Démarre le processus de calibration de l'écran"""
    try:
        # Créer l'image de calibration
        from frame.calibration import test_orientation
        image = test_orientation()
        
        # Afficher l'image de calibration
        from frame.display import display
        display()
        
        return jsonify(success=True, message="Calibration started. Check your e-Paper display.")
    except Exception as e:
        return jsonify(success=False, error=str(e)), 500

@app.route('/api/token', methods=['GET'])
@require_auth
def get_api_token():
    """Retourne le token API actuel"""
    return jsonify(success=True, api_token=API_TOKEN)

@app.route('/api/setup', methods=['POST'])
def save_setup():
    if is_configured():
        return jsonify(success=False, error="Already configured"), 400
    
    data = request.get_json()
    if not data:
        return jsonify(success=False, error="Invalid data"), 400
    
    # Si aucun token API n'est fourni, en générer un automatiquement
    if 'API_TOKEN' not in data or not data['API_TOKEN']:
        import secrets
        data['API_TOKEN'] = secrets.token_urlsafe(32)
    
    # Créer le fichier .env avec les paramètres fournis
    with open(ENV_FILE, 'w') as f:
        for key, value in data.items():
            f.write(f"{key}={value}\n")
    
    return jsonify(success=True, api_token=data['API_TOKEN'])


def _validate_words(payload, key):
    if not isinstance(payload, dict) or key not in payload:
        return None, 'Invalid payload'
    items = payload.get(key)
    if not isinstance(items, list):
        return None, 'Invalid payload'
    names = []
    for item in items:
        if not isinstance(item, dict) or 'name' not in item:
            return None, 'Invalid payload'
        name = item['name'].strip()
        if not name:
            return None, 'Empty tag not allowed'
        names.append(name)
    lowered = [n.lower() for n in names]
    if len(set(lowered)) != len(lowered):
        return None, 'Duplicate tags'
    return {key: [{'name': n} for n in names]}, None

if __name__ == '__main__':
    app.run(host='0.0.0.0')
