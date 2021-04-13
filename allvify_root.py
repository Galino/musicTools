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




def getDesiredPlaylists():
    f = open("DesiredPlaylists.txt", "r")
    return f.read().split("\n")



playlistToUrl = po.obtainPlaylistInfo("11136385296")

desiredPlaylists = getDesiredPlaylists()
parentDir = "D:\\newDUB\\"

for key, url in playlistToUrl.items():
    length = len(key)
    keyEdit = re.sub('[^a-z|A-Z|0-9|]+', '',key)
    print (keyEdit , (50- length) * ".", url)

    if keyEdit in desiredPlaylists:
        utils.createOutputDirectory(parentDir, keyEdit)

        cmd = "savify -q best -o %s -t playlist %s" % (parentDir+keyEdit, url)
        print("download spotify playlist: " + cmd)
        p1 = subprocess.run(cmd, shell=True)
        print(p1)


# for key, url in playlistToUrl.items():
#     keyEdit = re.sub('[^a-z|A-Z|0-9|]+', '',key)
#     print (keyEdit)

