#!/home/uli/.virtualenvs/pyqt/bin/python
# draw_circle.py: Draw a circle using matplotlib
# This is a test program in view of an implementation of the magic wand
# TinyML program
# Copyright (c) U. Raich, 24.11.2025 
# It is part of the course on TinyML at the
# University of Cape Coast, Ghana

import matplotlib.pyplot as plt
from math import pi,sin,cos

# The parametric formula of a circle is:
# x = r*cos(phi)
# y = r*sin(phi)

radius = 2
noOfPoints=100

x = []
y = []

for r in range(noOfPoints+1):
    x.append(radius*cos(2*pi*r/noOfPoints))
    y.append(radius*sin(2*pi*r/noOfPoints))

plt.title("Circle with radius {:4.2f}".format(radius))
plt.plot(x,y)
plt.show()
