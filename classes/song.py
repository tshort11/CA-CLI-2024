class Song:
    """
    A class to represent a song.

    Attributes:
    ----------
    id : int
        Unique identifier for the song.
    title : str
        Title of the song.
    artist : str
        Name of the artist or band who performed the song.
    album : str
        Name of the album the song belongs to.
    duration_ms : int
        Duration of the song in milliseconds.
    release_date : str, optional
        Release date of the song (e.g., "YYYY-MM-DD"). Defaults to None.
    """

    def __init__(self, id, title, artist, album, duration_ms, release_date=None):
        """
        Initialize a Song object with the given attributes.

        Parameters:
        ----------
        id : int
            Unique identifier for the song.
        title : str
            Title of the song.
        artist : str
            Name of the artist or band who performed the song.
        album : str
            Name of the album the song belongs to.
        duration_ms : int
            Duration of the song in milliseconds.
        release_date : str, optional
            Release date of the song (e.g., "YYYY-MM-DD"). Defaults to None.
        """
        self.id = id  # Unique identifier for the song
        self.title = title  # Title of the song
        self.artist = artist  # Artist or band name
        self.album = album  # Album the song belongs to
        self.duration_ms = duration_ms  # Duration of the song in milliseconds
        self.release_date = release_date  # Optional release date of the song

    def __repr__(self):
        """
        Return a string representation of the Song object.

        Returns:
        -------
        str
            A string with detailed information about the Song object.
        """
        return (f"Song(id={self.id}, title='{self.title}', "
                f"artist='{self.artist}', album='{self.album}', "
                f"duration={self.duration_ms} ms, release_date={self.release_date})")

    def to_dict(self):
        """
        Convert the Song object into a dictionary representation.

        Returns:
        -------
        dict
            A dictionary containing the song's details (id, title, artist, album, duration, release_date).
        """
        return {
            'id': self.id,  # Song ID
            'title': self.title,  # Song title
            'artist': self.artist,  # Artist name
            'album': self.album,  # Album name
            'duration_ms': self.duration_ms,  # Duration in milliseconds
            'release_date': self.release_date  # Optional release date
        }
