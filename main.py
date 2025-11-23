import os
import re
from urllib.parse import urlparse
from colorama import Fore, Style, init, Back
import requests
from bs4 import BeautifulSoup
from ytmusicapi import YTMusic
import yt_dlp
init()

os.system('cls')
os.system('title spotify-cli')

ascii_art = Fore.LIGHTGREEN_EX + r"""                                                          
  ▄▄▄▄ ▄▄▄▄   ▄▄▄ ▄▄▄▄▄▄ ▄▄ ▄▄▄▄▄ ▄▄ ▄▄      ▄▄▄▄ ▄▄    ▄▄ 
 ███▄▄ ██▄█▀ ██▀██  ██   ██ ██▄▄  ▀███▀ ▄▄▄ ██▀▀▀ ██    ██""" + Fore.GREEN + """
 ▄▄██▀ ██    ▀███▀  ██   ██ ██      █       ▀████ ██▄▄▄ ██

""" + Style.RESET_ALL
print(ascii_art)

url = input(" " + Back.LIGHTGREEN_EX + Fore.BLACK + "[?]" + Back.GREEN + Fore.BLACK + "Enter Spotify track URL: " + Style.RESET_ALL)
if not url.startswith("https://open.spotify.com"):
    print(" " + Back.LIGHTRED_EX + Fore.BLACK + "[!]" + Back.RED + Fore.BLACK +
          "Only open.spotify.com URLs are supported!" + Style.RESET_ALL)

parsed = urlparse(url)
domain = parsed.netloc or "unknown"

track_type = "Unknown"
track_name = "Unknown"
artist = "Unknown"
album = "Unknown"
year = "Unknown"
creator = "Unknown"

try:
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
    with requests.get(url, headers=headers, stream=True) as r:
        r.raise_for_status()
        total_length = int(r.headers.get('content-length', 0))
        downloaded = 0
        content = b""
        for chunk in r.iter_content(chunk_size=1024):
            if chunk:
                content += chunk
                downloaded += len(chunk)
                bar_length = 20
                filled_length = int(bar_length * downloaded // total_length) if total_length else bar_length
                percent = int(downloaded * 100 // total_length) if total_length else 100
                bar = "█" * filled_length + "-" * (bar_length - filled_length)
                print(f"\rProcessing... [{bar}] {percent}% {domain}", end="")
        print()
    soup = BeautifulSoup(content, "html.parser")
    if "track" in url:
        track_type = "Track"
    elif "playlist" in url:
        track_type = "Playlist"

    meta_title = soup.find("meta", property="og:title")
    if meta_title:
        track_name = meta_title.get("content", "Unknown")
    if track_type == "Track":
        meta_desc = soup.find("meta", property="og:description")
        if meta_desc:
            desc = meta_desc.get("content", "")
            parts = [p.strip() for p in desc.split("·")]
            if len(parts) >= 4:
                artist = " · ".join(parts[:-3])
                album = parts[-3]
                year = parts[-1]
            elif len(parts) == 3:
                artist = parts[0]
                album = parts[1]
                year = "Unknown"
            elif len(parts) == 2:
                artist = parts[0]
                album = "Unknown"
                year = "Unknown"
            else:
                artist = desc
    elif track_type == "Playlist":
        meta_creator = soup.find("meta", property="music:creator")
        if meta_creator:
            creator = meta_creator.get("content", "Unknown")
except Exception as e:
    track_name = f"Error: {e}"

os.system('cls')
print(ascii_art)

print(" " + Back.LIGHTGREEN_EX + Fore.BLACK + "[+]" + Back.GREEN + Fore.BLACK + "Type: " + track_type + Style.RESET_ALL)
if track_type == "Track":
    print(" " + Back.LIGHTGREEN_EX + Fore.BLACK + "[+]" + Back.GREEN + Fore.BLACK + "Name: " + track_name + Style.RESET_ALL)
    print(" " + Back.LIGHTGREEN_EX + Fore.BLACK + "[+]" + Back.GREEN + Fore.BLACK + "Artist: " + artist + Style.RESET_ALL)
    print(" " + Back.LIGHTGREEN_EX + Fore.BLACK + "[+]" + Back.GREEN + Fore.BLACK + "Album: " + album + Style.RESET_ALL)
    print(" " + Back.LIGHTGREEN_EX + Fore.BLACK + "[+]" + Back.GREEN + Fore.BLACK + "Year: " + year + Style.RESET_ALL)
elif track_type == "Playlist":
    print(" " + Back.LIGHTGREEN_EX + Fore.BLACK + "[+]" + Back.GREEN + Fore.BLACK + "Name: " + track_name + Style.RESET_ALL)
    print(" " + Back.LIGHTGREEN_EX + Fore.BLACK + "[+]" + Back.GREEN + Fore.BLACK + "Creator: " + creator + Style.RESET_ALL)

yt = YTMusic()

if track_type == "Track":
    results = yt.search(f"{track_name} {artist}", filter='songs')
    if results:
        first = results[0]
        video_id = first['videoId']
        yt_url = f"https://www.youtube.com/watch?v={video_id}"
        if not os.path.exists("downloads"):
            os.makedirs("downloads")
        safe_name = re.sub(r'[\\/*?:"<>|]', '', f"{track_name} - {artist}")
        ydl_opts = {
		    'format': 'bestaudio/best',
		    'outtmpl': f'downloads/{safe_name}.%(ext)s',
		    'quiet': True,
		    'no_warnings': True,
		    'restrictfilenames': True,
		    'ffmpeg_location': os.path.join(os.getcwd(), "ffmpeg", "bin", "ffmpeg.exe"),
		    'postprocessors': [{
		        'key': 'FFmpegExtractAudio',
		        'preferredcodec': 'mp3',
		        'preferredquality': '192',
		    }],
		}

        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([yt_url])
            os.system('cls')
            print(ascii_art)
            print(" " + Back.LIGHTGREEN_EX + Fore.BLACK + "[OK]" + Back.GREEN + Fore.BLACK + f"Downloaded: downloads/{safe_name}.mp3"   + Style.RESET_ALL)
        except Exception as e:
            os.system('cls')
            print(ascii_art)
            print(" " + Back.LIGHTRED_EX + Fore.BLACK + "[!]" + Back.RED + Fore.BLACK + f"Error downloading: {e}" + Style.RESET_ALL)
    else:
        print(" " + Back.LIGHTRED_EX + Fore.BLACK + "[!]" + Back.RED + Fore.BLACK +
              "NO YOUTUBE MUSIC FOUND!" + Style.RESET_ALL)
