import os
import subprocess
import json

pullDataFromQuest = True

if pullDataFromQuest:
    # Step 1: List all the custom levels in the SongLoader folder on the Quest using adb

    result = subprocess.run(["adb", "shell","ls", "/sdcard/ModData/com.beatgames.beatsaber/Mods/SongLoader/CustomLevels/"], capture_output=True, text=True)
    folders = result.stdout.strip().split("\n")

    # Step 2: Pull all the custom levels from the Quest using adb

    os.makedirs("BeatMaps", exist_ok=True)
    for folder in folders:
        src_folder = f"/sdcard/ModData/com.beatgames.beatsaber/Mods/SongLoader/CustomLevels/{folder}"
        dst_folder = f"BeatMaps/{folder}"
        subprocess.run(["adb", "pull", src_folder, dst_folder])

# Step 3: Read all the song names and author names from the info.dat files of each map
songs = []
for root, dirs, files in os.walk("BeatMaps"):
    for file in files:
        if file.endswith("info.dat") or file.endswith("Info.dat"):
            with open(os.path.join(root, file), "r", encoding="utf8") as f:
                info = json.load(f)
                try:
                    song = info["_songName"]
                    author = info["_songAuthorName"]
                    filename=info["_songFilename"]
                    songs.append((root, song, author, filename))
                    print(f"Found {song} by {author}")
                    break
                except:
                    print("An error occured when reading a beatmap:")
                    print(info)
            break
# Step 4: Save all the songs into a folder with the correct names
os.makedirs("Playlist", exist_ok=True)
i=0
for song in songs:
    try:
        src_path = os.path.join(song[0], song[3])
        dst_path = os.path.join(".\\Playlist", f"{song[1]} - {song[2]}.ogg")
        if os.path.exists(dst_path):
            continue
        command = f'copy "{src_path}" "{dst_path}"'
        #print(command)
        #subprocess.run(["copy", f'"{src_path}"', f'"{dst_path}"']) # This doesn't work for some reason
        os.system(command)
        i+=1
    except Exception as e:
        print(f"Failed to copy {song[1]} - {song[2]}: {e}")
        print(f"Source: {src_path}")
        print(f"Destination: {dst_path}")
actualSongs = os.listdir("Playlist")
print(f"{len(actualSongs)} songs were copied, {len(songs)-len(actualSongs)} songs encountered errors or were duplicates.")