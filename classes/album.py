class Album:
    """
    A class to represent a music album.

    Attributes:
    ----------
    id : int
        Unique identifier for the album.
    title : str
        Title of the album.
    artist : str
        Name of the artist or band who created the album.
    release_date : str
        The release date of the album (e.g., "YYYY-MM-DD").
    genre : str, optional
        Genre of the album (e.g., "Rock", "Pop"). Defaults to None.
    rating : Any
        User rating for the album, can be set externally. Defaults to None.
    """

    def __init__(self, id, title, artist, release_date, genre=None):
        """
        Initialize an Album object with the given attributes.

        Parameters:
        ----------
        id : int
            Unique identifier for the album.
        title : str
            Title of the album.
        artist : str
            Name of the artist or band who created the album.
        release_date : str
            The release date of the album (e.g., "YYYY-MM-DD").
        genre : str, optional
            Genre of the album (e.g., "Rock", "Pop"). Defaults to None.
        """
        self.id = id  # Unique identifier for the album
        self.title = title  # Album title
        self.artist = artist  # Artist or band name
        self.release_date = release_date  # Album release date
        self.genre = genre  # Genre of the album, optional
        self.rating = None  # Album rating, can be assigned later

    def to_dict(self):
        """
        Convert the Album object into a dictionary representation.

        Returns:
        -------
        dict
            A dictionary containing album details (title, artist, release date).
        """
        return {
            'title': self.title,  # Album title
            'artist': self.artist,  # Album artist
            'release_date': self.release_date  # Album release date
        }
