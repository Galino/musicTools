import json
import re
import subprocess


def testJsonParsing():
    f = open("playlist.json", "r")
    jsonAsString  = f.read()
    json_data = json.loads(jsonAsString)
    # print(json_data)
    playlistInfo = dict()
    for item in json_data["items"]:
        playlistInfo[item["name"]] = item["external_urls"]["spotify"]
        
    for name , link in playlistInfo.items():
        print (name , "   ", link)

def testDict():
    x = dict()
    x["a"] = 5
    x["b"] = 7

    y = dict()
    y["b"] = 9
    y["c"] = 514564

    x.update(y)
    print (str(x))

def testLen():
    # parentDir = "hula"
    # keyEdit = "vooooka"
    # url = "urelelelelelel"
    cmd = "savify -q best -o D:\\newDUB\\Cossacks -t playlist https://open.spotify.com/playlist/7oQOeFacXFchcyH7R3oqr7"
    p1 = subprocess.run(cmd, shell=True)
    print(p1)
    if (p1.returncode == 0):
        print("uspech")
    else:
        print("shit happens")

def testPlaylist():
    f = open("DesiredPlaylists.txt", "r")
    lists = f.read().split("\n")
    print (str(lists))

# testJsonParsing()
testLen()