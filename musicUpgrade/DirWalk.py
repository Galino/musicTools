import os
from .ParsedDir import ParsedDir

def dirWalk(pathToDir):
    allParsedDirs = []
    for root, subdirs, files in os.walk(pathToDir):
        parsedDir = ParsedDir()
        parsedDir.playlist = root.split("\\")[-1]
        parsedDir.tracks = files
        allParsedDirs.append(parsedDir)

    return allParsedDirs