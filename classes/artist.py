class Artist:
    """
    A class to represent a musical artist.

    Attributes:
    ----------
    id : int
        Unique identifier for the artist.
    name : str
        Name of the artist or band.
    genre : str, optional
        Genre associated with the artist (e.g., "Pop", "Rock"). Defaults to None.
    """

    def __init__(self, id, name, genre=None):
        """
        Initialize an Artist object with the given attributes.

        Parameters:
        ----------
        id : int
            Unique identifier for the artist.
        name : str
            Name of the artist or band.
        genre : str, optional
            Genre associated with the artist. Defaults to None.
        """
        self.id = id  # Unique identifier for the artist
        self.name = name  # Name of the artist or band
        self.genre = genre  # Genre of the artist, optional

    def __str__(self):
        """
        Return a string representation of the Artist object.

        Returns:
        -------
        str
            A string containing the artist's name and genre (if available).
        """
        return f"{self.name} (Genre: {self.genre if self.genre else 'Unknown'})"

    def to_dict(self):
        """
        Convert the Artist object into a dictionary representation.

        Returns:
        -------
        dict
            A dictionary containing the artist's id, name, and genre.
        """
        return {
            'id': self.id,  # Artist ID
            'name': self.name,  # Artist name
            'genre': self.genre  # Artist genre
        }
