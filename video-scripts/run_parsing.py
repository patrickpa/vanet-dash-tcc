import glob
import sys
import subprocess

video_dict = {"BusyStreetScene":["./vid_1/SIM-RUNS/", 13], "CarsStoping": ["./vid_2/SIM-RUNS/", 9]}

folder = "/home/patrick/omnetpp-5.3/samples/vanet-dash-v.0.1/simulations/cars/"
sim_runs_folder = folder + "results/DASH-*.vec"

for video_n in video_dict:

    video = video_n
    video_len = video_dict[video_n][1]
    vid_sim_path = video_dict[video_n][0]

    sim_parse_file = 0

    for sim_file in glob.iglob(sim_runs_folder):
        sim_parse_file += 1
        command = 'python parse_sim_log.py {} {} {} {} {}'.format(video, video_len, sim_file, vid_sim_path, sim_parse_file)
        print ('Running command: ' + command)
        subprocess.call(command, shell=True)

    print("All {} sim(s) parsed.".format(sim_parse_file))

