import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

class SpotifyHandler:
    """
    A handler for interacting with the Spotify API using client credentials.

    This class provides methods to authenticate and search for albums
    using the Spotify Web API.

    Attributes:
    ----------
    client_id : str
        Spotify application client ID.
    client_secret : str
        Spotify application client secret.
    sp : spotipy.Spotify
        Authenticated Spotipy client for making API requests.
    """

    def __init__(self, client_id, client_secret):
        """
        Initialize SpotifyHandler with authentication details and set up Spotipy client.

        Parameters:
        ----------
        client_id : str
            Spotify application client ID.
        client_secret : str
            Spotify application client secret.
        """
        self.client_id = client_id  # Spotify API client ID
        self.client_secret = client_secret  # Spotify API client secret
        self.sp = self.authenticate()  # Initialize authenticated Spotipy client

    def authenticate(self):
        """
        Authenticate using Spotify's Client Credentials flow.

        Returns:
        -------
        spotipy.Spotify
            Authenticated Spotipy client for making API requests.
        """
        # Use SpotifyClientCredentials for app-only authentication
        auth_manager = SpotifyClientCredentials(
            client_id=self.client_id,
            client_secret=self.client_secret
        )
        return spotipy.Spotify(auth_manager=auth_manager)

    def search_album(self, album_name):
        """
        Search for an album by name using the Spotify API.

        Parameters:
        ----------
        album_name : str
            The name of the album to search for.

        Returns:
        -------
        dict
            A dictionary containing search results for albums matching the query.
        """
        # Query the Spotify API for albums matching the given name
        results = self.sp.search(q=album_name, type='album')
        return results
