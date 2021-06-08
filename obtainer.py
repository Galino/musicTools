import json
import subprocess
import os
import re

def createOutputDirectory(parentDir, dir):
    # Path
    path = os.path.join(parentDir, dir)
    if not(os.path.exists(path)):
        os.mkdir(path)
        print("Directory '%s' created" % dir)
    else:
        print ("Directory '%s' already existed" % dir)
    return path


def obtainAllPlaylists(sp):
    results = sp.current_user_playlists()
    playlistToUrl = processPlaylistsIntoDict(results)
    limit = results['limit']
    offset = results['offset']
    total = results['total']
    while (limit + offset < total):
        results = sp.next(results)
        playlistToUrl.update(processPlaylistsIntoDict(results))

        limit = results['limit']
        offset = results['offset']
        total = results['total']
    return playlistToUrl


def processPlaylistsIntoDict(playlistsAsJson):
    json_data = playlistsAsJson
    # print(json.dumps(json_data, indent=4, sort_keys=True)) # prettify json
    playlistInfo = dict()
    print(json_data)
    for item in json_data["items"]:
        playlistInfo[item["name"]] = item["external_urls"]["spotify"]

    return playlistInfo


def getDesiredPlaylists(name):
    f = open(name, "r")
    return f.read().split("\n")

def obtainSongsFromDesiredPlatlits(playlistToUrl, desiredPlaylist = "DesiredPlaylistsNew.txt"):
    desiredPlaylists = getDesiredPlaylists(desiredPlaylist)
    parentDir = "/home/galb/Music/"

    for key, url in playlistToUrl.items():
        length = len(key)
        keyEdit = re.sub('[^a-z|A-Z|0-9|]+', '',key)
        print (keyEdit , (50 - length) * ".", url)

        if keyEdit in desiredPlaylists:
            createOutputDirectory(parentDir, keyEdit)

            cmd = "savify -q best -o %s -t playlist %s" % (parentDir+keyEdit, url)
            print("download spotify playlist: " + cmd)
            p1 = subprocess.run(cmd, shell=True)
            print(p1)