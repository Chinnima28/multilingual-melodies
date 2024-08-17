from flask import Flask, request, redirect, jsonify, send_from_directory
import requests
import base64
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__, static_folder='.')

# Spotify credentials from environment variables
SPOTIFY_CLIENT_ID = os.getenv('SPOTIFY_CLIENT_ID')
SPOTIFY_CLIENT_SECRET = os.getenv('SPOTIFY_CLIENT_SECRET')
SPOTIFY_REDIRECT_URI = os.getenv('SPOTIFY_REDIRECT_URI')

access_token = None

@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

@app.route('/script.js')
def serve_js():
    return send_from_directory('.', 'script.js')

@app.route('/callback')
def callback():
    code = request.args.get('code')
    if code:
        try:
            token_url = 'https://accounts.spotify.com/api/token'
            headers = {
                'Authorization': 'Basic ' + base64.b64encode(f"{SPOTIFY_CLIENT_ID}:{SPOTIFY_CLIENT_SECRET}".encode()).decode(),
                'Content-Type': 'application/x-www-form-urlencoded'
            }
            data = {
                'grant_type': 'authorization_code',
                'code': code,
                'redirect_uri': SPOTIFY_REDIRECT_URI
            }
            response = requests.post(token_url, headers=headers, data=data)
            response_data = response.json()
            global access_token
            access_token = response_data['access_token']
            return f"Access token: {access_token}"
        except Exception as e:
            print('Error exchanging code for token:', e)
            return 'Error exchanging code for token', 500
    else:
        return 'No code provided', 400

@app.route('/current-track')
def current_track():
    if not access_token:
        return 'No access token available', 401

    try:
        headers = {
            'Authorization': f'Bearer {access_token}'
        }
        response = requests.get('https://api.spotify.com/v1/me/player/currently-playing', headers=headers)
        track = response.json().get('item')
        if track:
            return jsonify({
                'id': track['id'],
                'name': track['name'],
                'artist': ', '.join(artist['name'] for artist in track['artists'])
            })
        else:
            return 'No track currently playing', 404
    except Exception as e:
        print('Error fetching current track:', e)
        return 'Error fetching current track', 500

@app.route('/lyrics', methods=['GET'])
def lyrics():
    artist = request.args.get('artist')
    title = request.args.get('title')
    if not artist or not title:
        return 'Artist or title not provided', 400

    try:
        response = requests.get(f'https://api.lyrics.ovh/v1/{artist}/{title}')
        lyrics = response.json().get('lyrics')
        if lyrics:
            return jsonify({'lyrics': lyrics})
        else:
            return 'Lyrics not found', 404
    except Exception as e:
        print('Error fetching lyrics:', e)
        return 'Error fetching lyrics', 500

@app.route('/translate', methods=['POST'])
def translate():
    data = request.json
    text = data.get('text')
    source_lang = data.get('sourceLang', 'en')
    target_lang = data.get('targetLang')

    if not text or not target_lang:
        return 'Text or target language not provided', 400

    try:
        # Update this URL with the correct endpoint for Lingva Translate
        response = requests.get(f'https://lingva.ml/api/v1/{source_lang}/{target_lang}/{text}')
        response.raise_for_status()  # Raise an exception for HTTP errors
        translation = response.json().get('translation')

        if translation:
            return jsonify({'translatedText': translation})
        else:
            return 'Translation not found', 404
    except Exception as e:
        print('Error translating text:', e)
        return 'Error translating text', 500

if __name__ == '__main__':
    app.run(port=3000, debug=True)
