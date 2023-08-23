from find_track_info import *
from folder_file_path import path
import os

# Path to the directory containing your MP3 files
music_folder_path = path

# Iterate over the files in the folder
for filename in os.listdir(music_folder_path):
    # add more endswith for flac and so on
    if filename.endswith('.mp3'):
        # Print the file name before processing
        print("")
        print(f"Processing file: {filename}")

        # Build the full file path
        audio_file_path = os.path.join(music_folder_path, filename)

        # Rest of your existing code to process the file
        artist, title, album, release_date, track_number = find_song_info(ACOUSTID_API_KEY, audio_file_path)

        print("Artist:", artist)
        print("Title:", title)
        print("Album:", album)
        print("Release Date:", release_date)
        print("Track Number:", track_number)
        print("")
