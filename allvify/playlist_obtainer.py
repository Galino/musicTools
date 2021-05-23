
from lib import settings
import requests
import json

# 11136385296
def obtainPlaylistInfo(userId):
    print("obtain spotify playlists...")
    limit = 50
    playlistToUrl = dict()

    offset = 0
    total = offset + 1 #only fol init
    while (offset) < total:
        url = "https://api.spotify.com/v1/users/" + str(userId) + "/playlists?limit=" + str(limit) + "&offset=" + str(offset)
        # myobj = "{\"name\":\"" + playlistName + "_LF" + "\",\"description\":\""+ playlistName +"\",\"public\":false}"
        print("execute" , url)
        response = requests.get(url, headers = settings.HEADER)
        print (response.status_code)
        json_data = json.loads(response.text)        
        playlistToUrl.update(processPlaylistsIntoDict(json_data))
        offset = json_data["offset"] + limit
        total = json_data["total"]
        print ("total:" , total)
    return  playlistToUrl


def processPlaylistsIntoDict(playlistsAsJson):
    json_data = playlistsAsJson
    # print(json.dumps(json_data, indent=4, sort_keys=True)) # prettify json
    playlistInfo = dict()
    print(json_data)
    for item in json_data["items"]:
        playlistInfo[item["name"]] = item["external_urls"]["spotify"]
        
    return playlistInfo
    




    # curl -X "GET" "https://api.spotify.com/v1/users/11136385296/playlists"
    #  -H "Accept: application/json" -H "Content-Type: application/json"
    #   -H "Authorization: Bearer BQCg6hD0Co64cboWOBIH5DkSuL13yeTYQOuYESqXGw5w0OjvimDgFAnyZfQQ8OWynKpATD4oF6ap1KR-ii6MJoU_W7T5nUw8-3_ft2S5f2JNd6Zv_yo2pb9e9U3W4rXMwQ4mbcPWqtBKfnS6wtOn1P6pZdNtuQy_n_onM6LMPX72bN-tvAwUr7PlBClR1pGhYSmz_0hKv8Olzpu5BtA3LOB5ZVM"