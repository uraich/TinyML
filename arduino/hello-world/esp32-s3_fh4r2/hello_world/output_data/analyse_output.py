#!/home/uli/.virtualenvs/AI/bin/python
# analyse_output.py: This is a helper program for the hello world TinyML demo.
# It takes the file created by:
# minicom | grep tee output.txt
# und plots the data
# As comparison a regular sine wave is plotted
# Copyright (c) U. Raich, 26.Nov. 2025
# This program is part of the TinyML course at the
# University of Cape Coast, Ghana.
# It is released under the MIT license

# import the needed libraries
import matplotlib.pyplot as plt
from math import sin, pi

# Read only lines that have the text x_value in them
helloWorldDataFilename = "output.txt"
dataFile = open(helloWorldDataFilename,"r")
x_values = []
y_values = []
fileContent = []
line = dataFile.readline()
while line:
    start = line.find("x_value")
    if start != -1:
        line = line[start:]
        fileContent.append(line.strip())
    line = dataFile.readline()
    
# Find the first line where both x and y values are zero
first_index = 0
while True:
    p = fileContent[first_index].split(',')
    if '0.00000' in p[0] and '0.00000' in p[1]:
        print("First index: ",first_index)
        print(fileContent[first_index])
        break
    else :
        first_index += 1

# find the line where the next cycle starts
last_index = first_index+1
while True:
    p = fileContent[last_index].split(',')
    if '0.00000' in p[0] and '0.00000' in p[1]:
        print("Last index: ",last_index)
        print(fileContent[last_index])
        break
    else :
        last_index += 1

print("Line index where the current sine cycle starts: ",first_index)
print("Index of line starting a new sine cycle: ",last_index)
print("Line starting a new cycle: ",fileContent[last_index])
noOfDataPoints = last_index - first_index
print("This corresponds to ",noOfDataPoints, " values")

# Go through one cycle and extract the x and y values
for index in range(first_index,last_index):
    values = fileContent[index].split(',')
    x_values.append(float(values[0][values[0].find(':') +1 :]))
    y_values.append(float(values[1][values[1].find(':') +1 :]))

# Plot the results and compare them to a regular sine cycle
x_comparison = []
y_comparison = []
for i in range(noOfDataPoints):
    x_comparison.append(2.0*pi*i/noOfDataPoints)
    y_comparison.append(sin(x_comparison[i]))

plt.title("Output from the hello world Tensorflow model")
plt.plot(x_values,y_values)
plt.plot(x_comparison,y_comparison)
plt.show()
