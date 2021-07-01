from bottle import route, run, request
import getch
import spotipy
from spotipy import oauth2
import json
from obtainer import *

PORT_NUMBER = 8080

# SPOTIFY CLIENT INFO
spotifyClient = open('SPOTIFY_CLIENT.txt', "r")
spotiSplit = spotifyClient.read().split("\n")
SPOTIPY_CLIENT_ID = spotiSplit[0].split("=")[1]
SPOTIPY_CLIENT_SECRET = spotiSplit[1].split("=")[1]
SPOTIPY_REDIRECT_URI = spotiSplit[2].split("=")[1]

SCOPE = 'user-library-read, playlist-read-private, playlist-read-collaborative, playlist-modify-public, playlist-modify-private'
CACHE = '.spotipyoauthcache'

sp_oauth = oauth2.SpotifyOAuth(SPOTIPY_CLIENT_ID, SPOTIPY_CLIENT_SECRET, SPOTIPY_REDIRECT_URI, scope=SCOPE,
                               cache_path=CACHE)


def processPlaylistsIntoDict(playlistsAsJson):
    json_data = playlistsAsJson
    # print(json.dumps(json_data, indent=4, sort_keys=True)) # prettify json
    playlistInfo = dict()
    print(json_data)
    for item in json_data["items"]:
        playlistInfo[item["name"]] = item["external_urls"]["spotify"]

    return playlistInfo



@route('/')
def index():
    access_token = ""
    token_info = sp_oauth.get_cached_token()

    if token_info:
        print("Found cached token!")
        access_token = token_info['access_token']
    else:
        url = request.url
        code = sp_oauth.parse_response_code(url)
        if code != url:
            print("Found Spotify auth code in Request URL! Trying to get valid access token...")
            token_info = sp_oauth.get_access_token(code)
            access_token = token_info['access_token']

    if access_token:
        print("Access token available! Trying to get user information...")

        sp = spotipy.Spotify(access_token)
        desiredPlaylists = getDesiredPlaylists("DesiredPlaylistsTEST.txt")
        filteredPlaylists = []
        print("Playlists:")
        for playlist in obtainAllPlaylistComplet(sp):
            print(stripName(playlist['name']))
            if (stripName(playlist['name'])) in desiredPlaylists:
                filteredPlaylists.append(playlist)

        removeDuplicatesFromMyLibrary(filteredPlaylists, sp)

        # printResultPlaylistNames(sp)
        # sp.playlist_items()
        # obtainSongsFromDesiredPlaylists(playlistToUrl, desiredPlaylist = "DesiredPlaylistsTEST.txt" )

        return "done"

    else:
        return htmlForLoginButton()


def removeDuplicatesFromMyLibrary(filteredPlaylists, sp):
    print("Going to remove duplicates from Library")
    for i, playlist in enumerate(filteredPlaylists):
        print("Check Playlist - " + playlist['name'])
        playlistItems = obtainAllItemsOfPlaylist(sp, playlist['id'])
        for item in playlistItems:
            track = item['track']
            print("Checking track " + str(track['name']) + " from " + str(playlist['name']))
            occuredInPlaylits = [playlist]
            if (i + 1 == len(filteredPlaylists)):
                break
            for otherPlaylist in filteredPlaylists[i + 1:]:
                otherPlaylistItems = obtainAllItemsOfPlaylist(sp, otherPlaylist['id'])

                if playlistItemsContainTrack(otherPlaylistItems, track['id']) and playlist['name'] != otherPlaylist['name']:
                    print("track is also in " + str(otherPlaylist['name']))
                    occuredInPlaylits.append(otherPlaylist)
                    print("actual list of occurences: " + str(occuredInPlaylits))
            # skip non-duplicates
            if (len(occuredInPlaylits) <= 1):
                continue

            artists = []
            for artist in track['artists']:
                artists.append(artist['name'])
            print("Found " + str(artists) + " - " + str(track['name']) + " in playlists: ")
            for i, occurrence in enumerate(occuredInPlaylits):
                print(str(i + 1) + ") " + str(occurrence['name']))
            print("Let track only in playlist:")

            go = False
            choseNum = 0
            while (go != True):
                # chosen = msvcrt.getch()  # this will load as byte value b'
                chosen = getch.getch()
                print(chosen)
                if (not (chosen.isdigit()) or int(chosen) > len(occuredInPlaylits)):
                    print("Choose number 1-", len(occuredInPlaylits))
                else:
                    choseNum = int(chosen)
                    go = True
            playlistNum = choseNum - 1

            occuredInPlaylits.remove(occuredInPlaylits[playlistNum])
            removeItemFromPlaylists(sp, occuredInPlaylits, track)
            occuredInPlaylits = []
        print("done")


def printResultPlaylistNames(sp):
    results = sp.current_user_playlists()
    limit = results['limit']
    offset = results['offset']
    total = results['total']
    for i, res in enumerate(results['items']):
        print(str(i) + " - " + res['name'])
    while (limit + offset < total):
        results = sp.next(results)
        for i, res in enumerate(results['items']):
            print(str(i) + " - " + res['name'])
        limit = results['limit']
        offset = results['offset']
        total = results['total']


def htmlForLoginButton():
    auth_url = getSPOauthURI()
    htmlLoginButton = "<a href='" + auth_url + "'>Login to Spotify</a>"
    return htmlLoginButton


def getSPOauthURI():
    auth_url = sp_oauth.get_authorize_url()
    return auth_url


run(host='localhost', port=8080)


"""
budem mat zoznam playlistov, s ktorymi chcem pracovat
vezmem vsetky a cele playlisty
v kazdom playliste budem v cykle brat po jednej pesnicke p1
dotiahnem si dalsi playlist 
porovnam p1-ID s ID kazdej pesnicky dotiahnuteho playlistu
    ak najdem zhodu, poznacim si playlist a pesnicku (index pesnicky v playliste)
po prejdeni vsetkych ostatnych playlistov si vypisem playlisty s cislami kde vsade sa nachadza
Cislom si vyberiem jeden playlist v ktorom chcem pesnicku nechat a z ostatnych hu odstranim  
"""