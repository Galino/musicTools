import json
import re
import subprocess
import os


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


def deleteStupidWord(veta):
    znovaVeta = ""
    for slovo in veta.split(" "):
        print (slovo)
        if not re.search("[^\x00-\x7F]+", slovo):
            znovaVeta += slovo + " "
    return znovaVeta[0:-1]
# testJsonParsing()
# print (deleteStupidWord( "björk  áll is fúll of love chrisô su remix Düsseldorf, Köln, Москва, 北京市, إسرائيل !@#$'"))

pathToDir = "D:\\newDUB\\"
# for root, subdirs, files in os.walk(pathToDir):
#     print (root)

def getDesiredPlaylists(name):
    f = open(name, "r")
    return f.read().split("\n")


pathToDir = "D:\\newDUB\\"
files = os.listdir(pathToDir)

listOld = getDesiredPlaylists("DesiredPlaylists.txt")
listNew = getDesiredPlaylists("DesiredPlaylistsNew.txt")

savifyDeprecated = []
savifyActual = []

for subor in files:
    if subor in listOld and subor not in listNew:
        savifyDeprecated.append(subor)

    if subor in listNew:
        savifyActual.append(subor)
    

savifyDeprecated.sort()
savifyActual.sort()
# for name in savifyDeprecated:
#     print(name)

for name in savifyActual:
    print(name)