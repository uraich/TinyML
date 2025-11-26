#!/home/uli/.virtualenvs/AI/bin/python
# plotstrokes.py: plot the stroke files. These files are used to check out
# the BlueTooth communication mechanism
# copyright (c) U. Raich 11.11.2025
# This program is part of the course on TinyML at the
# University of Cape Coast, Ghana
# It is released under the MIT license

import matplotlib.pyplot as plt

def plotStrokes():
    fig, axs = plt.subplots(5,2,figsize=(8, 15))
    fig.suptitle("The 10 different digit strokes",y=1.0)
    
    for s in range(10):
        strokeFilename = "digit_{:d}.txt".format(s)
        strokeFile = open(strokeFilename,"r")
        strokeData = strokeFile.readlines()
        x_array = []
        y_array = []
    
        for i in range(len(strokeData)):
            xy = strokeData[i].split()
            x_array.append(float(xy[0]))
            y_array.append(float(xy[1]))
        # print(x)
            if s < 5:
                l = 0
                k = s
            else:
                l = 1
                k = s-5
            
            axs[k,l].set_title("Stroke file: {:s}".format(strokeFilename))
            axs[k,l].set_xlabel('x')
            axs[k,l].set_ylabel('y')
            axs[k,l].set_xlim(-0.5, 0.5)
            axs[k,l].set_ylim(-0.5, 0.5)
            axs[k,l].plot(x_array, y_array)
        
    fig.tight_layout()
    plt.show() 

plotStrokes()
