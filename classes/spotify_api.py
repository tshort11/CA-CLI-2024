from prettytable import PrettyTable
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from spotipy.exceptions import SpotifyException
import requests
import time

class SpotifyAPI:
    """
    A class to interact with Spotify's API.

    This class provides methods to authenticate, search for albums, songs, and artists,
    retrieve new releases, and get the user's top tracks.

    Attributes:
    ----------
    client_id : str
        Spotify application client ID.
    client_secret : str
        Spotify application client secret.
    redirect_uri : str
        Redirect URI registered with the Spotify API.
    scope : str
        Spotify access permissions required for the API (e.g., "user-top-read").
    sp : spotipy.Spotify
        Spotify client for making API requests.
    access_token : str, optional
        Access token for Spotify API requests.
    refresh_token : str, optional
        Refresh token to renew access token when it expires.
    token_expires : float, optional
        Timestamp for when the token expires.
    """

    def __init__(self, client_id, client_secret, redirect_uri):
        """
        Initialize SpotifyAPI with authentication details and set up Spotipy client.
        """
        self.client_id = client_id
        self.client_secret = client_secret
        self.redirect_uri = redirect_uri
        self.scope = "user-top-read"  # Permission scope for accessing user data
        self.sp = self.authenticate()  # Authenticate with Spotify API
        self.access_token = None
        self.refresh_token = None
        self.token_expires = None 

    def refresh_access_token(self):
        """
        Refresh the Spotify API access token using the refresh token.
        """
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
                self.token_expires = time.time() + data['expires_in']
                print("Access token refreshed successfully.")
            else:
                print("Failed to refresh access token:", response.json())
        else:
            print("No refresh token available.")

    def refresh_token_if_expired(self):
        """
        Check if the access token has expired and refresh it if needed.
        """
        if self.token_expires and (time.time() > self.token_expires):
            self.refresh_access_token()

    def authenticate(self):
        """
        Authenticate with Spotify and initialize the Spotipy client.

        Returns:
        -------
        spotipy.Spotify
            Authenticated Spotipy client.
        """
        sp_oauth = SpotifyOAuth(
            client_id=self.client_id,
            client_secret=self.client_secret,
            redirect_uri=self.redirect_uri,
            scope=self.scope
        )
        token_info = sp_oauth.get_access_token(as_dict=False)
        return spotipy.Spotify(auth=token_info)

    def search_album(self, album_name):
        """
        Search for an album by name.

        Parameters:
        ----------
        album_name : str
            The name of the album to search for.

        Returns:
        -------
        dict or None
            A dictionary with album details if found, otherwise None.
        """
        self.refresh_token_if_expired()  # Ensure token is valid
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
        """
        Search for a song by name.

        Parameters:
        ----------
        song_name : str
            The name of the song to search for.

        Returns:
        -------
        dict or None
            A dictionary with song details if found, otherwise None.
        """
        self.refresh_token_if_expired()
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
        """
        Search for an artist by name.

        Parameters:
        ----------
        artist_name : str
            The name of the artist to search for.

        Returns:
        -------
        dict or None
            A dictionary with artist details if found, otherwise None.
        """
        self.refresh_token_if_expired()
        try:
            result = self.sp.search(q='artist:' + artist_name, type='artist')
            return result['artists']['items'][0] if result['artists']['items'] else None
        except SpotifyException as e:
            print("Error searching for artist:", e)
            return None

    def get_new_releases(self):
        """
        Retrieve new album releases.

        Returns:
        -------
        list
            A list of dictionaries containing new album details.
        """
        self.refresh_token_if_expired()
        results = self.sp.new_releases(limit=10)
        return results['albums']['items']

    def get_top_tracks(self):
        """
        Retrieve the user's top tracks.

        Returns:
        -------
        list
            A list of dictionaries containing the user's top tracks.
        """
        self.refresh_token_if_expired()
        results = self.sp.current_user_top_tracks(limit=10)
        return results['items']


def display_new_releases(releases):
    """
    Display new album releases in a tabular format.

    Parameters:
    ----------
    releases : list
        A list of album dictionaries to display.
    """
    table = PrettyTable()
    table.field_names = ["Album Name", "Artist(s)", "Release Date", "URL"]

    for album in releases:
        album_name = album['name']
        artists = ", ".join([artist['name'] for artist in album['artists']])
        release_date = album['release_date']
        url = album['external_urls']['spotify']

        table.add_row([album_name, artists, release_date, url])

    print(table)
