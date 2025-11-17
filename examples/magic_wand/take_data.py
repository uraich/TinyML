# take_data.py: reads the acceleration and gyroscope data for 5s
# and saves the results into files
# The acceleration and gyroscope data are used to check the algorithm
# preparing the input tensor to the magic wand model
# Copyright (c) U. Raich Dec 2023
# This program is part of the TinyML course at the
# University of Cape Coast, Ghana
# It is released under the MIT license

from lsm6ds3_imu import LSM6DS3_IMU
from utime import sleep_ms
from micropython import const
import math, sys

IMU = LSM6DS3_IMU()
IMU.setContinuousMode() # enable the fifo

acceleration_data = []
gyroscope_data    = []
data_index = 0

print("Start taking data")

for i in range(500): # this corresponds to ~ 5s at a sampling rate of 104 Hz
    while not IMU.accelerationAndGyroscopeAvailable():
        sleep_ms(2)
    data_count, gyro_samples,acc_samples = IMU.readAccelerationAndGyroscope()
    data_index += data_count
    for i in range(data_count):
        acceleration_data.append(acc_samples[i])
        gyroscope_data.append(gyro_samples[i])

# write the measure data to disk
print("No of samples taken: {:d}, length of data array: {:d}".format(data_index,
                                                                     len(acceleration_data)))
f = open("acceleration_data.txt","w")
f.write("x, y, z\n")
for i in range(len(acceleration_data)):
    f.write("{:8.4f}, {:8.4f}, {:8.4f}\n".format(acceleration_data[i][0],
                                                 acceleration_data[i][1],
                                                 acceleration_data[i][2]))
f.close()

f = open("gyroscope_data.txt","w")
f.write("x, y, z\n")
for i in range(len(gyroscope_data)):
    f.write("{:8.4f}, {:8.4f}, {:8.4f}\n".format(gyroscope_data[i][0],
                                                 gyroscope_data[i][1],
                                                 gyroscope_data[i][2]))
f.close()

