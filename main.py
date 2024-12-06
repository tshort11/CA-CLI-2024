import json
import os
import sys
import requests
from rich.console import Console
from colorama import Fore, Back, Style
from prettytable import PrettyTable
from classes.user import User
from classes.album import Album
from classes.song import Song
from classes.artist import Artist  
from classes.spotify_api import SpotifyAPI

# Dictionary to store user objects indexed by their username.
users = {}

# Constants to store client id and secret for spotify API.
client_id='b822e6dd652d466581c81bee14a44cdc'
client_secret='a5904fb2416a46eca583170f23ab2383'

# Function to load user data from a JSON file
def load_users(filename='users.json'):
    """
    Load user data from a JSON file into the 'users' dictionary.
    
    Purpose:
        Reads stored user data from a JSON file to initialize application state.

    Inputs:
        filename (str): Name of the JSON file storing user data.

    Outputs:
        Updates the global 'users' dictionary with User objects.

    Notes:
        If the file does not exist, an appropriate message is displayed.
        If the file has invalid JSON, it prompts the user to start fresh.
    """
    try:
        with open(filename, 'r') as f:
            user_data = json.load(f)
            for data in user_data:
                user = User(
                    user_id=data['user_id'], 
                    username=data['username'], 
                    email=data['email'], 
                    password=data['password'],
                    favorite_albums=data.get('favorite_albums', []),
                    favorite_songs=data.get('favorite_songs', []),
                    favorite_artists=data.get('favorite_artists', [])
                    
                )
                users[user.username] = user
    except FileNotFoundError:
        print("No previous user data found. Starting fresh.")  
    except json.JSONDecodeError:
        print("Create an account to rate all your favourite music!") 


# Function to save user data to a JSON file
def save_users(filename='users.json'):
    """
    Save all user data to a JSON file.
    
    Purpose:
        Writes the current state of the 'users' dictionary to a JSON file to persist data.

    Inputs:
        filename (str): Name of the JSON file to save user data to.

    Outputs:
        A JSON file containing serialized user information.

    Notes:
        Each User object is converted to a dictionary format before saving.
        If an IOError occurs, it prints an error message.
    """
    try:
        with open(filename, 'w') as f:
            json.dump([user.to_dict() for user in users.values()], f)
        print("Thank you for sharing your favourites! Saved successfully.")
    except IOError as e:
        print(f"Error saving users: {e}")


# Function to validate user input
def validate_input(prompt, type_=str, min_length=1, max_length=50):
    """
    Validate user input based on type and length constraints.

    Purpose:
        Ensures user input meets specified criteria and converts it to the expected type.

    Inputs:
        prompt (str): Message to display to the user.
        type_ (type): Expected data type of the input.
        min_length (int): Minimum length of the input.
        max_length (int): Maximum length of the input.

    Outputs:
        Returns user input converted to the specified type.

    Notes:
        Re-prompts the user if input is invalid.
    """
    while True:
        user_input = input(prompt)
        if min_length <= len(user_input) <= max_length:
            try:
                return type_(user_input)
            except ValueError:
                print(f"Please enter a valid {type_.__name__}.")
        else:
            print(f"Input must be between {min_length} and {max_length} characters.")


# Function to create a new user account
def create_account(username, password):
    """
    Create a new user account and add it to the system.

    Purpose:
        Generates a new User object and stores it in the 'users' dictionary.

    Inputs:
        username (str): Desired username for the account.
        password (str): Desired password for the account.

    Outputs:
        User: The created User object.

    Notes:
        Each user is assigned a unique ID based on the current number of users.
        Prints a success message upon account creation.
    """
    user_id = len(users) + 1  
    user = User(user_id, username, 'user@example.com', password)
    users[username] = user  
    print(f"Account created for {username}.")
    return user  


# Check if a JSON file exists to load users, otherwise start fresh
if os.path.exists('users.json'):
    load_users()
else:
    print("Create an account to rate all your favourite music!")


