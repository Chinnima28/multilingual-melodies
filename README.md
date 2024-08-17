# Multilingual Melodies

Multilingual Melodies is a web application that connects with Spotify to fetch currently playing track information and display its lyrics. Users can also translate these lyrics into multiple languages using the Lingva Translate API.

## Features

- **Authorize Spotify**: Connect your Spotify account to get track details.
- **Fetch Current Track**: Retrieve and display the currently playing track.
- **Get Lyrics**: Show lyrics for the current track.
- **Translate Lyrics**: Translate lyrics into various languages.

## Setup

1. **Clone the Repository:**

    ```bash
    git clone https://github.com/yourusername/multilingual-melodies.git
    cd multilingual-melodies
    ```

2. **Install Dependencies:**

    Ensure you have Python and Flask installed. Install required packages with:

    ```bash
    pip install -r requirements.txt
    ```

3. **Create a `.env` File:**

    In the root directory, create a `.env` file and add your Spotify credentials:

    ```env
    SPOTIFY_CLIENT_ID=your_spotify_client_id
    SPOTIFY_CLIENT_SECRET=your_spotify_client_secret
    SPOTIFY_REDIRECT_URI=http://localhost:3000/callback
    ```

4. **Run the Application:**

    Start the Flask server:

    ```bash
    python server.py
    ```

5. **Open Your Browser:**

    Go to `http://localhost:3000` to start using the app.

## API Endpoints

- **GET /current-track**: Get details of the currently playing track.
- **GET /lyrics**: Fetch lyrics for a specified artist and track title.
- **POST /translate**: Translate lyrics to a chosen language.


