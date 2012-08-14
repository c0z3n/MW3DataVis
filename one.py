from pyprocessing import *
import cPickle as pickle
import datetime as dt
import math

filename=""
valid_filename = False

nodes = []

size(640, 360);
nodes = []

FILE_EXTENSION = ".kdt"
DIRECTORY_PREFIX = "..\\"
MAP_TABLES = []
FILE_NAMES = [
                    "Lockdown",
                    "Bootleg",
                    "Mission",
                    "Carbon",
                    "Dome",
                    "Downturn",
                    "Hardhat",
                    "Interchange",
                    "Fallen",
                    "Bakaara",
                    "Resistance",
                    "Arkaden",
                    "Outpost",
                    "Seatown",
                    "Underground",
                    "Village"
             ]

             
for idx, file in enumerate(FILE_NAMES):
    filename = DIRECTORY_PREFIX + file + FILE_EXTENSION
    if os.path.isfile(r"%s" %filename):
        MAP_TABLES.append(pickle.load(open(filename, "rb")))
    else:
        print "could not load map \"" + file + "\""
        MAP_TABLES.append(None)
        
eyeX = 0
eyeY = 1500
eyeZ = 400

centerX = 0
centerY = 0
centerZ = 0

frameRate(30)
selected_map = 8
indexpoint = 20

noLights()
noSmooth()

def draw():
    background(0);
    pushMatrix();
    now = dt.datetime.now()
    #translate(width/2,500 , -1000);
    #rotateY(radians(int(now.strftime("%S%f"))/72000))
    #rotateX(radians(90))
    time = int(now.strftime("%S%f"))*.00000008
    multiplier = 2000
    #print time, math.cos(time)*multiplier, math.sin(time)*multiplier
    camera(math.cos(time)*multiplier, math.sin(time)*multiplier, -300, 0, 0, 0, 0, 0, 1)
    # pushMatrix();
    
    # popMatrix();
    stroke(255)
    strokeWeight(1)
    for datapoint in MAP_TABLES[selected_map]:
        point(datapoint[0]/2, datapoint[1]/2, 0-(datapoint[2]/2))
    popMatrix();

run()