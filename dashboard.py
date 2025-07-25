from flask import Flask, request, send_from_directory, jsonify
import os
import json

from OnFrame.download import download

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
WEB_DIR = os.path.join(BASE_DIR, 'OnWeb')

app = Flask(__name__, static_folder=WEB_DIR, static_url_path='')

@app.route('/')
def index():
    return send_from_directory(WEB_DIR, 'index.html')

@app.route('/<path:path>')
def static_proxy(path):
    return send_from_directory(WEB_DIR, path)

@app.route('/upload.php', methods=['POST'])
def upload_image():
    file = request.files.get('image')
    if not file:
        return 'No image uploaded', 400
    file.save(os.path.join(WEB_DIR, 'img.png'))
    return 'Image uploaded to server.'

@app.route('/update-json.php', methods=['POST'])
def update_json():
    data = request.get_json()
    if data is None:
        return jsonify(success=False), 400
    with open(os.path.join(WEB_DIR, 'function.json'), 'w') as f:
        json.dump(data, f)
    return jsonify(success=True)

@app.route('/update_tags.php', methods=['POST'])
def update_tags():
    data = request.get_json()
    if data is None:
        return jsonify(success=False), 400
    with open(os.path.join(WEB_DIR, 'tags.json'), 'w') as f:
        json.dump(data, f)
    return jsonify(success=True)

@app.route('/update_bantag.php', methods=['POST'])
def update_bantag():
    data = request.get_json()
    if data is None:
        return jsonify(success=False), 400
    with open(os.path.join(WEB_DIR, 'bantag.json'), 'w') as f:
        json.dump(data, f)
    return jsonify(success=True)

@app.route('/new', methods=['POST'])
def trigger_new():
    download()
    return jsonify(success=True)

if __name__ == '__main__':
    app.run(host='0.0.0.0')
