from matplotlib import pyplot as plt
import csv
import yaml

x = []
y = []

with open('buffersize_time_BusyStreetScene.csv','r') as csvfile:
    plots = csv.reader(csvfile, delimiter=';')
    for row in plots:
        x.append(float(row[0]))
        y.append(float(row[1]))

plt.plot(x,y, label='Buffer Size')
plt.xlabel('x')
plt.ylabel('y')
plt.title('Buffer Size x Time\n')
plt.legend()
plt.show()