# Function to authenticate a user
def login(username, password):
    """
    Authenticate a user by verifying their credentials.

    Purpose:
        Matches input username and password with stored user data.

    Inputs:
        username (str): The username provided during login.
        password (str): The password provided during login.

    Outputs:
        bool: True if authentication is successful, False otherwise.

    Notes:
        Prints a success message if login is successful, or an error message if not.
    """
    user = users.get(username)
    if user and user.check_password(password):
        print(f"Welcome back {username}!")
        return True
    else:
        print("Invalid username or password.")
        return False


# Function to handle user account setup (creation or login)
def account_setup():
    """
    Provide options to create a new account, log in, or exit.

    Purpose:
        Manages the initial interaction for account creation or login.

    Outputs:
        User: Returns the logged-in or newly created User object.

    Notes:
        Includes error handling for account creation and login processes.
    """
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
                return create_account(username, password)
            except Exception as e:
                print(f"Error creating account: {e}")

        elif choice == '2':
            try:
                username = input("Enter your username: ")
                password = input("Enter your password: ")
                if login(username, password):
                    return users.get(username)
            except Exception as e:
                print(f"Error during login: {e}")

        elif choice == '3':
            print("Goodbye!")
            sys.exit()

        else:
            print("Invalid choice. Please try again.")
    
    
# Function to refresh Spotify API access tokens
def refresh_access_token(refresh_token):
    """
    Refresh the Spotify API access token using a refresh token.

    Purpose:
        Maintains session validity by generating a new access token.

    Inputs:
        refresh_token (str): Spotify API refresh token.

    Outputs:
        str: The new access token, or None if the refresh fails.

    Notes:
        Uses base64 encoding for client credentials and makes an API POST request.
    """
    import base64
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
        response.raise_for_status()
        return response.json().get('access_token')
    except requests.exceptions.RequestException as e:
        print(f"Failed to refresh token: {e}")
        return None

def add_favorite_album_with_rating(user, spotify):
    """
    Add a favorite album with a user-provided rating.

    Purpose:
        Allows the user to search for albums using the Spotify API, 
        view album details, and add them to their list of favorite albums with a rating.

    Inputs:
        user (User): The currently logged-in user object.
        spotify (SpotifyAPI): An instance of the Spotify API wrapper for searching album details.

    Behavior:
        - Prompts the user for album names until they add 5 favorite albums or choose to exit.
        - Validates album information retrieved from the Spotify API.
        - Prompts the user to provide a rating between 0 and 5 for each album.
        - Adds the album with its rating to the user's list of favorite albums.

    Outputs:
        Updates the user's favorite albums list with album objects and ratings.
        Prints messages to indicate progress, success, or errors.
    """
    while len(user.favorite_albums) < 5:
        # Prompt the user for an album name
        album_name = input("Enter your favourite album's name (or type 'exit' to stop): ")
        
        if album_name.lower() == 'exit':
            print("Excellent choices! \n Exiting album addition.")
            break

        print(f"Searching for album: {album_name}")
        # Use the Spotify API to search for the album
        album_info = spotify.search_album(album_name)
        print(f"Great choice! Here's the information on your album: {album_info}")

        if album_info and 'title' in album_info and 'artist' in album_info and 'release_date' in album_info:
            # Create an Album object if album details are complete
            album = Album(1, album_info['title'], album_info['artist'], album_info['release_date'], "Unknown")

            while True:
                try:
                    # Prompt the user for a rating between 0 and 5
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
    """
    Add a favorite song with a user-provided rating.

    Purpose:
        Enables the user to search for songs using the Spotify API,
        view song details, and add them to their list of favorite songs with a rating.

    Inputs:
        user (User): The currently logged-in user object.
        spotify (SpotifyAPI): An instance of the Spotify API wrapper for searching song details.

    Behavior:
        - Prompts the user for song names until they add 5 favorite songs or choose to exit.
        - Validates song information retrieved from the Spotify API.
        - Prompts the user to provide a rating between 0 and 5 for each song.
        - Adds the song with its rating to the user's list of favorite songs.

    Outputs:
        Updates the user's favorite songs list with song objects and ratings.
        Prints messages to indicate progress, success, or errors.
    """
    while len(user.favorite_songs) < 5:
        # Prompt the user for a song name
        song_name = input("Enter your favourite song's name (or type 'exit' to stop): ")
        if song_name.lower() == 'exit':
            break 

        print(f"Searching for song: {song_name}")
        # Use the Spotify API to search for the song
        song_info = spotify.search_song(song_name)
        print(f"You picked: {song_info}")

        if song_info and 'title' in song_info and 'artist' in song_info and 'album' in song_info:
            # Create a Song object if song details are complete
            song = Song(1, song_info['title'], song_info['artist'], song_info['album'], song_info['duration_ms'])

            while True:
                try:
                    # Prompt the user for a rating between 0 and 5
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
    """
    Add a favorite artist to the user's profile.

    Purpose:
        Enables the user to search for artists using the Spotify API
        and add them to their list of favorite artists.

    Inputs:
        user (User): The currently logged-in user object.
        spotify (SpotifyAPI): An instance of the Spotify API wrapper for artist searches.

    Behavior:
        - Prompts the user for an artist name.
        - Uses the Spotify API to fetch artist details.
        - If the artist is found, creates an Artist object and adds it to the user's favorites list.
        - Displays success or error messages based on the search result.

    Outputs:
        Updates the user's favorite artists list.
        Prints success messages for additions or error messages for missing artists.
    """
    # Prompt the user to enter the name of the artist to be added
    artist_name = input("Enter the name of the artist to add to favorites: ")
    # Use the Spotify API to search for the artist by name
    artist_info = spotify.search_artist(artist_name)
    if artist_info:
        # Create an Artist object if the search was successful
        artist = Artist(artist_info['id'], artist_info['name'], artist_info.get('genre', 'Unknown'))
        # Add the artist to the user's list of favorite artists
        user.add_favorite_artist(artist)
        print(f"Artist '{artist.name}' added to {user.username}'s favorites.")
    else:
        # Print an error message if the artist was not found
        print(f"Artist '{artist_name}' not found.")


