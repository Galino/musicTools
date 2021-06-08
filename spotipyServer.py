from bottle import route, run, request
import spotipy
from spotipy import oauth2
import json
from obtainer import *

PORT_NUMBER = 8080
SPOTIPY_CLIENT_ID = '2b716b05be6e40a38c49aff0e59e878c'
SPOTIPY_CLIENT_SECRET = '2ecf43c20f2b490ab3fdcea9a312ee23'
SPOTIPY_REDIRECT_URI = 'http://localhost:8080'
SCOPE = 'user-library-read, playlist-read-private, playlist-read-collaborative'
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
        playlistToUrl = dict()
        print("Access token available! Trying to get user information...")

        sp = spotipy.Spotify(access_token)
        playlistToUrl = obtainAllPlaylists(sp)
        obtainSongsFromDesiredPlatlits(playlistToUrl, desiredPlaylist = "DesiredPlaylistsTEST.txt" )

        return str(playlistToUrl)

    else:
        return htmlForLoginButton()


def htmlForLoginButton():
    auth_url = getSPOauthURI()
    htmlLoginButton = "<a href='" + auth_url + "'>Login to Spotify</a>"
    return htmlLoginButton


def getSPOauthURI():
    auth_url = sp_oauth.get_authorize_url()
    return auth_url


run(host='localhost', port=8080)