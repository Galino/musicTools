import subprocess
# # import msvcrt
# # go = False
# # tracks = [5,6,7,8,9]
# # chosen = 0
# # while (go != True):
# #     chosen = msvcrt.getch()
# #     choseNum = int(chosen.decode('utf-8'))
# #     if (choseNum > len(tracks)):
# #         print ("Choose number 1-", len(tracks))
# #     else:
# #         go = True
# # trackNum = choseNum-1
# import re
# # print("truckNum = {}".format(tracks[trackNum]))
# def getTrackForSpotifySearch(track):
#     modifiedTrack = ""
#     #only mp3 files
#         # track = re.sub(r'Zomboy|Young', "Zomgirl", track)
#     if ".mp3"  in track:
#         modifiedTrack  = re.sub(r"&|\(|\)|\[|\]|ft.|feat.|vs|free download|original mix|official video|.mp3","", track.lower())
#         modifiedTrack = re.sub(r"[0-1][0-9](-| -)", "", modifiedTrack)
#         modifiedTrack = re.sub(r"-","", modifiedTrack)
#         modifiedTrack  = modifiedTrack.replace(" ", "%20")
#         return modifiedTrack         
#     else:
#         return ""

# name = "Flying Horseman (official video)- 10,000 Feet.mp3"
# output = getTrackForSpotifySearch(name)
# print(output)

# p1 = subprocess.run("savify -q best -o . -t track https://open.spotify.com/track/7vzzE56ly3ykTbizEKAs2O?context=spotify%3Aplaylist%3A37i9dQZF1DX5Q27plkaOQ3&si=xCFGla6NTqCDCN8_TwvgnQ", shell=True)
# print ("p1 - ", p1)
import os 

# s = "D:\\DUB\\TEST\\testA"
# dir = "testB"
# parentDir = s.rsplit('\\',1)[0]

# path = os.path.join(parentDir, dir+"_SF")
# os.mkdir(path)
# print("Directory '% s' created" % dir) 
# print (path)
# def createOutputDirectory(parentDir, dir):  
#     # Path 
#     path = os.path.join(parentDir, dir)
#     if not(os.path.exists(path))
#     os.mkdir(path)
#     print("Directory '% s' created" % dir) 
#     return path
    


# pathToDir = "D:\\DUB\\AKOV"
# createOutputDirectory(parentDir,)

pole = [1,2,3,4,5,5,6,7,89,1,2,44,2,3,5,7]
x = 90
print (pole[x:x+10])