def discover_music(user, spotify):
    """
    Display new music releases for the user.

    Purpose:
        Uses the Spotify API to retrieve and display a list of the latest music releases.
        Provides details like album name, artist(s), release date, and a Spotify URL.

    Inputs:
        user (User): The currently logged-in user object.
        spotify (SpotifyAPI): An instance of the Spotify API wrapper for fetching new releases.

    Behavior:
        - Fetches new music releases using the Spotify API.
        - Formats the data into a table using PrettyTable.
        - Displays the formatted table to the user.

    Outputs:
        Prints a table of new music releases, including album details and a URL to listen.
    """
    print("\nNew Releases:\n")
    # Fetch new music releases using the Spotify API
    new_music = spotify.get_new_releases()
    # Initialize a PrettyTable to display the results in a tabular format
    new_releases_table = PrettyTable()
    new_releases_table.field_names = ["Album Title", "Artist(s)", "Release Date", "Total Tracks", "Listen Here"]

    # Populate the table with album data
    for album in new_music:
        album_name = album.get('name', 'Unknown Album')  # Get the album name or default to 'Unknown'
        release_date = album.get('release_date', 'Unknown Release Date')  # Get the release date
        total_tracks = album.get('total_tracks', 'Unknown Track Count')  # Get the number of tracks
        # Combine all artist names into a single string
        artist_name = ', '.join(artist['name'] for artist in album.get('artists', []))
        # Get the Spotify URL for the album
        album_url = album.get('external_urls', {}).get('spotify', 'No URL available')

        # Add the album information as a row in the table
        new_releases_table.add_row([album_name, artist_name, release_date, total_tracks, album_url])

    # Display the table
    print(new_releases_table)


