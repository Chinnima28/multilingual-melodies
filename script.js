document.addEventListener('DOMContentLoaded', () => {
    document.getElementById('auth-button').addEventListener('click', () => {
        window.location.href = `https://accounts.spotify.com/authorize?client_id=0d3a53f5d28e42ed82b1b3feaadc6aa4&response_type=code&redirect_uri=http://localhost:3000/callback&scope=user-read-currently-playing`;
    });

    document.getElementById('get-track-info').addEventListener('click', async () => {
        try {
            const response = await fetch('/current-track');
            if (!response.ok) throw new Error('Failed to fetch track info');

            const trackInfo = await response.json();
            document.getElementById('track-info').innerHTML = `Track Name: ${trackInfo.name}, Artist: ${trackInfo.artist}`;

            // Fetch lyrics
            const lyricsResponse = await fetch(`/lyrics?artist=${encodeURIComponent(trackInfo.artist)}&title=${encodeURIComponent(trackInfo.name)}`);
            if (!lyricsResponse.ok) throw new Error('Failed to fetch lyrics');

            const lyricsData = await lyricsResponse.json();
            document.getElementById('lyrics').textContent = lyricsData.lyrics || 'Lyrics not found.';
        } catch (error) {
            console.error(error);
            document.getElementById('lyrics').textContent = 'Error fetching lyrics.';
        }
    });

    document.getElementById('translate-button').addEventListener('click', async () => {
        const lyrics = document.getElementById('lyrics').textContent;
        const targetLang = document.getElementById('language').value;
    
        if (!lyrics || !targetLang) {
            document.getElementById('translated-lyrics').textContent = 'Please fetch lyrics and select a language.';
            return;
        }
    
        try {
            const response = await fetch('/translate', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ text: lyrics, sourceLang: 'en', targetLang })
            });
    
            if (!response.ok) throw new Error('Failed to translate text');
    
            const data = await response.json();
            document.getElementById('translated-lyrics').textContent = data.translatedText || 'Translation failed.';
        } catch (error) {
            console.error(error);
            document.getElementById('translated-lyrics').textContent = 'Error translating text.';
        }
    });
    
});
