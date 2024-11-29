import json
import os
import requests
from rich.console import Console
from colorama import Fore, Back, Style
from prettytable import PrettyTable
from classes.user import User
from classes.album import Album
from classes.song import Song
from classes.artist import Artist  
from classes.spotify_api import SpotifyAPI

users = {}

def load_users(filename='users.json'):
    try:
        with open(filename, 'r') as f:
            user_data = json.load(f)
            for data in user_data:
                user = User(
                    user_id=data['user_id'], 
                    username=data['username'], 
                    email=data['email'], 
                    password=data['password']
                )
                users[user.username] = user
    except FileNotFoundError:
        print("No previous user data found. Starting fresh.")  
    except json.JSONDecodeError:
         print("Create an account to rate all your favourite music!") 



def save_users(filename='users.json'):
    try:
        with open(filename, 'w') as f:
            json.dump([user.to_dict() for user in users.values()], f)
        print("Thank you for sharing your favourites! Saved successfully.")
    except IOError as e:
        print(f"Error saving users: {e}")

def validate_input(prompt, type_=str, min_length=1, max_length=50):
    while True:
        user_input = input(prompt)
        if min_length <= len(user_input) <= max_length:
            try:
                return type_(user_input)
            except ValueError:
                print(f"Please enter a valid {type_.__name__}.")
        else:
            print(f"Input must be between {min_length} and {max_length} characters.")


def create_account(username, password):
    user_id = len(users) + 1  
    user = User(user_id, username, 'user@example.com', password)
    users[username] = user  
    print(f"Account created for {username}.")
    return user  

if os.path.exists('users.json'):
    load_users()
else:
    print("Create an account to rate all your favourite music!")


def login(username, password):
    user = users.get(username)
    if user and user.check_password(password):
        print(f"Welcome back {username}!")
        return True
    else:
        print("Invalid username or password.")
        return False

def account_setup():
    global users
    print("\nWelcome to" + Style.BRIGHT + " interlude!")
    print(Style.RESET_ALL)

    while True:
        print("1. Create Account")
        print("2. Login")
        print("3. Exit")

        choice = input("Enter your choice (1/2/3): ")

        if choice == '1':
            try:
                username = input("Enter a username: ")
                password = input("Enter a password: ")
                user_id = len(users) + 1
                user = User(user_id, username, 'user@example.com', password)
                create_account(username, password)
                users[username] = user  
                print(f"Welcome, {username}. Let's get started!")
                return user
            except Exception as e:
                print(f"Error creating account: {e}")

        elif choice == '2':
            try:
                username = input("Enter your username: ")
                password = input("Enter your password: ")
                if login(username, password):
                    user = users.get(username)
                    if user:
                        print(f"Login successful! Welcome, {username}.")
                        return user
                    else:
                        print("Error: User not found in the system.")
                else:
                    print("Login failed. Please try again.")
            except Exception as e:
                print(f"Error during login: {e}")

        elif choice == '3':
            print("Goodbye!")
            break

        else:
            print("Invalid choice. Please try again.")

def refresh_access_token(refresh_token):
    import requests
    try:
        url = 'https://accounts.spotify.com/api/token'
        headers = {
            'Authorization': 'Basic ' + base64.b64encode(f'{client_id}:{client_secret}'.encode()).decode()
        }
        payload = {
            'grant_type': 'refresh_token',
            'refresh_token': refresh_token
        }
        response = requests.post(url, headers=headers, data=payload)
        response.raise_for_status()  # Raises HTTPError if status is 4xx or 5xx
        return response.json().get('access_token')
    except requests.exceptions.RequestException as e:
        print(f"Failed to refresh token: {e}")
        return None


            
def add_favorite_album_with_rating(user, spotify):
    while len(user.favorite_albums) < 5:
        album_name = input("Enter your favourite albums name (or type 'exit' to stop): ")
        
        if album_name.lower() == 'exit':
            print("Excellent choices! \n Exiting album addition.")
            break

        print(f"Searching for album: {album_name}")
        album_info = spotify.search_album(album_name)
        print(f"Great choice! Heres the information on your album: {album_info}")

        if album_info and 'title' in album_info and 'artist' in album_info and 'release_date' in album_info:
            album = Album(1, album_info['title'], album_info['artist'], album_info['release_date'], "Unknown")

            while True:
                try:
                    rating = float(input("Rate this album out of 5: "))
                    if 0 <= rating <= 5:
                        album.rating = rating
                        user.add_favorite_album(album)
                        print(f"Added {album_name} with a rating of {rating}.")
                        break
                    else:
                        print("Please enter a rating between 0 and 5.")
                except ValueError:
                    print("Invalid rating. Please enter a number between 0 and 5.")

        else:
            print(f"Album '{album_name}' not found or data incomplete on Spotify.")

    if len(user.favorite_albums) >= 5:
        print("Amazing work! You have added 5 of your favorite albums!")

