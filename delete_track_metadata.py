import os
from mutagen.mp3 import MP3
from folder_file_path import *

# Path to the directory containing your MP3 files
music_folder_path = path 

# Iterate over the files in the folder
for filename in os.listdir(music_folder_path):
    if filename.endswith('.mp3'):
        # Build the full file path
        audio_file_path = os.path.join(music_folder_path, filename)

        try:
            # Load the audio file
            audio = MP3(audio_file_path)

            # Delete all metadata except audio
            audio.delete()
            
            # Save the changes back to the file
            audio.save()

            print(f"Metadata deleted for: {filename}")
        except Exception as e:
            print(f"Error processing {filename}: {e}")
