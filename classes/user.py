import json

class User:
    def __init__(self, user_id, username, email, password):
        self.user_id = user_id
        self.username = username
        self.email = email
        self.password = password
        self.favorite_albums = []
        self.favorite_songs = []
        self.favorite_artists = []

    def check_password(self, password):
        return self.password == password

    def add_favorite_album(self, album):
        if len(self.favorite_albums) < 5:
            self.favorite_albums.append(album)
            print(f"Album '{album.title}' added to {self.username}'s favorites.")
        else:
            print("You have already added 5 favorite albums.")

    def add_favorite_song(self, song):
        if len(self.favorite_songs) < 5:
            self.favorite_songs.append(song)
            print(f"Song '{song.title}' added to {self.username}'s favorites.")
        else:
            print("You have already added 5 favorite songs.")

    def add_favorite_artist(self, artist):
        if len(self.favorite_artists) < 5:
            self.favorite_artists.append(artist)
            print(f"Artist '{artist.name}' added to {self.username}'s favorites.")
        else:
            print("You have already added 5 favorite artists.")

    def to_dict(self):
        return {
            'user_id': self.user_id,
            'username': self.username,
            'email': self.email,
            'password': self.password,
            'favorite_albums': [album.to_dict() for album in self.favorite_albums],
            'favorite_songs': [song.to_dict() for song in self.favorite_songs],
            'favorite_artists': [artist.to_dict() for artist in self.favorite_artists]
        }
