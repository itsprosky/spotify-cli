## spotify-cli

`spotify-cli` is a Python script for downloading Spotify tracks in MP3 format from YouTube.

Currently, only individual tracks are supported (playlists and albums are not supported yet).

It performs the following actions:

1. Parses the Spotify track URL to extract information: track title, artist, album, and release year.

2. Uses [`ytmusicapi`](https://github.com/sigma67/ytmusicapi) to search for the track on YouTube Music.

3. Downloads the track using [`yt-dlp`](https://github.com/yt-dlp/yt-dlp) and converts it to MP3.

4. Uses ffmpeg for conversion

---
# Installation
To use this script, you need to install [`ffmpeg`][(https://github.com/yt-dlp/yt-dlp](https://www.ffmpeg.org/download.html) and place the [`ffmpeg`][(https://github.com/yt-dlp/yt-dlp](https://www.ffmpeg.org/download.html) folder next to the script.
You also need to install the following modules:
```bash
pip install colorama requests beautifulsoup4 ytmusicapi yt-dlp
```
For now, the script is only designed for Windows.
