import json

class User:
    """
    A class to represent a user in the application.

    Attributes:
    ----------
    user_id : int
        Unique identifier for the user.
    username : str
        The user's username.
    email : str
        The user's email address.
    password : str
        The user's password.
    favorite_albums : list
        A list of the user's favorite album objects (maximum of 5).
    favorite_songs : list
        A list of the user's favorite song objects (maximum of 5).
    favorite_artists : list
        A list of the user's favorite artist objects (maximum of 5).
    """

    def __init__(self, user_id, username, email, password, favorite_albums=None, favorite_songs=None, favorite_artists=None):
        """
        Initialize a User object with basic information and favorite items.

        Parameters:
        ----------
        user_id : int
            Unique identifier for the user.
        username : str
            The user's username.
        email : str
            The user's email address.
        password : str
            The user's password.
        favorite_albums : list, optional
            A list of the user's favorite albums. Defaults to an empty list.
        favorite_songs : list, optional
            A list of the user's favorite songs. Defaults to an empty list.
        favorite_artists : list, optional
            A list of the user's favorite artists. Defaults to an empty list.
        """
        self.user_id = user_id  # Unique identifier for the user
        self.username = username  # User's username
        self.email = email  # User's email
        self.password = password  # User's password
        self.favorite_albums = favorite_albums if favorite_albums is not None else []  # User's favorite albums
        self.favorite_songs = favorite_songs if favorite_songs is not None else []  # User's favorite songs
        self.favorite_artists = favorite_artists if favorite_artists is not None else []  # User's favorite artists

    def check_password(self, password):
        """
        Verify if the given password matches the user's password.

        Parameters:
        ----------
        password : str
            The password to verify.

        Returns:
        -------
        bool
            True if the passwords match, otherwise False.
        """
        return self.password == password

    def add_favorite_album(self, album):
        """
        Add an album to the user's list of favorite albums (maximum of 5).

        Parameters:
        ----------
        album : Album
            The album object to add to the user's favorites.

        Returns:
        -------
        None
        """
        if len(self.favorite_albums) < 5:
            self.favorite_albums.append(album)
            print(f"Album '{album.title}' added to {self.username}'s favorites.")
        else:
            print("You have already added 5 favorite albums.")

    def add_favorite_song(self, song):
        """
        Add a song to the user's list of favorite songs (maximum of 5).

        Parameters:
        ----------
        song : Song
            The song object to add to the user's favorites.

        Returns:
        -------
        None
        """
        if len(self.favorite_songs) < 5:
            self.favorite_songs.append(song)
            print(f"Song '{song.title}' added to {self.username}'s favorites.")
        else:
            print("You have already added 5 favorite songs.")

    def add_favorite_artist(self, artist):
        """
        Add an artist to the user's list of favorite artists (maximum of 5).

        Parameters:
        ----------
        artist : Artist
            The artist object to add to the user's favorites.

        Returns:
        -------
        None
        """
        if len(self.favorite_artists) < 5:
            self.favorite_artists.append(artist)
            print(f"Artist '{artist.name}' added to {self.username}'s favorites.")
        else:
            print("You have already added 5 favorite artists.")

    def to_dict(self):
        """
        Convert the User object into a dictionary representation.

        Returns:
        -------
        dict
            A dictionary containing the user's details and favorite items.
        """
        return {
            'user_id': self.user_id,  # User ID
            'username': self.username,  # Username
            'email': self.email,  # Email
            'password': self.password,  # Password
            'favorite_albums': [album.to_dict() for album in self.favorite_albums],  # Favorite albums as dictionaries
            'favorite_songs': [song.to_dict() for song in self.favorite_songs],  # Favorite songs as dictionaries
            'favorite_artists': [artist.to_dict() for artist in self.favorite_artists]  # Favorite artists as dictionaries
        }
