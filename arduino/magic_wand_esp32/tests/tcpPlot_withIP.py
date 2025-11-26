#!/home/uli/.virtualenvs/pyqt/bin/python
# tcpPlot_withIP.py plots data coming from a TCP server
# This is a test program for the magic wand demo
# It receives
# - the number of data to follow
# - x,y point data
# In the final program the magic wand stroke data will be transmitted
# and plotted for inspection
# Copyright (c) U. Raich, 24.11.2025
# This program is part of the TinyML course
# at the University of Cape Coast, Ghana
# It is released under the MIT license

import sys,socket
import pyqtgraph as pg
from PyQt6 import QtWidgets
x = []
y = []

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.plot_graph = pg.PlotWidget()
        self.setCentralWidget(self.plot_graph)
        self.plot_graph.setBackground("w")
        self.pen = pg.mkPen(color=(0, 0, 0), width=2)
        
    def plot(self,x,y):
        self.plot_graph.setTitle("Data from the ESP32 TCP server")
        self.plot_graph.plot(x, y, pen=self.pen)

def client_program(host_ip):

    host = socket.gethostname()  # as both code is running on same pc
    port = 5000  # socket server port number

    client_socket = socket.socket()  # instantiate
    print("Connecting to ",host,":",port)
    try:
        client_socket.connect((host_ip, port))  # connect to the server
    except OSError as error:
        print("Connection failed, please check IP address and port number")
        sys.exit()
        
    # Receive connection message and print it
    server_msg = client_socket.recv(64).decode()  # receive response
    print(server_msg)
    message = "ok\r\n"
    client_socket.send(message.encode())

    # get the points
    index = 0
    while True:
        server_msg = client_socket.recv(64).decode()
        if server_msg.lower().strip() == 'bye':
            break;
        if server_msg[:2] == "\r\n":
            server_msg = server_msg[2:]
        # print("Length of server message: ",len(server_msg))
        if server_msg == "":
            continue
        # print("Server message: ",server_msg)
        # print(server_msg)
        # b = bytearray()
        # b.extend(map(ord, server_msg))
        # for i in range(len(b)):
        #     print("0x{:02x}, ".format(b[i]),end="")
        # print("")
    
        data = server_msg.split(sep="\r\n")[0]
        # print("data: ",data)
        point = data.split(',')
        x.append(float(point[0]))
        y.append(float(point[1]))
        # print("index: ",index)
        print("Point: {:4.2f}, {:4.2f}".format(x[index],y[index]))
        index += 1
        client_socket.send(message.encode())

    print("bye seen")
    # plt.title("Data from the TCP server")
    # plt.plot(x,y)
    # plt.show()
    client_socket.close()  # close the connection
    return

if __name__ == '__main__':
    # check if IP address has been given
    if len(sys.argv) != 2:
        print("Usage: client_withIP IP_address_of_your_server")
        print("e.g. client_withIP 192.168.0.46")
        sys.exit()
        
    app =  QtWidgets.QApplication([])
    main = MainWindow()
    client_program(sys.argv[1])

    main.plot(x,y)
    main.show()
    app.exec()
