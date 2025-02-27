import sys

from librespot.audio.decoders import AudioQuality
from tabulate import tabulate

from album import download_album, download_artist_albums
from const import TRACK, NAME, ID, ARTIST, ARTISTS, ITEMS, TRACKS, EXPLICIT, ALBUM, ALBUMS, \
    OWNER, PLAYLIST, PLAYLISTS, DISPLAY_NAME
from playlist import get_playlist_songs, get_playlist_info, download_from_user_playlist, download_playlist
from podcast import download_episode, get_show_episodes
from track import download_track, get_saved_tracks
from utils import sanitize_data, splash, split_input, regex_input_for_urls
from zspotify import ZSpotify

SEARCH_URL = 'https://api.spotify.com/v1/search'


def client() -> None:
    """ Connects to spotify to perform query's and get songs to download """
    ZSpotify()
    splash()

    if ZSpotify.check_premium():
        print('[ DETECTED PREMIUM ACCOUNT - USING VERY_HIGH QUALITY ]\n\n')
        ZSpotify.DOWNLOAD_QUALITY = AudioQuality.VERY_HIGH
    else:
        print('[ DETECTED FREE ACCOUNT - USING HIGH QUALITY ]\n\n')
        ZSpotify.DOWNLOAD_QUALITY = AudioQuality.HIGH

    if len(sys.argv) > 1:
        if sys.argv[1] == '-p' or sys.argv[1] == '--playlist':
            download_from_user_playlist()
        elif sys.argv[1] == '-ls' or sys.argv[1] == '--liked-songs':
            for song in get_saved_tracks():
                if not song[TRACK][NAME]:
                    print(
                        '###   SKIPPING:  SONG DOES NOT EXIST ON SPOTIFY ANYMORE   ###')
                else:
                    download_track(song[TRACK][ID], 'Liked Songs/')
                print('\n')
        else:
            track_id, album_id, playlist_id, episode_id, show_id, artist_id = regex_input_for_urls(
                sys.argv[1])

            if track_id is not None:
                download_track(track_id)
            elif artist_id is not None:
                download_artist_albums(artist_id)
            elif album_id is not None:
                download_album(album_id)
            elif playlist_id is not None:
                playlist_songs = get_playlist_songs(playlist_id)
                name, _ = get_playlist_info(playlist_id)
                for song in playlist_songs:
                    download_track(song[TRACK][ID],
                                   sanitize_data(name) + '/')
                    print('\n')
            elif episode_id is not None:
                download_episode(episode_id)
            elif show_id is not None:
                for episode in get_show_episodes(show_id):
                    download_episode(episode)

    else:
        search_text = ''
        while len(search_text) == 0:
            search_text = input('Enter search or URL: ')

        track_id, album_id, playlist_id, episode_id, show_id, artist_id = regex_input_for_urls(
            search_text)

        if track_id is not None:
            download_track(track_id)
        elif artist_id is not None:
            download_artist_albums(artist_id)
        elif album_id is not None:
            download_album(album_id)
        elif playlist_id is not None:
            playlist_songs = get_playlist_songs(playlist_id)
            name, _ = get_playlist_info(playlist_id)
            for song in playlist_songs:
                download_track(song[TRACK][ID], sanitize_data(name) + '/')
                print('\n')
        elif episode_id is not None:
            download_episode(episode_id)
        elif show_id is not None:
            for episode in get_show_episodes(show_id):
                download_episode(episode)
        else:
            search(search_text)


