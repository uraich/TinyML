#!/usr/bin/python3
import numpy as np
import matplotlib.pyplot as plt

stroke_pixels = []
for i in range(10):
    f = open("{:d}.bin".format(i),"rb")
    stroke_pixels.append((np.frombuffer(f.read(),dtype=np.int8) + 128).reshape((32,32,3)))


fig,ax = plt.subplots(2,5)
fig.suptitle("Stroke test data for all 10 digits")
for i in range(2):
    for j in range(5):
        ax[i,j].set_axis_off()
        ax[i,j].imshow(stroke_pixels[i*5+j])
plt.show()
