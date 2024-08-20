from flask import Flask, request, jsonify, send_from_directory
import subprocess
import os

app = Flask(__name__, static_folder='.')

@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

@app.route('/script.js')
def serve_js():
    return send_from_directory('.', 'script.js')

@app.route('/lyrics', methods=['GET'])
def lyrics():
    artist = request.args.get('artist')
    title = request.args.get('title')

    if not artist or not title:
        return 'Artist or title not provided', 400

    try:
        result = subprocess.run(
            ['java', 'MultilingualMelodiesJava', artist, title],  # Call the Java program
            stdout=subprocess.PIPE
        )
        lyrics = result.stdout.decode('utf-8').strip()
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
        result = subprocess.run(
            ['java', 'MultilingualMelodiesJava', text, source_lang, target_lang],  # Call the Java program
            stdout=subprocess.PIPE
        )
        translation = result.stdout.decode('utf-8').strip()
        if translation:
            return jsonify({'translatedText': translation})
        else:
            return 'Translation not found', 404
    except Exception as e:
        print('Error translating text:', e)
        return 'Error translating text', 500

if __name__ == '__main__':
    app.run(port=3000, debug=True)
