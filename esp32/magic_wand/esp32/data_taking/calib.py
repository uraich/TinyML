# calib.py Measure the average accelerometer and gyroscope data and print them
# These values can be used as inital values for
# Estimate_Gyroscope_Drift and EstimateGravityDirection of the magic wand
# program
# Copyright (c) U.Raich, 24. Feb. 2026
# This program is part of the TinyML course at the
# University of Cape Coast,Ghana
# It is released under the MIT license

from lsm6ds3_imu import LSM6DS3_IMU
from micropython import const
from time import sleep_ms
import math
import sys
from ulab import numpy as np

NO_OF_SAMPLES_TO_AVG = const(100)
NOISE_MEAS           = const(200)

avr_gyroscope_drift = np.empty((3,),dtype=np.float)
avr_gravity_direction = np.empty((3,),dtype=np.float)

imu =  LSM6DS3_IMU()
imu.setContinuousMode()
imu.printFifoRegisterSettings()

# read a number of accelerometer and gyroscope measurements and average them
# Do not move the IMU while running the program

print("Measuring the average gyroscope drift and the average gravity direction")
print("Do not move the IMU while running this program")

print("Raw Gyroscope and accelerometer values:")
for sample in range(NO_OF_SAMPLES_TO_AVG):
    while not imu.accelerationAndGyroscopeAvailable():
        # print("Waiting for data")
        continue
    new_gyro, new_accel    = imu.readAccelerationAndGyroscope()
    avr_gyroscope_drift   += new_gyro
    avr_gravity_direction += new_accel
    print("{:05.3f}, {:05.3f}, {:05.3f},   {:05.3f}, {:05.3f}, {:05.3f}".format(
        new_gyro[0], new_gyro[1], new_gyro[2], new_accel[0], new_accel[2], new_accel[2]))

avr_gyroscope_drift /= NO_OF_SAMPLES_TO_AVG
avr_gravity_direction /= NO_OF_SAMPLES_TO_AVG

print("Average gyroscope drift: {:05.3f}, {:05.3f}, {:05.3f}".format(
    avr_gyroscope_drift[0],avr_gyroscope_drift[1],avr_gyroscope_drift[2]))
print("Average gravity direction: {:05.3f}, {:05.3f}, {:05.3f}".format(
        avr_gravity_direction[0],avr_gravity_direction[1],
        avr_gravity_direction[2]))

print("Now we measure accelerometer and gyroscope again and subtract")
print("the average gyro drift and gravity direction")
print("This will show us the measurement noise")

for sample in range(NO_OF_SAMPLES_TO_AVG):
    while not imu.accelerationAndGyroscopeAvailable():
        # print("Waiting for data")
        continue
print("Gyroscope and accelerometer values with average gyro drift and average gravity subtracted: ")
for sample in range(NOISE_MEAS):
    while not imu.accelerationAndGyroscopeAvailable():
    # print("Waiting for data")
        continue
    new_gyro, new_accel = imu.readAccelerationAndGyroscope()
    gyro_corrected = new_gyro - avr_gyroscope_drift
    accel_corrected = new_accel - avr_gravity_direction
    '''
    print("{:05.3f}, {:05.3f}, {:05.3f},   {:05.3f}, {:05.3f}, {:05.3f}".format(
        gyro_corrected[0],gyro_corrected[1],gyro_corrected[2],
        accel_corrected[0],accel_corrected[1],accel_corrected[2]))
    '''
    print("{:05.3f}, {:05.3f}, {:05.3f}".format(
        gyro_corrected[0],gyro_corrected[1],gyro_corrected[2]))