def search(search_term):
    """ Searches Spotify's API for relevant data """
    params = {'limit': '10',
              'offset': '0',
              'q': search_term,
              'type': 'track,album,artist,playlist'}

    # Parse args
    splits = search_term.split()
    for split in splits:
        index = splits.index(split)

        if split[0] == '-' and len(split) > 1:
            if len(splits)-1 == index:
                raise IndexError('No parameters passed after option: {}\n'.
                                 format(split))

        if split == '-l' or split == '-limit':
            try:
                int(splits[index+1])
            except ValueError:
                raise ValueError('Paramater passed after {} option must be an integer.\n'.
                                 format(split))
            if int(splits[index+1]) > 50:
                raise ValueError('Invalid limit passed. Max is 50.\n')
            params['limit'] = splits[index+1]

        if split == '-t' or split == '-type':

            allowed_types = ['track', 'playlist', 'album', 'artist']
            passed_types = []
            for i in range(index+1, len(splits)):
                if splits[i][0] == '-':
                    break

                if splits[i] not in allowed_types:
                    raise ValueError('Parameters passed after {} option must be from this list:\n{}'.
                                     format(split, '\n'.join(allowed_types)))

                passed_types.append(splits[i])
            params['type'] = ','.join(passed_types)

    if len(params['type']) == 0:
        params['type'] = 'track,album,artist,playlist'

    # Clean search term
    search_term_list = []
    for split in splits:
        if split[0] == "-":
            break
        search_term_list.append(split)
    if not search_term_list:
        raise ValueError("Invalid query.")
    params["q"] = ' '.join(search_term_list)

    resp = ZSpotify.invoke_url_with_params(SEARCH_URL, **params)

    counter = 1
    dics = []

    total_tracks = 0
    if TRACK in params['type'].split(','):
        tracks = resp[TRACKS][ITEMS]
        if len(tracks) > 0:
            print('###  TRACKS  ###')
            track_data = []
            for track in tracks:
                if track[EXPLICIT]:
                    explicit = '[E]'
                else:
                    explicit = ''

                track_data.append([counter, f'{track[NAME]} {explicit}',
                                  ','.join([artist[NAME] for artist in track[ARTISTS]])])
                dics.append({
                    ID: track[ID],
                    NAME: track[NAME],
                    'type': TRACK,
                })

                counter += 1
            total_tracks = counter - 1
            print(tabulate(track_data, headers=[
                  'S.NO', 'Name', 'Artists'], tablefmt='pretty'))
            print('\n')
            del tracks
            del track_data

    total_albums = 0
    if ALBUM in params['type'].split(','):
        albums = resp[ALBUMS][ITEMS]
        if len(albums) > 0:
            print('###  ALBUMS  ###')
            album_data = []
            for album in albums:
                album_data.append([counter, album[NAME],
                                  ','.join([artist[NAME] for artist in album[ARTISTS]])])
                dics.append({
                    ID: album[ID],
                    NAME: album[NAME],
                    'type': ALBUM,
                })

                counter += 1
            total_albums = counter - total_tracks - 1
            print(tabulate(album_data, headers=[
                  'S.NO', 'Album', 'Artists'], tablefmt='pretty'))
            print('\n')
            del albums
            del album_data

    total_artists = 0
    if ARTIST in params['type'].split(','):
        artists = resp[ARTISTS][ITEMS]
        if len(artists) > 0:
            print('###  ARTISTS  ###')
            artist_data = []
            for artist in artists:
                artist_data.append([counter, artist[NAME]])
                dics.append({
                    ID: artist[ID],
                    NAME: artist[NAME],
                    'type': ARTIST,
                })
                counter += 1
            total_artists = counter - total_tracks - total_albums - 1
            print(tabulate(artist_data, headers=[
                  'S.NO', 'Name'], tablefmt='pretty'))
            print('\n')
            del artists
            del artist_data

    total_playlists = 0
    if PLAYLIST in params['type'].split(','):
        playlists = resp[PLAYLISTS][ITEMS]
        if len(playlists) > 0:
            print('###  PLAYLISTS  ###')
            playlist_data = []
            for playlist in playlists:
                playlist_data.append(
                    [counter, playlist[NAME], playlist[OWNER][DISPLAY_NAME]])
                dics.append({
                    ID: playlist[ID],
                    NAME: playlist[NAME],
                    'type': PLAYLIST,
                })
                counter += 1
            total_playlists = counter - total_artists - total_tracks - total_albums - 1
            print(tabulate(playlist_data, headers=[
                  'S.NO', 'Name', 'Owner'], tablefmt='pretty'))
            print('\n')
            del playlists
            del playlist_data

    if total_tracks + total_albums + total_artists + total_playlists == 0:
        print('NO RESULTS FOUND - EXITING...')
    else:
        selection = ''
        while len(selection) == 0:
            selection = str(input('SELECT ITEM(S) BY S.NO: '))
        inputs = split_input(selection)
        for pos in inputs:
            position = int(pos)
            for dic in dics:
                print_pos = dics.index(dic) + 1
                if print_pos == position:
                    if dic['type'] == TRACK:
                        download_track(dic[ID])
                    elif dic['type'] == ALBUM:
                        download_album(dic[ID])
                    elif dic['type'] == ARTIST:
                        download_artist_albums(dic[ID])
                    else:
                        download_playlist(dic)
