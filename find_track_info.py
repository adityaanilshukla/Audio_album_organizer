import acoustid

# import API key
# make an api_key.py file for your own copy
from api_key import *
import re
import requests
from base64 import b64encode

from spotify_keys import *

# remove random strings in song name that make it hard to determine songs/album metadata
def clean_up_song_name(song_name):
    # Remove text enclosed in parentheses
    cleaned_name = re.sub(r'\([^)]*\)', '', song_name)
    # Remove leading and trailing spaces
    cleaned_name = cleaned_name.strip()
    return cleaned_name


# find matches in acoustid's database
def get_recording_matches(ACOUSTID_API_KEY, fingerprint, duration):
    return acoustid.lookup(ACOUSTID_API_KEY, fingerprint, duration)

# get most common value in list
def most_common(lst):
    return max(set(lst), key=lst.count)

# get the song title from the matches
def get_song_title(recording_matches):
    song_titles = []
    for match in recording_matches['results']:
        if 'recordings' in match:  # Check if 'recordings' key is present
            for recording in match['recordings']:
                song_title = recording.get('title', 'N/A')
                if song_title != 'N/A':
                    song_titles.append(song_title)

    if song_titles:
        song_title = most_common(song_titles)
        return song_title
    else:
        return 'N/A'


# get the song artist from the matches
def get_song_artist(recording_matches):
    song_artists = []
    for match in recording_matches['results']:
        if 'recordings' in match:  # Check if 'recordings' key is present
            for recording in match['recordings']:
                artist_names = [artist['name'] for artist in recording.get('artists', [])]
                song_artists.extend(artist_names)

    if song_artists:
        song_artist = most_common(song_artists)
        return song_artist
    else:
        return 'N/A'



def get_spotify_access_token(client_id, client_secret):
    auth_str = f'{client_id}:{client_secret}'
    auth_bytes = auth_str.encode('utf-8')
    auth_base64 = b64encode(auth_bytes).decode('utf-8')
    
    headers = {
        'Authorization': f'Basic {auth_base64}'
    }
    
    data = {
        'grant_type': 'client_credentials'
    }
    
    response = requests.post('https://accounts.spotify.com/api/token', headers=headers, data=data)
    token_data = response.json()
    
    access_token = token_data.get('access_token')
    return access_token



def pull_spotify_metadata(artist, title):
    access_token = get_spotify_access_token(SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECRET)
    
    headers = {
        'Authorization': f'Bearer {access_token}'
    }
    
    params = {
        'q': f'artist:"{artist}" track:"{title}"',
        'type': 'track',
        'limit': 1
    }

    try:
        response = requests.get(f'{SPOTIFY_API_URL}search', headers=headers, params=params)
        data = response.json()

        if 'tracks' in data and 'items' in data['tracks'] and len(data['tracks']['items']) > 0:
            track_info = data['tracks']['items'][0]
            album = track_info['album']['name']
            release_date = track_info['album']['release_date'][:4]
            track_number = track_info['track_number']
            return album, release_date, track_number

    except requests.RequestException:
        pass

    return 'N/A', 'N/A', 'N/A'


# find the songs info for autocategorizing
# TODO: Make this function find genre and album cover and so on
# TODO: Make this function handle errors


def find_song_info(ACOUSTID_API_KEY, file_path):

    duration, fingerprint = acoustid.fingerprint_file(file_path)
    
    recording_matches = get_recording_matches(ACOUSTID_API_KEY, fingerprint, duration)

    artist = get_song_artist(recording_matches)
    title = clean_up_song_name(get_song_title(recording_matches))  # remove random strings in song name
    
    album, release_date, track_number = 'N/A', 'N/A', 'N/A'  # Default values
    
    if artist != 'N/A' and title != 'N/A':
        album, release_date, track_number = pull_spotify_metadata(artist, title)
    
    return artist, title, album, release_date, track_number

