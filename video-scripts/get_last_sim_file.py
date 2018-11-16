import os
import glob

vid_sim_path = "/home/patrick/omnetpp-5.3/samples/vanet-dash-v.0.1/video-scripts/vid_1/SIM-RUNS/*.yaml"

version = 0

for sim_file in glob.iglob(vid_sim_path):
    version_file = sim_file.split("_")[3][0]
    if version_file > version:
        version = version_file
        
    print(version)