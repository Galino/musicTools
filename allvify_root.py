import requests
import json
import subprocess
import os
import re
from lib import settings
from lib import utils
import allvify.playlist_obtainer as po


from savify import Savify
from savify.types import Type, Format, Quality
from savify.utils import PathHolder

# cmd = "savify -q best -o testPlaylist -t playlist https://open.spotify.com/playlist/1EoDKOIZX8IrwiQOzws1Av?si=Jp6_75GyQvO1_uyJ4o1qUA"


# print("download spotify playlist: " + cmd)
# p1 = subprocess.run(cmd, shell=True)
# print(p1)



def desiredPlaylistsSituation():
    listOld = getDesiredPlaylists("DesiredPlaylists.txt")
    listNew = getDesiredPlaylists("DesiredPlaylistsNew.txt")
    print("OLD  -- " ,str(listOld))
    print("NEW  -- " ,str(listNew))

    print("Those are missing:")
    for name in listOld:
        if not name in listNew:
            print (name)

    print("\n\n\n")
    print("Those are new:")
    for name in listNew:
        if not name in listOld:
            print (name)

def getDesiredPlaylists(name):
    f = open(name, "r")
    return f.read().split("\n")


def printUserPlaylists(userId):
    playlistToUrl = po.obtainPlaylistInfo(userId=userId)
    for key, url in playlistToUrl.items():
        length = len(key)
        keyEdit = re.sub('[^a-z|A-Z|0-9|]+', '',key)
        print (keyEdit , (50 - length) * ".", url)

def obtainSongFromDesiredPlatlits(userId):
    playlistToUrl = po.obtainPlaylistInfo(userId=userId)

    desiredPlaylists = getDesiredPlaylists("DesiredPlaylistsNew.txt")
    parentDir = "D:\\newDUB\\spotifyMusic\\"

    for key, url in playlistToUrl.items():
        length = len(key)
        keyEdit = re.sub('[^a-z|A-Z|0-9|]+', '',key)
        print (keyEdit , (50 - length) * ".", url)

        if keyEdit in desiredPlaylists:
            utils.createOutputDirectory(parentDir, keyEdit)

            cmd = "savify -q best -o %s -t playlist %s" % (parentDir+keyEdit, url)
            print("download spotify playlist: " + cmd)
            p1 = subprocess.run(cmd, shell=True)
            print(p1)


# REMEMBER - bearer I copy into header allow me to obtain only PUBLIC playlists
userId = "11136385296"
obtainSongFromDesiredPlatlits(userId)

# printUserPlaylists(userId=userId)


# print("Those are same:")
# for name in listOld:
#     if name in listNew:
#         print (name)


# for key, url in playlistToUrl.items():
#     keyEdit = re.sub('[^a-z|A-Z|0-9|]+', '',key)
#     print (keyEdit)

