class Song:
    def __init__(self, id, title, artist, album, duration_ms, release_date=None):
        self.id = id
        self.title = title
        self.artist = artist
        self.album = album
        self.duration_ms = duration_ms
        self.release_date = release_date  

    def __repr__(self):
        return (f"Song(id={self.song_id}, title={self.title}, "
                f"artist={self.artist}, album={self.album}, duration={self.duration_ms} ms)")
    def to_dict(self):
        return {
        'id': self.id,
        'title': self.title,
        'artist': self.artist,
        'album': self.album,
        'duration_ms': self.duration_ms,
    }
