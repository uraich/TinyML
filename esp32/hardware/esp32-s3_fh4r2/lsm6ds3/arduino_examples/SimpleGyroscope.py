# SimpleGyroscope.py: a port of SimpleGyroscope.ino
# from the Arduino_LSM6DS3 library examples to MicroPython
# Author: U. Raich
# This program is part of the course on TinyML at the
# University of Cape Coast, Ghana
# It is released under the MIT license
# 26. Oct. 2025

from LSM6DS3_i2c import LSM6DS3_I2C
from LSM6DS3_const import *
from utime import sleep_ms

lsm6ds3 = LSM6DS3_I2C()
print("Device ID: 0x{:02x}".format(lsm6ds3.getDeviceID))
print("Reset the device")
lsm6ds3.sw_reset()
sleep_ms(10)

# The following is done in the "begin" method of the Arduino LSM6DS3 class

# Read the device ID
deviceID = lsm6ds3.getDeviceID
print("Device ID: 0x{:02x}".format(deviceID))
if not deviceID == 0x6c and not deviceID == 0x69:
    print("Read wrong device ID")
# Setting up the gyroscope control register to work at 104 Hz, 2000 dps and
# in bypass mode

lsm6ds3.gyro_full_scale = "2000 dps"
lsm6ds3.gyro_odr = "104 Hz"
print("Gyroscope control register (LSM6DS3_CTRL2_G): 0x{:02x}".format(lsm6ds3.ctrl2_g))

# Set the Accelerometer control register to work at 104 Hz, 4 g,and in bypass mode and enable ODR/4
# low pass filter (check figure9 of LSM6DS3's datasheet)
lsm6ds3.acc_odr = "104 Hz"
lsm6ds3.acc_full_scale = "4g"
lsm6ds3.acc_bandwidth = "100 Hz"
print("Acceleration sensor control register (LSM6DS3_CTRL1_XL): 0x{:02x}".format(lsm6ds3.ctrl1_xl))
print("Angular rate sensor control register (LSM6DS3_CTRL7_G): 0x{:02x}".format(lsm6ds3.ctrl7_g))

# end of the begin method simulation

# lsm6ds3.debugging=True
gyroSamplingRate = lsm6ds3.gyro_odr;
print("Gyroscope sampling rate: " + lsm6ds3.gyro_odr_txt(gyroSamplingRate))
print("Gyrosope in degrees/second")
print("X\tY\tZ")
while True:
    while not lsm6ds3.acc_data_available:
        # print("no temperature data yet")
        sleep_ms(10)
    gyro_data = lsm6ds3.gyro
    print("{:4.2f}\t{:4.2f}\t{:4.2f}".format(gyro_data[0],gyro_data[1],gyro_data[2]))
    sleep_ms(10)

