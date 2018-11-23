import yaml

final_file = "final_metrics.yaml"
final_output = {}

qos = "med_qos_metrics.yaml"
qoe = "med_qlt_frame.yaml"
buff = "med_buffersize.yaml"

yaml_qos = yaml.load(open(qos, 'r'))
yaml_qoe = yaml.load(open(qoe, 'r'))
yaml_buff = yaml.load(open(buff, 'r'))

end_to_end_delay_mean = 0.0
end_to_end_delay_stddev = 0.0
pck_loss_mean = 0.0
pck_loss_stddev = 0.0

c1 = 0
c2 = 0

for i in yaml_qos:
    if 'end_to_end_delay' in i:
        end_to_end_delay_mean += yaml_qos[i]['mean']
        end_to_end_delay_stddev += yaml_qos[i]['stddev']
        c1 += 1
    if 'pk_loss' in i:
        pck_loss_mean += yaml_qos[i]['mean']
        pck_loss_stddev += yaml_qos[i]['stddev']
        c2 += 1

end_to_end_delay_mean /= float(c1)
end_to_end_delay_stddev /= float(c1)
pck_loss_mean /= float(c2)
pck_loss_stddev /= float(c2)

final_output['end_to_end_delay'] = {'mean':end_to_end_delay_mean, 'stddev': end_to_end_delay_stddev}
final_output['pck_loss'] = {'mean': pck_loss_mean, 'stddev': pck_loss_stddev}

print("QoS Metrics:")
print (end_to_end_delay_mean, end_to_end_delay_stddev, pck_loss_mean, pck_loss_stddev)

c = 0.0
qlt_mean = 0.0
qlt_stddev = 0.0
delay_mean = 0.0
delay_stddev = 0.0

for i in yaml_qoe:
    if 'Qlt_mean' in i:
        qlt_mean += yaml_qoe[i]
    if 'Qlt_stddev' in i:
        qlt_stddev += yaml_qoe[i]
    if 'delayPlayBack_mean' in i:
        delay_mean += yaml_qoe[i]
    if 'delayPlayBack_stddev' in i:
        delay_stddev += yaml_qoe[i]
    c += 1.0

c /= 4.0

qlt_mean /= c
qlt_stddev /= c
delay_mean /= c
delay_stddev /= c

final_output['Qlt'] = {'mean':qlt_mean , 'stddev': qlt_stddev}
final_output['Delay_Playback'] = {'mean': delay_mean, 'stddev': delay_stddev} 

print("QoE Metrics:")
print(qlt_mean, qlt_stddev, delay_mean, delay_stddev)

c = 0.0
buff_mean = 0.0
buff_stddev = 0.0

for i in yaml_buff:
    if 'BufferSize_mean' in i:
        buff_mean += yaml_buff[i]
    if 'BufferSize_stddev' in i:
        buff_stddev += yaml_buff[i]
    c += 1.0

c /= 2.0

buff_mean /= c
buff_stddev /= c
final_output['BufferSize'] = {'mean': buff_mean, 'stddev': buff_stddev}

print("Buff Metrics:")
print(buff_mean, buff_stddev)


output = open(final_file, 'w')
yaml.dump(final_output, output, default_flow_style=False)
output.close()










