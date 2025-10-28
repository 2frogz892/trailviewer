<details><summary>Tap to copy code</summary>
from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('map.html')

@app.route('/trails')
def get_trails():
    lat = request.args.get('lat')
    lon = request.args.get('lon')
    if not lat or not lon:
        return jsonify({"error": "missing lat/lon"}), 400

    overpass_url = "https://overpass-api.de/api/interpreter"
    query = f"""
    [out:json];
    way["highway"="path"](around:5000,{lat},{lon});
    out geom;
    """
    r = requests.get(overpass_url, params={'data': query})
    data = r.json()

    trails = []
    for element in data.get('elements', []):
        coords = [(p['lat'], p['lon']) for p in element.get('geometry', [])]
        if coords:
            trails.append({'id': element['id'], 'coords': coords})

    return jsonify(trails)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
    </details>
    
