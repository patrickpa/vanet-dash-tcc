import re
import yaml
import sys
import glob
import math
from collections import OrderedDict


# in-line parameters #######################

running_video = sys.argv[1]
video_len = int(sys.argv[2])
vec_file_name = sys.argv[3]
vid_sim_path = sys.argv[4]
sim_parse_file = int(sys.argv[5])

############################################

file = open(vec_file_name, 'r')
vec_log = file.read()
file.close()

# m = re.compile(r"vector [0-9]+ Highway_AE\.car\[[0-9]\]\.tcpApp\[[0-9]\] DASHQualityLevel:vector ETV")
m = re.compile(r"vector [0-9]+ Highway_USP\.car\[[0-9]\]\.tcpApp\[[0-9]\] DASHQualityLevel:vector ETV")

all_vecs = m.findall(vec_log)

list_of_frames_qlt = {}

for vec in all_vecs[:10]:
    vector_number = vec.split(' ')[1]

    regex = "^{}\t[0-9]+\t[0-9]+\.[0-9]+\t[0-9]".format(vector_number)

    n = re.compile(r"{}".format(regex), flags=re.MULTILINE)
    all_val = n.findall(vec_log)
    list_of_frames_qlt[vector_number] = all_val

final_list = {}

for frame_list in list_of_frames_qlt:
    l = list_of_frames_qlt[frame_list]

    qlts_n_times = {}

    for frame in l:
        sim_qlt = frame.split("\t")[3]
        sim_time = frame.split("\t")[2]
        qlts_n_times[sim_time] = sim_qlt 

    final_list[frame_list] = qlts_n_times

dump = []


med_qlt_frame = ''

file_med_qlt_frame = "med_qlt_frame.yaml"
med_qlt_frame_file = open(file_med_qlt_frame, 'a')

file_plot_bitrate_time = "bitrate_time_aux_{}.yaml".format(running_video)
plot_bitrate_time = open(file_plot_bitrate_time, 'r')

bitrate_time_dict = yaml.load(plot_bitrate_time)
plot_bitrate_time.close()

if bitrate_time_dict == None:
    bitrate_time_dict = {}

count_sims = sim_parse_file * len(all_vecs)
for l in final_list:
    sim_dic = {}
    sim_dic['Name'] = running_video
    sim_dic['Sim_Number'] = count_sims
    sim_dic['Frames'] = []

    count_frames = 0
    qlt_sum = 0.0
    delay_sum = 0.0

    all_qltys = []
    all_delays = []

    ordered_final_list = {float(k):v for k,v in final_list[l].items()}
    ordered_final_list = OrderedDict(sorted(ordered_final_list.items()))

    frame_zero_time = 0.0

    for time in ordered_final_list:
        frame = ordered_final_list[time]
        frame_qlt = ''

        if count_frames == 0:
            frame_zero_time = time

        if count_frames < video_len:

            qlt_convert = 400.00

            if frame == '0':
                frame_qlt = '{}_l'.format(count_frames)
                qlt_convert = 400.00

            elif frame == '1':
                frame_qlt = '{}_m'.format(count_frames)
                qlt_convert = 800.00

            else:
                frame_qlt = '{}_h'.format(count_frames)
                qlt_convert = 1500.00

            sim_dic['Frames'].append(frame_qlt)
            all_qltys.append(qlt_convert)

            if float(time) > (frame_zero_time + 1.0):
                delay = (float(time) - (frame_zero_time + 1.0))
                delay_sum += delay
                all_delays.append(delay)
            else:
                delay_sum += 0.0
                all_delays.append(0.0)

            if time in bitrate_time_dict:
                bitrate_time_dict[time] = (bitrate_time_dict[time] + qlt_convert) / 2.0
            else:
                bitrate_time_dict[time] = qlt_convert

            frame_zero_time = time

            count_frames += 1
            qlt_sum += qlt_convert

    qlt_mean = qlt_sum/count_frames
    delay_mean = delay_sum/count_frames

    qlt_stddev = 0.0
    delay_stddev = 0.0

    for x in all_qltys:
        qlt_stddev += (x - qlt_mean) * (x - qlt_mean)

    if count_frames > 1:
        qlt_stddev /= count_frames - 1
    qlt_stddev = math.sqrt(qlt_stddev)

    for x in all_delays:
        delay_stddev += (x - delay_mean) * (x - delay_mean)

    if count_frames > 1:
        delay_stddev /= count_frames - 1
    delay_stddev = math.sqrt(delay_stddev)

    med_qlt_frame += "Qlt_mean {0}: {1}\nQlt_stddev{0}: {2}\n".format(running_video + str(count_sims) , qlt_mean, qlt_stddev)
    med_qlt_frame += "delayPlayBack_mean {0}: {1}\ndelayPlayBack_stddev {0}: {2}\n".format(running_video + str(count_sims) , delay_mean, delay_stddev)

    count_sims -= 1

    dump.append(sim_dic)

print (med_qlt_frame)

med_qlt_frame_file.write(med_qlt_frame)
med_qlt_frame_file.close()

file_plot_bitrate_time = "bitrate_time_aux_{}.yaml".format(running_video)
plot_bitrate_time_new = open(file_plot_bitrate_time, 'w')

yaml.dump(bitrate_time_dict, plot_bitrate_time_new, default_flow_style=False)

plot_bitrate_time_new.close()

count_dumps = sim_parse_file * len(all_vecs)
for d in dump:
    file_name = vid_sim_path + 'vid_sim_{}.yaml'.format(count_dumps)
    file_dump = open(file_name, 'w')

    yaml.dump(d, file_dump, default_flow_style=False)

    file_dump.close()

    count_dumps -= 1
