import re
import yaml
import sys

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

m = re.compile(r"vector [0-9]+ Highway\.car\[[0-9]\]\.tcpApp\[[0-9]\] DASHQualityLevel:vector ETV")
all_vecs = m.findall(vec_log)

list_of_frames_qlt = {}

for vec in all_vecs:
    vector_number = vec.split(' ')[1]

    regex = "^{}\t[0-9]+\t[0-9]+\.[0-9]+\t[0-9]".format(vector_number)

    n = re.compile(r"{}".format(regex), flags=re.MULTILINE)
    all_val = n.findall(vec_log)
    list_of_frames_qlt[vector_number] = all_val

final_list = {}

for frame_list in list_of_frames_qlt:
    l = list_of_frames_qlt[frame_list]

    qlts = []

    for frame in l:
        sim_qlt = frame.split("\t")[3]
        qlts.append(sim_qlt)      

    final_list[frame_list] = qlts

dump = []

count_sims = 1 * sim_parse_file
for l in final_list:
    sim_dic = {}
    sim_dic['Name'] = running_video
    sim_dic['Sim_Number'] = count_sims
    sim_dic['Frames'] = []

    count_frames = 0

    for frame in final_list[l]:
        frame_qlt = ''

        if count_frames < video_len:

            if frame == '0':
                frame_qlt = '{}_l'.format(count_frames)

            elif frame == '1':
                frame_qlt = '{}_m'.format(count_frames)

            else:
                frame_qlt = '{}_h'.format(count_frames)

            sim_dic['Frames'].append(frame_qlt)
            count_frames += 1

    count_sims += 1

    dump.append(sim_dic)

count_dumps = 0
for d in dump:
    file_name = vid_sim_path + 'vid_sim_{}.yaml'.format(count_dumps)
    file_dump = open(file_name, 'w')

    yaml.dump(d, file_dump, default_flow_style=False)

    file_dump.close()

    count_dumps += 1
