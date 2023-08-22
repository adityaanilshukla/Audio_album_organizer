import acoustid

# import API key
# make an api_key.py file for your own copy
from api_key import ACOUSTID_API_KEY

#test name to be changed later
audio_file_path = 'audioFile.mp3'

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
        for recording in match['recordings']:
            song_title = recording.get('title', 'N/A')
            if song_title != 'N/A':
                song_titles.append(song_title)

    # the correct one is prob the most common val
    song_title = most_common(song_titles)
    return song_title



# get the song artist from the matches
def get_song_artist(recording_matches):

    song_artists = []
    for match in recording_matches['results']:
        for recording in match['recordings']:
            artist_names = [artist['name'] for artist in recording.get('artists', [])]
            song_artists.extend(artist_names)


    # the correct one is prob the most common val
    song_artist = most_common(song_artists)
    return song_artist

# find the songs info for autocategorizing
# TODO: Make this function find genre album, album cover and so on
# TODO: Make this function handle errors

def find_song_info(ACOUSTID_API_KEY,file_path):
    
    duration, fingerprint = acoustid.fingerprint_file(file_path)
    
    recording_matches = get_recording_matches(ACOUSTID_API_KEY, fingerprint, duration)

    artist = get_song_artist(recording_matches)
    title = get_song_title(recording_matches)

    return artist, title


artist,title = find_song_info(ACOUSTID_API_KEY, audio_file_path)

print(artist, title)

