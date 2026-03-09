# acc-gyro.py Measure accelerometer and gyroscope data and print them

# Copyright (c) U.Raich, 24. Feb. 2026
# This program is part of the TinyML course at the
# University of Cape Coast,Ghana
# It is released under the MIT license

from lsm6ds3_imu import LSM6DS3_IMU
from micropython import const
from time import sleep_ms
import sys

imu =  LSM6DS3_IMU()
imu.setContinuousMode()
imu.printFifoRegisterSettings()

# read a number of accelerometer and gyroscope measurements print them

print("Measuring the accelation and angular rotation speed using the accelerometer and gyroscope")

print("Raw Gyroscope and accelerometer values:")
try:
    while True:
        while not imu.accelerationAndGyroscopeAvailable():
            # print("Waiting for data")
            continue
        new_gyro, new_accel    = imu.readAccelerationAndGyroscope()

        print("{:05.3f}, {:05.3f}, {:05.3f},   {:05.3f}, {:05.3f}, {:05.3f}".format(
            new_gyro[0], new_gyro[1], new_gyro[2], new_accel[0], new_accel[2], new_accel[2]))

except KeyboardInterrupt:
    sys.exit(0)
