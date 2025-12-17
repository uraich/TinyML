#!/home/uli/.virtualenvs/pyqt/bin/python
# ledTest.py: Read the sin.txt file and use these data as LED light intensity
# Copyright U. Raich, 26.11.2025
#

import matplotlib.pyplot as plt

x = []
y = []
intensity = []
maxIntensity = 100
# read the file and store the data into an x,y array
with open('sin.txt', 'r') as file:
    for line in file:
        # print(line.strip())
        point = line.split()
        x.append(float(point[0]))
        y.append(float(point[1]))
        print(float(point[0]), float(point[1]))
# This was used to figure out, why the LED was sometimes flashing very bright:
# The y values my become slightly negative and we must limit the intensity to
# zero. Negative intensity numbers result in the bright flash
        intens = int(((float(point[1])+1)/2)*maxIntensity)
        # print(intens)

plt.title("Output from the TinyML hello world model")
plt.plot(x,y)
plt.show()