def view_user_info(user):
    """
    Display the user's profile information, including their favorite albums, songs, and artists.

    Purpose:
        Retrieves and displays the user's stored favorite albums, songs, and artists in a tabular format.

    Inputs:
        user (User): The currently logged-in user object.

    Behavior:
        - Checks if the user has favorite albums, songs, or artists.
        - Displays each category using PrettyTable with appropriate column headings.
        - Displays a message if no favorites are found in a category.

    Outputs:
        Prints tables with the user's favorite albums, songs, and artists.
        Prints messages for categories with no entries.
    """
    # Display favorite albums
    albums_table = PrettyTable()
    albums_table.field_names = ["Album Title", "Artist", "Rating"]
    print("\nYour Profile Information:")
    print("\n Here are your Favorite Albums:")

    if user.favorite_albums:
        # Add each favorite album to the table
        for album in user.favorite_albums:
            albums_table.add_row([album.title, album.artist, album.rating if hasattr(album, 'rating') else 'Not rated'])
        print(albums_table)
    else:
        # Print a message if no favorite albums are found
        print("Uh oh! You haven't added any favorite albums yet.")

    # Display favorite songs
    songs_table = PrettyTable()
    songs_table.field_names = ["Song Title", "Artist", "Rating"]

    print("\nFavorite Songs:")
    if user.favorite_songs:
        # Add each favorite song to the table
        for song in user.favorite_songs:
            songs_table.add_row([song.get('title'), song.get('artist'), song.get('rating') if hasattr(song, 'rating') else 'Not rated'])
        print(songs_table)
    else:
        # Print a message if no favorite songs are found
        print("Uh oh! You haven't added any favorite songs yet.")

    # Display favorite artists
    artists_table = PrettyTable()
    artists_table.field_names = ["Artist Name", "Genre"]

    print("\nFavorite Artists:")
    if user.favorite_artists:
        # Add each favorite artist to the table
        for artist in user.favorite_artists:
            artists_table.add_row([artist.name, artist.genre])
        print(artists_table)
    else:
        # Print a message if no favorite artists are found
        print("Uh oh! You haven't added any favorite artists yet.")


def main():
    """
    Main function to drive the application.

    Purpose:
        Handles the overall flow of the application, including loading user data,
        managing user account setup, and presenting the main menu for app functionality.

    Behavior:
        - Loads existing user data from a JSON file at startup.
        - Initializes necessary components like the console and Spotify API wrapper.
        - Provides a continuous loop for user interaction with the main menu.
        - Based on the user's menu choice, calls appropriate functions for app features.
        - Ensures user data is saved before exiting the application.

    Outputs:
        Displays a menu and executes corresponding app functionalities based on user input.
        Saves user data upon exit.
    """
    # Load user data from the JSON file at startup
    load_users()
    # Initialize the rich console for enhanced terminal output
    console = Console()
    # Create an instance of the Spotify API wrapper with required credentials
    spotify = SpotifyAPI(client_id=client_id, client_secret=client_secret, redirect_uri='http://localhost:8888/callback')
    
    while True:
        # Prompt the user for account setup (login or create account)
        user = account_setup()
        if user:
            # Main menu loop for user interaction
            while True:
                # Display the main menu
                print("\nMenu:")
                print("1. Add a Favorite Album")
                print("2. Add a Favorite Song")
                print("3. Add a Favorite Artist")
                print("4. Discover Music")
                print("5. View Your Favourites")
                print("6. Save and Exit")
                # Prompt the user to choose an option
                choice = input("Choose an option: ")

                # Call the appropriate function based on the user's choice
                if choice == '1':
                    # Add a favorite album with rating
                    add_favorite_album_with_rating(user, spotify)
                elif choice == '2':
                    # Add a favorite song with rating
                    add_favorite_song_with_rating(user, spotify)
                elif choice == '3':
                    # Add a favorite artist
                    add_favorite_artist(user, spotify)
                elif choice == '4':
                    # Discover new music using the Spotify API
                    discover_music(user, spotify)
                elif choice == '5':
                    # View user's favorite albums, songs, and artists
                    view_user_info(user)
                elif choice == '6':
                    # Save user data and exit the application
                    save_users()
                    print("Exiting...")
                    return
                else:
                    # Handle invalid menu options
                    print("Invalid choice. Please try again.")


# Entry point for the script
if __name__ == "__main__":
    """
    Purpose:
        Ensures the main function is only executed when the script is run directly,
        and not when imported as a module.

    Behavior:
        Calls the main function to start the application.
    """
    main()
