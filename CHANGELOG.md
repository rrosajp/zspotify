# Changelog:
### v0.5.2 - We're bad at counting (27 Nov 2021):
**General changes:**
- Fixed filenaming on Windows
- Fixed removal of special characters metadata
- Can now download different songs with the same name
- Real-time downloads now work correctly
- Removed some debug messages
- Added album_artist metadata
- Added global song archive
- Added SONG_ARCHIVE config value
- Added CREDENTIALS_LOCATION config value
- Added `--download` argument
- Added `--config-location` argument
- Added `--output` for output templating
- Save extra data in .song_ids
- Added options to regulate terminal output
- Direct download support for certain podcasts  
  
**Docker images:**
- Remember credentials between container starts
- Use same uid/gid in container as on host  
  
**Windows installer:**
- Now comes with full installer
- Dependencies are installed if not found

### v0.2.4 (27 Oct 2021):
- Added realtime downloading support to avoid account suspensions.
- Fix for downloading by artist.
- Replace audio conversion method for better quality.
- Fix bug when automatically setting audio bitrate.

### v0.2.3 (25 Oct 2021):
- Moved changelog to seperate file.
- Added argument parsing in search function (query results limit and query result types).
- Fixed spelling errors.
- Added mac specific install guide stuff.
- Fixed infinite loop.
- Fixed issue where zspotify could'nt run on python 3.8/3.9.
- Changed it so you can just run zspotify from the root folder again.
- Added function to auto generate config file if it doesnt exist.
- Fixed issue where if you enabled splitting discs into seperate folders downloading would fail.
- Added playlist file(m3u) creation for playlist download.

### v0.2.2 (24 Oct 2021):
- Added basic support for downloading an entire podcast series.
- Split code into multiple files for easier maintenance.
- Changed initial launch script to app.py
- Simplified audio formats.
- Added prebuild exe for Windows users.
- Added Docker file.
- Added CONTRIBUTING.md.
- Fixed artist names getting cutoff in metadata.
- Removed data sanitization of metadata tags. 

### v0.2.1 (23 Oct 2021):
- Moved configuration from hard-coded values to separate zs_config.json file.
- Add subfolders for each disc.
- Can now search and download all songs by artist.
- Show single progress bar for entire album.
- Added song number at start of track name in albums.

### v0.2.0 (22 Oct 2021):
- Added progress bar for downloads.
- Added multi-select support for all results when searching.
- Added GPLv3 Licence.
- Changed welcome banner and removed unnecessary debug print statements.

### v0.1.9 (22 Oct 2021):
- Added Gitea mirror for when the Spotify Glowies come to DMCA the shit out of this.
- Changed the discord server invite to a matrix server so that won't get swatted either.
- Added option to select multiple of our saved playlists to download at once.
- Added support for downloading an entire show at once.

### v0.1.8 (21 Oct 2021):
- Improved podcast downloading a bit.
- Simplified the code that catches crashes while downloading.
- Cleaned up code using linter again.
- Added option to just paste a url in the search bar to download it.
- Added a small delay between downloading each track when downloading in bulk to help with downloading issues and potential bans.

### v0.1.7 (21 Oct 2021):
- Rewrote README.md to look a lot more professional.
- Added patch to fix edge case crash when downloading liked songs.
- Made premium account check a lot more reliable.
- Added experimental podcast support for specific episodes!

### v0.1.6 (20 Oct 2021):
- Added Pillow to requirements.txt.
- Removed websocket-client from requirements.txt because librespot-python added it to their dependency list.
- Made it hide your password when you type it in.
- Added manual override to force premium quality if zspotify cannot auto detect it.
- Added option to just download the raw audio with no re-encoding at all.
- Added Shebang line so it runs smoother on Linux.
- Made it download the entire track at once now so it is more efficient and fixed a bug users encountered.

### v0.1.5 (19 Oct 2021):
- Made downloading a lot more efficient and probably faster.
- Made the sanitizer more efficient.
- Formatted and linted all the code.

### v0.1.4 (19 Oct 2021):
- Added option to encode the downloaded tracks in the "ogg" format rather than "mp3".
- Added small improvement to sanitation function so it catches another edge case.

### v0.1.3 (19 Oct 2021):
- Added auto detection about if the current account is premium or not. If it is a premium account it automatically sets the quality to VERY_HIGH and otherwise HIGH if we are using a free account.
- Fixed conversion function so it now exports to the correct bitrate.
- Added sanitation to playlist names to help catch an edge case crash.
- Added option to download all your liked songs into a sub-folder.

### v0.1.2 (18 Oct 2021):
- Added .gitignore.
- Replaced dependency list in README.md with a proper requirements.txt file.
- Improved the readability of README.md.

### v0.1.1 (16 Oct 2021):
- Added try/except to help catch crashes where a very few specific tracks would crash either the downloading or conversion part.

### v0.1.0 (14 Oct 2021):
- Adjusted some functions so it runs again with the newer version of librespot-python.
- Improved my sanitization function so it catches more edge cases.
- Fixed an issue where sometimes spotify wouldn't provide a song id for a track we are trying to download. It will now detect and skip these invalid tracks.
- Added additional check for tracks that cannot be "played" due to licence(and similar) issues. These tracks will be skipped.

### v0.0.9 (13 Oct 2021):
- Initial upload, needs adjustments to get working again after backend rewrite.
