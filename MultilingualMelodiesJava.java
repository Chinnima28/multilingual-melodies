import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.net.HttpURLConnection;
import java.net.URL;

public class MultilingualMelodiesJava {

    public static void main(String[] args) {
        if (args.length == 2) {

            String artist = args[0];
            String title = args[1];
            String lyrics = fetchLyrics(artist, title);
            System.out.println(lyrics != null ? lyrics : "Lyrics not found");
        } else if (args.length == 3) {

            String lyrics = args[0];
            String sourceLang = args[1];
            String targetLang = args[2];
            String translatedLyrics = translateLyrics(lyrics, sourceLang, targetLang);
            System.out.println(translatedLyrics != null ? translatedLyrics : "Translation not found");
        } else {
            System.out.println("Invalid arguments");
        }
    }

    public static String fetchLyrics(String artist, String title) {
        try {
            String apiUrl = String.format("https://api.lyrics.ovh/v1/%s/%s", artist, title);
            URL url = new URL(apiUrl);
            HttpURLConnection conn = (HttpURLConnection) url.openConnection();
            conn.setRequestMethod("GET");
            
            BufferedReader in = new BufferedReader(new InputStreamReader(conn.getInputStream()));
            StringBuilder response = new StringBuilder();
            String line;
            
            while ((line = in.readLine()) != null) {
                response.append(line);
            }
            in.close();
            
            String jsonResponse = response.toString();
            // For simplicity, assuming lyrics are directly available as plain text
            return jsonResponse; 
        } catch (Exception e) {
            e.printStackTrace();
            return null;
        }
    }

    public static String translateLyrics(String lyrics, String sourceLang, String targetLang) {
        try {
            String apiUrl = String.format("https://lingva.ml/api/v1/%s/%s/%s", sourceLang, targetLang, lyrics);
            URL url = new URL(apiUrl);
            HttpURLConnection conn = (HttpURLConnection) url.openConnection();
            conn.setRequestMethod("GET");
            
            BufferedReader in = new BufferedReader(new InputStreamReader(conn.getInputStream()));
            StringBuilder response = new StringBuilder();
            String line;
            
            while ((line = in.readLine()) != null) {
                response.append(line);
            }
            in.close();
            
            String jsonResponse = response.toString();
            return jsonResponse; // Replace with actual JSON parsing
        } catch (Exception e) {
            e.printStackTrace();
            return null;
        }
    }
}
