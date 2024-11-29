import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

class SpotifyHandler:
    def __init__(self, client_id, client_secret):
        self.client_id = client_id
        self.client_secret = client_secret
        self.sp = self.authenticate()

    def authenticate(self):
        auth_manager = SpotifyClientCredentials(client_id=self.client_id, client_secret=self.client_secret)
        return spotipy.Spotify(auth_manager=auth_manager)

    def search_album(self, album_name):
        results = self.sp.search(q=album_name, type='album')
        return results
