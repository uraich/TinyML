#!/home/uli/.virtualenvs/AI/bin/python
# show_samples.py: displays the sample files

import numpy as np
import matplotlib.pyplot as plt

fig, axs = plt.subplots(2,5,num="MNIST samples")
plt.set_cmap('Greys')

for i in range(2):
    for j in range(5):
        filename = "sample{:d}.bin".format(5*i+j)
        f = open(filename,"rb")
        pixels = f.read()
        f.close()
        pixel_array = np.frombuffer(pixels,dtype=np.int8)
        # reshape the array to (28,28)
        pixel_array = pixel_array.reshape(28,28)
        axs[i,j].axis('off')
        axs[i,j].imshow(pixel_array)
plt.show()
        
