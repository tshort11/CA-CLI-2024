class Album:
    def __init__(self, id, title, artist, release_date, genre=None):
        self.id = id
        self.title = title
        self.artist = artist
        self.release_date = release_date
        self.genre = genre  # Default genre to None
        self.rating = None



    def to_dict(self):
        return {
            'title': self.title,
            'artist': self.artist,
            'release_date': self.release_date
        }
