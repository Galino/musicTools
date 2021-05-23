# import subprocess
from musicUpgrade.musicSearcher import getUrls
from musicUpgrade.DirWalk import dirWalk
import requests
from lib import settings
import json
import subprocess
import os


# dir |Rename-Item -NewName {$_.name -replace  "^[0-1][0-9]", "Wolfmother"}

def createSpotifyPlaylist(playlistName):
    print("create spotify playlist...")
    url = 'https://api.spotify.com/v1/users/11136385296/playlists'
    myobj = "{\"name\":\"" + playlistName + "_LF" + "\",\"description\":\"" + playlistName + "\",\"public\":false}"
    response = requests.post(url, data=myobj, headers=settings.HEADER)
    json_data = json.loads(response.text)
    # print(json.dumps(json_data, indent=4, sort_keys=True)) # prettify json
    print("create Playlist response - \"{}\" - ".format(response))

    playlistInfo = dict()
    playlistInfo['id'] = json_data['id']
    playlistInfo['url'] = json_data['external_urls']['spotify']

    return playlistInfo


def fillSpotifyPlaylist(playlistID, trackUris):
    print("fill spotify playlist...")
    url = 'https://api.spotify.com/v1/playlists/' + playlistID + '/'
    print("TRACK URIS - " + str(trackUris))
    tracksUrl = 'tracks?uris=' + makeTracksAsQueryString(trackUris)
    response = requests.post(url + tracksUrl, headers=settings.HEADER)
    print("Add items to Playlist response - \"{}\" - ".format(response))


def makeTracksAsQueryString(trackUris):
    queryStr = ""
    for uri in trackUris:
        queryStr = queryStr + uri.replace(":", "%3A") + "%2C"
    return queryStr[:-3]  # remove last escape seq


def createOutputDirectory(parentDir, dir):
    # Path 
    path = os.path.join(parentDir, dir)

    if not (os.path.exists(path)):
        os.mkdir(path)
        print("Directory '%s' created" % dir)
    else:
        print("Directory '%s' already existed" % dir)
    return path


def donwloadSpotifyPlaylist(output, url):
    savify = "savify -q best"
    quality = " -q best"
    output = " -o " + output + ""
    typ = " -t playlist "

    cmd = savify + quality + output + typ + url
    print("download spotify playlist: " + cmd)
    p1 = subprocess.run(cmd, shell=True)
    print(p1)


pathToDir = "D:\\DUB\\SpotifyLocalFiles\\The Chillstep Dealer"
outputDir = "D:\\newDUB"

print("starting")
allParsedDirs = dirWalk(pathToDir)
for dir in allParsedDirs:
    print("dir playlist = ", dir.playlist)
    print("tracks = ", dir.tracks)
    playlistInfo = createSpotifyPlaylist(dir.playlist)
    x = 0
    while (True):
        tenTracks = dir.tracks[x:x + 10]
        spotifyUris = getUrls(dir.playlist, tenTracks)

        fillSpotifyPlaylist(playlistInfo['id'], spotifyUris)

        x = x + 10
        if x > len(dir.tracks):
            break

    # dirPath = createOutputDirectory(outputDir, dir.playlist)

    # donwloadSpotifyPlaylist(dirPath, playlistInfo['url'])

    # downloadSpotifyPlaylist
print("End of app")

# add Songs to playlist

# call Savify upont created Playlist


# url = 'https://api.spotify.com/v1/users/11136385296/playlists'
# # myobj = {"name":"New Playlist TEST3",
# #         "description":"New playlist description",
# #         "public":False}

# myobj = "{\"name\":\"New Playlist TEST4\",\"description\":\"New playlist description\",\"public\":false}"

# myHeader = {
#     "Accept": "application/json",
#     "Content-Type": "application/json",
#     "Authorization": "Bearer BQCpqKSBSMkEdfvCLlr4wxUmyL6l1S_QQtA11bNaTTRWVWl_po36UQiuVwez-v7MnmTgtmVRkAHTxFLWZJITOQfVCrwCv7J7iVTrylknQXfbgAMqb9foHkye1eMl0Vs4hQS0_S9m16tbE9XmYdWWi7LvhEj4Ny0Jm8eLoZPInu3b7pmCrT6ilKZKx5T8oMNF"}
# x = requests.post(url, data = myobj, headers = myHeader)

# print(x.text)

# p1 = subprocess.run("node .\\web-api-auth-examples\\authorization_code\\app.js", shell=True)

# print ("HOLA HEJ = ", p1)

# savifyCmd = "savify -t playlist -o . https://open.spotify.com/playlist/14i44YClmsh5x5jgNunwUP?si=v2Xxae9CSvynaJYrV0fsVQ"
# print (subprocess.run(savifyCmd, shell=True))
