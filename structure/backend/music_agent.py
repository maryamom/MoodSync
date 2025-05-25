import spotipy
from spotipy.oauth2 import SpotifyOAuth
from dotenv import load_dotenv
import openai
import os 


class MusicAgent:
    def __init__(self, spotify_client_id, spotify_client_secret, redirect_uri, openai_api_key):
        """
        Initialize the MusicAgent with Spotify and OpenAI credentials.

        Args:
            spotify_client_id (str): Spotify Client ID.
            spotify_client_secret (str): Spotify Client Secret.
            redirect_uri (str): Redirect URI for Spotify OAuth.
            openai_api_key (str): OpenAI API key.
        """
        # Spotify Initialization
        self.sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
            client_id=spotify_client_id,
            client_secret=spotify_client_secret,
            redirect_uri=redirect_uri,
            scope="user-read-playback-state user-modify-playback-state"
        ))

        # OpenAI Initialization
        openai.api_key = openai_api_key

    def generate_music_query(self, emotion_or_state):
        """
        Use OpenAI GPT to generate a Spotify search query based on the detected emotion or state.

        Args:
            emotion_or_state (str): The detected emotion or state (e.g., "calm", "anxious", "motivated").

        Returns:
            str: Spotify search query (e.g., a song, artist, genre, or mood).
        """
        try:
            messages = [
                {"role": "system", "content": "You are an assistant that helps recommend Spotify music based on emotional states."},
                {"role": "user", "content": f"The detected emotion is: {emotion_or_state}. Suggest a query Spotify can use to play relevant music. Provide a detailed suggestion, such as 'uplifting pop playlist' or 'relaxing piano instrumental'."}
            ]
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=messages,
                max_tokens=100
            )
            query = response.choices[0].message["content"].strip()
            print(f"OpenAI Generated Query: {query}")
            return query
        except Exception as e:
            print(f"Error generating music query: {e}")
            return None

    def play_music_on_spotify(self, search_query):
        """
        Search Spotify for music and play it on an active device.

        Args:
            search_query (str): Spotify search query.
        """
        try:
            print(f"Searching Spotify for: {search_query}...")
            # Search Spotify for relevant content
            results = self.sp.search(q=search_query, limit=1, type='track,playlist,album')

            # Determine the URI of the best result
            uri = None
            if results['tracks']['items']:
                track = results['tracks']['items'][0]
                uri = track['uri']
                print(f"Playing track: {track['name']} by {track['artists'][0]['name']}")
            elif results['playlists']['items']:
                playlist = results['playlists']['items'][0]
                uri = playlist['uri']
                print(f"Playing playlist: {playlist['name']}")
            elif results['albums']['items']:
                album = results['albums']['items'][0]
                uri = album['uri']
                print(f"Playing album: {album['name']} by {album['artists'][0]['name']}")
            else:
                print("No relevant content found on Spotify.")
                return

            # Get active Spotify devices
            devices = self.sp.devices()
            if devices['devices']:
                device_id = devices['devices'][0]['id']
                print(f"Playing on device: {devices['devices'][0]['name']}")
                self.sp.start_playback(device_id=device_id, context_uri=uri)
            else:
                print("No active Spotify devices found. Please start Spotify on a device.")
        except Exception as e:
            print(f"Error playing music on Spotify: {e}")

    def play_music_based_on_emotion(self, emotion_or_state):
        """
        End-to-end function to generate a recommendation, search Spotify, and play the music.

        Args:
            emotion_or_state (str): Detected emotion or state (e.g., "happy", "stressed").
        """
        # Generate a music query using OpenAI
        search_query = self.generate_music_query(emotion_or_state)
        if search_query:
            # Play music on Spotify
            self.play_music_on_spotify(search_query)


if __name__ == "__main__":
    load_dotenv()

    # Spotify and OpenAI API credentials
    spotify_client_id = os.getenv("SPOTIFY_CLIENT_ID")
    spotify_client_secret = os.getenv("SPOTIFY_CLIENT_SECRET")
    redirect_uri = os.getenv("REDIRECT_URI")
    openai_api_key = os.getenv("OPENAI_API_KEY")

    # Initialize the MusicAgent
    music_agent = MusicAgent(
        spotify_client_id=spotify_client_id,
        spotify_client_secret=spotify_client_secret,
        redirect_uri=redirect_uri,
        openai_api_key=openai_api_key
    )

    # Example detected emotion
    detected_emotion = "calm"

    # Play music based on the detected emotion
    music_agent.play_music_based_on_emotion(detected_emotion)
