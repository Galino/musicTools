import os

def createOutputDirectory(parentDir, dir):  
    # Path 
    path = os.path.join(parentDir, dir)
    if not(os.path.exists(path)):
        os.mkdir(path)
        print("Directory '%s' created" % dir) 
    else:
        print ("Directory '%s' already existed" % dir)
    return path