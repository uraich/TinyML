#!/home/uli/.virtualenvs/pyqt/bin/python
# draw_circle_pyqt.py: Draw a circle using the plot widget in pyqt6
# This is a test program in view of an implementation of the magic wand
# TinyML program
# Copyright (c) U. Raich, 24.11.2025 
# It is part of the course on TinyML at the
# University of Cape Coast, Ghana

import pyqtgraph as pg
from PyQt6 import QtWidgets

from math import pi,sin,cos

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.plot_graph = pg.PlotWidget()
        self.setCentralWidget(self.plot_graph)
        self.plot_graph.setBackground("w")
        self.pen = pg.mkPen(color=(0, 0, 0), width=2)
        
    def plot(self,radius,x,y):
        self.plot_graph.setTitle("Circle of radius {:4.2f}".format(radius))
        self.plot_graph.plot(x, y, pen=self.pen)


app = QtWidgets.QApplication([])
main = MainWindow()

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

main.plot(radius,x,y)
main.show()
app.exec()

