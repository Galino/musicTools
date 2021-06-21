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
SPOTIPY_CLIENT_ID = spotiSplit[0].split("=")[1] #'2b716b05be6e40a38c49aff0e59e878c'
SPOTIPY_CLIENT_SECRET = spotiSplit[1].split("=")[1] #'2ecf43c20f2b490ab3fdcea9a312ee23'
SPOTIPY_REDIRECT_URI = spotiSplit[2].split("=")[1] #'http://localhost:8080'

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
        for playlist in obtainAllPlaylistComplet(sp):
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
    for i, playlist in enumerate(filteredPlaylists):
        playlistItems = obtainAllItemsOfPlaylist(sp, playlist['id'])
        for item in playlistItems:
            track = item['track']
            occuredInPlaylits = [playlist]
            if (i + 1 == len(filteredPlaylists)):
                break
            for otherPlaylist in filteredPlaylists[i + 1:]:
                otherPlaylistItems = obtainAllItemsOfPlaylist(sp, otherPlaylist['id'])

                if playlistItemsContainTrack(otherPlaylistItems, track['id']):
                    occuredInPlaylits.append(otherPlaylist)
            # skip non-duplicates
            if (len(occuredInPlaylits) <= 1):
                continue

            artists = []
            for artist in track['artists']:
                artists.append(artist['name'])
            print("Found " + str(artists) + " - " + track['name'] + " in playlists: ")
            for i, occurrence in enumerate(occuredInPlaylits):
                print(str(i + 1) + ") " + occurrence['name'])
            print("Let track only in playlist:")

            go = False
            while (go != True):
                # chosen = msvcrt.getch()  # this will load as byte value b'
                chosen = getch.getch()
                print(chosen)
                choseNum = int(chosen)
                if (choseNum > len(occuredInPlaylits)):
                    print("Choose number 1-", len(occuredInPlaylits))
                else:
                    go = True
            playlistNum = choseNum - 1

            occuredInPlaylits.remove(occuredInPlaylits[playlistNum])
            removeItemFromPlaylists(sp, occuredInPlaylits, track)


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