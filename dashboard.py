from flask import Flask, request, send_from_directory, jsonify
from functools import wraps
import os
import json

from frame.download import download
from frame.config import API_TOKEN

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
WEB_DIR = os.path.join(BASE_DIR, 'OnWeb')

app = Flask(__name__, static_folder=WEB_DIR, static_url_path='')


def require_auth(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        header = request.headers.get("Authorization", "")
        token = header.split(" ")[-1] if header.startswith("Bearer ") else header
        if not API_TOKEN or token != API_TOKEN:
            return "Unauthorized", 401
        return func(*args, **kwargs)
    return wrapper

@app.route('/')
def index():
    return send_from_directory(WEB_DIR, 'index.html')

@app.route('/<path:path>')
def static_proxy(path):
    return send_from_directory(WEB_DIR, path)

@app.route('/api/upload', methods=['POST'])
@require_auth
def upload_image():
    file = request.files.get('image')
    if not file:
        return 'No image uploaded', 400
    file.save(os.path.join(WEB_DIR, 'img.png'))
    return 'Image uploaded to server.'

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
    download()
    return jsonify(success=True)


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
