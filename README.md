## spotify-cli

`spotify-cli` — это скрипт Python для загрузки треков Spotify в формате MP3 через YouTube.

В настоящее время поддерживается загрузка только отдельных треков (плейлистов и альбомов пока нет).

Он выполняет следующие действия:

1. Анализирует ссылку на трек Spotify для извлечения информации: название трека, исполнитель, альбом, год выпуска.

2. Использует [`ytmusicapi`](https://github.com/sigma67/ytmusicapi) для поиска трека в YouTube Music.

3. Скачивает трек с помощью [`yt-dlp`](https://github.com/yt-dlp/yt-dlp) и конвертирует его в MP3.

4. Использует `ffmpeg` для конвертации

---
# Installation
Для работы необходимо установить и поместить папку [`ffmpeg`][(https://github.com/yt-dlp/yt-dlp](https://www.ffmpeg.org/download.html) рядом со скриптом.
Также необходимо установить модули
```bash
pip install colorama requests beautifulsoup4 ytmusicapi yt-dlp

Пока скрипт орриентировать только под Windows.
