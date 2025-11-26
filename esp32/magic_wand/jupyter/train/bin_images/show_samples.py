#!/home/uli/.virtualenvs/AI/bin/python
import numpy as np
import matplotlib.pyplot as plt

fig, axs = plt.subplots(2,5,num="strokes")
for i in range(2):
    for j in range(5):
        filename = "digit_{:d}.bin".format(5*i+j)
        # print("filename: ",filename)
        raster = np.fromfile(filename,dtype=np.uint8)
        # reshape the array to (32,32,3)
        # Use Matplotlib to show the image
        axs[i,j].axis('off')
        axs[i,j].imshow(raster.reshape(32,32,3))
fig.tight_layout()
plt.show()

