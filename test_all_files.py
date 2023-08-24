from find_track_info import *
from folder_file_path import path

# for writing metadata to music file
from mutagen.easyid3 import EasyID3
from mutagen.id3._util import ID3NoHeaderError

import os # for routing file path
import socket #check if internet connection exists

import time # count time to wait for internet connection


def check_connection():
    try:
        # Create a socket object and connect to a well-known host (Googlefrom mutagen.id3 import ID3NoHeaderErrorfrom mutagen.id3 import ID3NoHeaderErrorfrom mutagen.id3 import ID3NoHeaderErrorfrom mutagen.id3 import ID3NoHeaderError DNS)
        socket.create_connection(("8.8.8.8", 53), timeout=2)
        return True
    except OSError:
        pass
    return False

def does_mp3_metadata_contain_unknowns(mp3_metadata):
       for value in mp3_metadata.values():
        if value == "N/a":
            return True
        return False


# Path to the directory containing your MP3 files
music_folder_path = path


# Iterate over the files in the folder
for filename in os.listdir(music_folder_path):
    # add more endswith for flac and so on
    if filename.endswith('.mp3'):
        while True:
            # Check internet connection before starting process
            connected = check_connection()

            if connected:
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

                if title != "N/A":
                    new_filename = title + ".mp3"
                    
                    try:
                        os.rename(os.path.join(music_folder_path, filename),
                                  os.path.join(music_folder_path, new_filename))

                        mp3 = EasyID3(os.path.join(music_folder_path, new_filename))
                        mp3["title"] = title
                        if artist != "N/A":
                            mp3["artist"] = artist
                        if album != "N/A":
                            mp3["album"] = album
                        mp3.save()
                    except (ID3NoHeaderError, FileNotFoundError):
                        print(f"Skipping {new_filename} due to missing ID3 tag header or file not found.")
                
                # Move to the next file in the loop
                break
            else:
                print("No internet connection. Waiting for 15 seconds...")
                time.sleep(15)

print("Finished processing all files.")