def add_favorite_song_with_rating(user, spotify):
    while len(user.favorite_songs) < 5:
        song_name = input("Enter your favourite songs name (or type 'exit' to stop): ")
        if song_name.lower() == 'exit':
            break 

        print(f"Searching for song: {song_name}")
        song_info = spotify.search_song(song_name)
        print(f"You picked: {song_info}")

        if song_info and 'title' in song_info and 'artist' in song_info and 'album' in song_info:
            song = Song(1, song_info['title'], song_info['artist'], song_info['album'], song_info['duration_ms'])

            while True:
                try:
                    rating = float(input("Rate this song out of 5: "))
                    if 0 <= rating <= 5:
                        song.rating = rating
                        user.add_favorite_song(song)
                        print(f"Added {song_name} with a rating of {rating}.")
                        break
                    else:
                        print("Please enter a rating between 0 and 5.")
                except ValueError:
                    print("Invalid rating. Please enter a number between 0 and 5.")
        else:
            print(f"Song '{song_name}' not found or data incomplete on Spotify.")

    if len(user.favorite_songs) >= 5:
        print("Amazing work! You have picked 5 of your favorite songs.")

def add_favorite_artist(user, spotify):
    artist_name = input("Enter the name of the artist to add to favorites: ")
    artist_info = spotify.search_artist(artist_name)
    if artist_info:
        artist = Artist(artist_info['id'], artist_info['name'], artist_info.get('genre', 'Unknown'))
        user.add_favorite_artist(artist)
        print(f"Artist '{artist}' added to {user.username}'s favorites.")
    else:
        print(f"Artist '{artist_name}' not found.")

def discover_music(user, spotify):
    print("\nNew Releases:\n")
    new_music = spotify.get_new_releases() 
    new_releases_table = PrettyTable()
    new_releases_table.field_names = ["Album Title", "Artist(s)", "Release Date", "Total Tracks", "Listen Here"]

    for album in new_music: 
        album_name = album.get('name', 'Unknown Album')
        release_date = album.get('release_date', 'Unknown Release Date')
        total_tracks = album.get('total_tracks', 'Unknown Track Count')
        artist_name = ', '.join(artist['name'] for artist in album.get('artists', []))
        album_url = album.get('external_urls', {}).get('spotify', 'No URL available')

    
        new_releases_table.add_row([album_name, artist_name, release_date, total_tracks, album_url])

    
    print(new_releases_table)

def view_user_info(user):
   
    albums_table = PrettyTable()
    albums_table.field_names = ["Album Title", "Artist", "Rating"]
    print("\nYour Profile Information:")
    print("\n Here are your Favorite Albums:")
    
    if user.favorite_albums:
        for album in user.favorite_albums:
            albums_table.add_row([album.title, album.artist, album.rating if hasattr(album, 'rating') else 'Not rated'])
        print(albums_table)
    else:
        print("uh oh! You haven't added any favorite albums yet.")
    
    songs_table = PrettyTable()
    songs_table.field_names = ["Song Title", "Artist", "Rating"]
    
    print("\nFavorite Songs:")
    if user.favorite_songs:
        for song in user.favorite_songs:
            songs_table.add_row([song.title, song.artist, song.rating if hasattr(song, 'rating') else 'Not rated'])
        print(songs_table)
    else:
        print("uh oh! You haven't added any favorite songs yet.")

    artists_table = PrettyTable()
    artists_table.field_names = ["Artist Name", "Genre"]
    
    print("\nFavorite Artists:")
    if user.favorite_artists:
        for artist in user.favorite_artists:
            artists_table.add_row([artist.name, artist.genre])
        print(artists_table)
    else:
        print("uh oh! You haven't added any favorite artists yet.")

def main():
    load_users()
    console = Console()
    spotify = SpotifyAPI(client_id='b822e6dd652d466581c81bee14a44cdc', client_secret='a5904fb2416a46eca583170f23ab2383', redirect_uri ='http://localhost:8888/callback')
    
    while True:
        user = account_setup()
        if user:
            while True:
                print("\nMenu:")
                print("1. Add a Favorite Album")
                print("2. Add a Favorite Song")
                print("3. Add a Favorite Artist")
                print("4. Discover Music")
                print("5. View Your Favourites")
                print("6. Save and Exit")
                choice = input("Choose an option: ")

                if choice == '1':
                    add_favorite_album_with_rating(user, spotify)
                elif choice == '2':
                    add_favorite_song_with_rating(user, spotify)
                elif choice == '3':
                    add_favorite_artist(user, spotify)
                elif choice == '4':
                    discover_music(user, spotify)
                elif choice == '5':
                    view_user_info(user)
                elif choice == '6':
                    save_users()
                    print("Exiting...")
                    return
                else:
                    print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()