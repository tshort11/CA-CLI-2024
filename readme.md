## Welcome to interlude!
This application allows users to discover and manage their favorite music, albums, and artists using the Spotify API

## Table of Contents
- [Installation Instructions](#installation-instructions)
- [Libraries](#dependencies)
- [System/Hardware Requirements](#systemhardware-requirements)
- [How to use](#How-to-use)
- [Features](#features)
- [License Information](#license-information)

## Instilation 
```
pip install -r requriements.txt
```

## Libraries 
The following libraries are required for the application to function correctly:

- json: For handling JSON data.
- os: For operating system interactions.
- requests: For making HTTP requests to the Spotify API.
- rich: For enhanced console output.
- colorama: For colored terminal text.
- prettytable: For displaying tabular data.
- your_custom_classes: Any custom classes you’ve implemented (e.g., User, Album, etc.).

## System/Hardware Requirements

To run this application, your system should meet the following requirements:

- Operating System: Windows, macOS, or Linux.
- Python: Version 3.7 or later

## How to use
### 1. User Account Management

- **Create an Account**:
  - When you launch the application, you will be presented with options to create an account or log in.
  - Select **1** for "Create Account".
  - Enter a username and a password when prompted.

- **Login**:
  - Select **2** for "Login".
  - Enter your username and password to access your profile.

### 2. Adding Favorite Albums

- **Add Favorite Album**:
  - After logging in, select **1** from the menu.
  - Enter the name of your favorite album when prompted.
  - The application will search for the album on Spotify.
  - Once found, you will be prompted to rate the album out of 5. Enter a rating between 0 and 5.

### 3. Adding Favorite Songs

- **Add Favorite Song**:
  - Select **2** from the menu.
  - Enter the name of your favorite song.
  - The application will search for the song on Spotify.
  - After finding it, rate the song out of 5 as prompted.

### 4. Adding Favorite Artists

- **Add Favorite Artist**:
  - Select **3** from the menu.
  - Enter the name of the artist you want to add to your favorites.
  - The application will search for the artist on Spotify and add them to your profile.

### 5. Discovering Music

- **Discover Music**:
  - Select **4** from the menu.
  - The application will display a list of new music releases. Each entry includes the album title, artist(s), release date, total tracks, and a link to listen on Spotify.

### 6. Viewing Your Favorites

- **View Your Favorites**:
  - Select **5** from the menu.
  - The application will display tables showing your favorite albums, songs, and artists along with their ratings.

### 7. Saving and Exiting

- **Save and Exit**:
  - Select **6** from the menu to save your user data and exit the application.
  - Your account information and favorites will be saved locally for future access.

### Tips for Best Experience

- Ensure you have a stable internet connection while using the application, as it interacts with the Spotify API for data.
- Remember to enter valid usernames and passwords that meet the application's requirements.
- Keep your dependencies up to date to ensure smooth functioning.

---

By following these instructions, you can fully utilize the features of the Music Recommendation CLI Application to manage and discover your favorite music!

## Features 

interlude! follows these features 

- User Account Management: Create and log in to user accounts.
- Favorite Albums: Add and rate your favorite albums.
- Favorite Songs: Add and rate your favorite songs.
- Favorite Artists: Add your favorite artists to your profile.
- Discover Music: Explore new releases and trending albums.
- View Profile Information: Check your saved favorites.
- Save User Data: User data is saved locally for easy retrieval.

## License Information

interlude! uses several third-party libraries. Below is a list of these libraries, their respective licenses, and a brief overview of the ethical considerations associated with their use.

### Third-Party Libraries

1. **requests**
   - **License**: Apache 2.0 License
   - **Ethical Consideration**: This license allows for both personal and commercial use, modification, and distribution. It promotes open-source collaboration while requiring proper attribution, ensuring that developers contribute back to the community.

2. **rich**
   - **License**: MIT License
   - **Ethical Consideration**: The MIT License is permissive, allowing for broad use and modification with minimal restrictions. This encourages sharing and innovation, which aligns with ethical software development practices.

3. **colorama**
   - **License**: MIT License
   - **Ethical Consideration**: Similar to rich, the MIT License ensures freedom in using the software, fostering an open and collaborative environment.

4. **prettytable**
   - **License**: MIT License
   - **Ethical Consideration**: The permissive nature of the MIT License allows developers to use and adapt the software without stringent restrictions, which is ethical as it promotes creativity and improvements.

5. **json**
   - **License**: Public Domain
   - **Ethical Consideration**: Since JSON is in the public domain, it can be used without any restrictions. This fosters a sense of community and cooperation among developers.

### Ethical Considerations

Using third-party libraries is ethical as long as you comply with their licenses. It is important to:

- **Attribution**: Give appropriate credit to the authors of the libraries used.
- **Adhere to License Terms**: Ensure compliance with the terms of the licenses, which may include sharing modifications under the same license or not using the libraries in ways that contradict their licenses.
- **Support Open Source**: Contributing to open-source projects and the community is a way to ethically engage with the software development ecosystem.

By using these libraries, you support the ethical principles of software development, which promote transparency, collaboration, and innovation.