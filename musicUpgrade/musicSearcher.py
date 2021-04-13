import requests
from lib import settings
import msvcrt
import json
import re
# dir |Rename-Item -NewName {$_.name -replace  "^[0-1][0-9]", "Wolfmother"}
def getUrls(playlist, fileOrigNames):
    # spotifyTrackSearch = "Zomboy%20%20Like%20A%20Bitch%20Kill%20The%20Noise%20Remix"
    # spotifyTrackSearch = "Zomboy%20%20Like%20A%20Bitch%20"
    tracksUris = []
    for fileOrigName in fileOrigNames:
        spotifyTrackSearch = getTrackForSpotifySearch(fileOrigName)
        print("spotifyTrackName = \"" , spotifyTrackSearch + "\"")
        if (spotifyTrackSearch == ""):
           writeToSongsSpotifyIsMissing(fileOrigName, playlist, spotifyTrackSearch.replace("%20", " ")) 
           continue
        response = requests.get(buildUrl(spotifyTrackSearch), headers = settings.HEADER)
        json_data = json.loads(response.text)
        # print ("response = ",json_data)
        # json_data.get()
        # print(json.dumps(json_data, indent=4, sort_keys=True)) # prettify json
        if ('tracks' not in json_data):
            print(json.dumps(json_data, indent=4, sort_keys=True)) # prettify json
            exit(1)

        tracks = json_data['tracks']['items']
        trackNum = -1
        if (len(tracks) == 0):
            print ("found nothing like: \"" + spotifyTrackSearch.replace("%20", " ") + "\"" )
            writeToSongsSpotifyIsMissing(fileOrigName, playlist, spotifyTrackSearch.replace("%20", " "))
            continue
        elif (len(tracks) > 1):
            print("Which one should I download? (press 0 for none)")
            print("Looking for: ", spotifyTrackSearch.replace("%20", " ") )
            for i in range(len(tracks)):
                print("{}) {} - {} ({})".format(i + 1, tracks[i]['artists'][0]['name'], tracks[i]['name'], tracks[i]['album']['name']))
            go = False
            chosen = 0
            while (go != True):
                chosen = msvcrt.getch() # this will load as byte value b'
                choseNum = int(chosen.decode('utf-8'))
                if (choseNum > len(tracks)):
                    print ("Choose number 1-", len(tracks))
                else:
                    go = True
            if (choseNum == 0):
                print("Song Skipped")
                writeToSongsSpotifyIsMissing(fileOrigName, playlist, spotifyTrackSearch.replace("%20", " "))
                continue

            trackNum = choseNum-1
        else:
            trackNum = 0

        print ("Chosen track: {} - {} ({})\n\n".format(tracks[trackNum]['artists'][0]['name'], tracks[trackNum]['name'], tracks[trackNum]['album']['name']))
        tracksUris.append(tracks[trackNum]['uri'])

    writeToSongsSpotifyIsMissing("--------------------------", "--------------------------", "--------------------------") #to divide each run  
    
    return tracksUris


def getTrackForSpotifySearch(track):
    modifiedTrack = ""
    #only mp3 files
        # track = re.sub(r'Zomboy|Young', "Zomgirl", track)
    if ".mp3" in track:
        modifiedTrack = track.lower()
        modifiedTrack  = re.sub(r"&|\(|\)|\[|\]|ft.|feat.|vs|free download|original mix|official video|.mp3","",modifiedTrack)
        modifiedTrack = re.sub(r"titan records|mindtech recordings|c4c recordings|close 2 death records|neurofunkgrid|dw|1440p","", modifiedTrack)
        modifiedTrack = re.sub(r"[0-1][0-9](-| -)", "", modifiedTrack)
        modifiedTrack = re.sub(r" x ", " ", modifiedTrack)
        modifiedTrack = re.sub(r"-","", modifiedTrack)
        modifiedTrack  = modifiedTrack.replace(" ", "%20")
        return modifiedTrack         
    else:
        return ""
        

#  trackURL - json_data['tracks']['items'][0]['external_urls']['spotify']
#  trackName - json_data['tracks']['items'][0]['name']
#  artist -  json_data['tracks']['items'][0]['artists'][0]['name']
def writeToSongsSpotifyIsMissing(origName, playlistName, songName):
    f = open("blackList.txt", "a")
    f.write(origName  + " - " + playlistName + " - " + songName + "\n")
    f.close()


def buildUrl(spotifyTrackSearch):
    baseUrl = "https://api.spotify.com/v1/search?"
    q = "q=" + spotifyTrackSearch
    postFix = "&type=track&limit=9"
    return baseUrl+q+postFix

# def buildHeader_Dict():
#     access_token = "BQAdYUhtG4rwo8FCL6HU9utIDTbBJv880THDnqRGsalKjRs5wH84lYihq35e-Fb7MRCgspIBkzEhZ4k9xMHHgWWKIle8MSoa5jbAoTFP-cjy-M25-7nAdQ-ayHY_n3ZF7fKLZrhMer5rHjnBJ_Ovco-gL_lhLOolWJthOuycSwGb8-ZI5K6UE-XdUJtywWVL"
#     return {
#     "Accept": "application/json",
#     "Content-Type": "application/json",
#     "Authorization": "Bearer " + access_token}


# getUrls(["Zomboy%20%20Like%20A%20Bitch%20"])