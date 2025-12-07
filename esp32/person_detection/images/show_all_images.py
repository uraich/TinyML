#!/home/uli/.virtualenvs/AI/bin/python
# shows all nine example images for person detection testing
# Copyright (c) U. Raich, Dec 2025

import os
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt

def read_img(img_path):
  """Read person / not a person image

  Args:
      img_path (str): path to an image file

  Returns:
      np.array : image in the correct np.array format
  """
  image = Image.open(img_path)
  data = np.asarray(image, dtype=np.float32)
  if data.shape != (96, 96):
    raise ValueError(
        "Invalid input image shape (image should have shape 96*96)"
    )
  # Normalize the image if necessary
  if data.max() > 1:
   data = data / 255.0
  # Model inference requires batch size one
  return data

pixel_array = [None]*9
for img in range(9):
    filename = "image{:d}.png".format(img)
    pixel_array[img] = read_img(filename)

fig, axs = plt.subplots(3,3)
for i in range(3):
    for j in range(3):
        axs[i,j].axis('off')
        axs[i,j].imshow(pixel_array[3*i+j],cmap="gray")

plt.show()
