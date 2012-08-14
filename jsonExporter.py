
#=================================================================#
#  jsonExporter.py - by c0z3n.                                    #
#                                                                 #
#  A simple tool to export MW3 killdata tables from               #  
#  .kdt pickled data files to json objects, to use with the       # 
#  online webGL viewer at http://c0z3n.org/mapping                #
#                                                                 #
#=================================================================#

import sys, os.path, cPickle, json
from collections import defaultdict

filenames = ["Arkaden", "Bakaara", "Bootleg", "Carbon", "Dome", "Downturn", 
             "Fallen", "Hardhat", "Interchange", "Lockdown", "Mission",
             "Outpost", "Resistance", "Seatown", "Underground", "Village",]

if not os.path.exists(r"jsonkdt"):
    os.makedirs(r"jsonkdt")
            
for n in filenames:
    json_file = "jsonkdt\\" + n.lower() +".json"
    filename = "..\\" + n + ".kdt"
    try:
        killdata_table = cPickle.load(open(filename, "rb"))
        export_list = []
        for point in killdata_table:
            temp_list = []
            export_list.append((point[0], point[2], point[1]))

        f = open(json_file, 'a')
        f.write(json.dumps(export_list))
        f.close()
    except:
        print "error with map: " + filenames[n]
        pass
        