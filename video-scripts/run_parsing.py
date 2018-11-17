import glob
import sys
import subprocess
import yaml

video_dict = {"BusyStreetScene":["./vid_1/SIM-RUNS/", 13], "CarsStoping": ["./vid_2/SIM-RUNS/", 9]}

folder = "/home/patrick/omnetpp-5.3/samples/vanet-dash-v.0.1/simulations/cars/"
sim_runs_folder = folder + "results/General-*.vec"


# Apaga os arquivos de medias de output
file_med_qlt_frame = "med_qlt_frame.yaml"
med_qlt_frame = open(file_med_qlt_frame, 'w')
med_qlt_frame.close()

file_med_qos_metrics = "med_qos_metrics.yaml"
med_qos_metrics = open(file_med_qos_metrics, 'w')
med_qos_metrics.close()
#######################################

# Analise de QoE
for video_n in video_dict:

    file_bitrate_time_aux = "bitrate_time_aux_{}.yaml".format(video_n)
    yaml_final_bitrate_time = open(file_bitrate_time_aux, 'w')
    file_plot_bitrate_time = "bitrate_time_{}.csv".format(video_n)
    plot_bitrate_time = open(file_plot_bitrate_time, 'w')
    plot_bitrate_time.close()
    yaml_final_bitrate_time.close()

    video = video_n
    video_len = video_dict[video_n][1]
    vid_sim_path = video_dict[video_n][0]

    sim_parse_file = 0

    for sim_file in glob.iglob(sim_runs_folder):
        sim_parse_file += 1
        command = 'python parse_sim_log_qoe.py {} {} {} {} {}'.format(video, video_len, sim_file, vid_sim_path, sim_parse_file)
        print ('Running command: ' + command)
        subprocess.call(command, shell=True)

    print("All QOE {} sim(s) parsed.".format(sim_parse_file))

    file_bitrate_time_aux = "bitrate_time_aux_{}.yaml".format(video)
    yaml_final_bitrate_time = open(file_bitrate_time_aux, 'r')
    file_plot_bitrate_time = "bitrate_time_{}.csv".format(video)
    plot_bitrate_time = open(file_plot_bitrate_time, 'w')

    bitrate_time_dict = yaml.load(yaml_final_bitrate_time)

    plot_bitrate_time.write("time; bitrate_mean;\n")
    for time in bitrate_time_dict:
        to_write = "{}; {};\n".format(time, bitrate_time_dict[time])
        plot_bitrate_time.write(to_write)

    plot_bitrate_time.close()
    yaml_final_bitrate_time.close()

#Analise de QoS
folder_qos = "/home/patrick/omnetpp-5.3/samples/vanet-dash-v.0.1/simulations/cars/"
sim_runs_folder_qos = folder_qos + "results/General-*.sca"
sim_parse_file_qos = 0

for sim_file in glob.iglob(sim_runs_folder_qos):
    sim_parse_file_qos += 1
    command = 'python parse_sim_log_qos.py {} {} {} {} {}'.format(video, video_len, sim_file, vid_sim_path, sim_parse_file_qos)
    print ('Running command: ' + command)
    subprocess.call(command, shell=True)

print("All QOS {} sim(s) parsed.".format(sim_parse_file))

