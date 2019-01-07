import re
import yaml
import sys
import glob
import math

# in-line parameters #######################

running_video = sys.argv[1]
video_len = int(sys.argv[2])
vec_file_name = sys.argv[3]
vid_sim_path = sys.argv[4]
sim_parse_file = int(sys.argv[5])

############################################

num_sim = 10

file = open(vec_file_name, 'r')
vec_log = file.read()
file.close()

file_med_qos_metrics = "med_qos_metrics.yaml"
med_qos_metrics = open(file_med_qos_metrics, 'a')

# m = re.compile(r"statistic Highway_AE\.car\[[0-9]\]\.tcpApp\[[0-9]\] endToEndDelay:histogram\nfield count [0-9]+\nfield mean [0-9]+\.[0-9]+\nfield stddev [0-9]+\.[0-9]+\n")
m = re.compile(r"statistic Highway_USP\.car\[[0-9]\]\.tcpApp\[[0-9]\] endToEndDelay:histogram\nfield count [0-9]+\nfield mean [0-9]+\.[0-9]+\nfield stddev [0-9]+\.[0-9]+\n")
all_vecs = m.findall(vec_log)

vecs_sum = 0
mean = 0
stddev = 0

for vec in all_vecs:
    vec_lines = vec.split('\n')
    vecs_sum += 1

    for line in vec_lines[2:-1]:
        metric = line.split(' ')

        if metric[1] == 'mean':
            mean += float(metric[2])
        else:
            stddev += float(metric[2])

mean /= vecs_sum
stddev /= vecs_sum

output = "end_to_end_delay mean/stddev {}:\n  mean: {}\n  stddev: {}\n".format(sim_parse_file, mean, stddev)

med_qos_metrics.write(output)

# n = re.compile(r"scalar Highway_AE\.car\[[0-9]\]\.tcpApp\[[0-9]\] sentPk:count [0-9]+")
n = re.compile(r"scalar Highway_USP\.car\[[0-9]\]\.tcpApp\[[0-9]\] sentPk:count [0-9]+")
all_sent = n.findall(vec_log)

#m = re.compile(r"scalar Highway_AE\.car\[[0-9]\]\.tcpApp\[[0-9]\] rcvdPk:count [0-9]+")
m = re.compile(r"scalar Highway_USP\.car\[[0-9]\]\.tcpApp\[[0-9]\] rcvdPk:count [0-9]+")
all_rcvd = m.findall(vec_log)

sr_dif_total = 0.0
car_count = 0
for v in all_sent:
    car_sent = v.split(' ')[3]
    car_rcvd = all_rcvd[car_count].split(' ')[3]

    miss = (float(car_sent) - float(car_count)) / float(car_sent)

    sr_dif_total += miss
    car_count += 1

sr_dif_total /= car_count

stddev_pck_loss = 0.0
car_count = 0

for v in all_sent:
    car_sent = v.split(' ')[3]
    car_rcvd = all_rcvd[car_count].split(' ')[3]

    miss = (float(car_sent) - float(car_count)) / float(car_sent)

    stddev_pck_loss += (miss - sr_dif_total) * (miss - sr_dif_total)
    car_count += 1

stddev_pck_loss = math.sqrt(stddev_pck_loss / float(car_count))

output_pk_loss = "pk_loss mean {}:\n  mean: {}\n  stddev: {}\n".format(sim_parse_file, sr_dif_total, stddev_pck_loss)
med_qos_metrics.write(output_pk_loss)

med_qos_metrics.close()

