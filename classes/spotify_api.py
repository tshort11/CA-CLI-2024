from prettytable import PrettyTable
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from spotipy.exceptions import SpotifyException
import requests
import time

class SpotifyAPI:
    def __init__(self, client_id, client_secret, redirect_uri):
        self.client_id = client_id
        self.client_secret = client_secret
        self.redirect_uri = redirect_uri
        self.scope = "user-top-read"
        self.sp = self.authenticate()
        self.access_token = None
        self.refresh_token = None
        self.token_expires = None 

    def refresh_access_token(self):
        if self.refresh_token:
            url = 'https://accounts.spotify.com/api/token'
            headers = {
                'Content-Type': 'application/x-www-form-urlencoded',
            }
            payload = {
                'grant_type': 'refresh_token',
                'refresh_token': self.refresh_token,
                'client_id': self.client_id,
                'client_secret': self.client_secret,
            }
            response = requests.post(url, headers=headers, data=payload)
            if response.status_code == 200:
                data = response.json()
                self.access_token = data['access_token']
                self.token_expires = data['expires_in']
                print("Access token refreshed successfully.")
            else:
                print("Failed to refresh access token:", response.json())
        else:
            print("No refresh token available.")

    def refresh_token_if_expired(self):
        if self.token_expires and (time.time() > self.token_expires):
            self.refresh_access_token()
            # Set the token expiry time
            self.token_expires = time.time() + 3600 

    # def search_album(self, album_name):
    #     self.refresh_token_if_expired()
    #     headers = {
    #         'Authorization': f'Bearer {self.access_token}'
    #     }

    def search_album(self, album_name):
        result = self.sp.search(q='album:' + album_name, type='album')
        albums = result['albums']['items']
        if albums:
            album = albums[0]
            return {
                'title': album['name'],
                'artist': album['artists'][0]['name'],
                'release_date': album['release_date'],
                'total_tracks': album['total_tracks']
            }
        return None

    def search_song(self, song_name):
        result = self.sp.search(q='track:' + song_name, type='track')
        tracks = result['tracks']['items']
        if tracks:
            track = tracks[0]
            return {
                'title': track['name'],
                'artist': track['artists'][0]['name'],
                'album': track['album']['name'],
                'duration_ms': track['duration_ms']
            }
        return None

    def search_artist(self, artist_name):
        self.refresh_token_if_expired()
        try:
            result = self.sp.search(q='artist:' + artist_name, type='artist')
            return result['artists']['items'][0] if result['artists']['items'] else None
        except SpotifyException as e:
            print("Error searching for artist:", e)
            return None
    
    def authenticate(self):
        sp_oauth = SpotifyOAuth(client_id=self.client_id, client_secret=self.client_secret,redirect_uri=self.redirect_uri, scope=self.scope)
        token_info = sp_oauth.get_access_token(as_dict=False)
        return spotipy.Spotify(auth=token_info)

    def get_new_releases(self):
        results = self.sp.new_releases(limit=10)
        return results['albums']['items']

    def get_top_tracks(self):
        results = self.sp.current_user_top_tracks(limit=10)
        return results['items']

def display_new_releases(releases):
    table = PrettyTable()
    table.field_names = ["Album Name", "Artist(s)", "Release Date", "URL"]

    for album in releases:
        album_name = album['name']
        artists = ", ".join([artist['name'] for artist in album['artists']])
        release_date = album['release_date']
        url = album['external_urls']['spotify']

        table.add_row([album_name, artists, release_date, url])

    print(table)
