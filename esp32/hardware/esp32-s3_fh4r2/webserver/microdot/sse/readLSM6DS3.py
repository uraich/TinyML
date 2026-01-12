# readLSM6DS3.py: Test program to read the lsm6ds3 and print the
# accelerometer, gyroscope and timestamp.
# The code is to be integrated into the SSE WEB server later
# Copyright (c) U. Raich, 6. Jan. 2026
# The program is part of the TinyML course at the
# University of Cape Coast, Ghana
# It is released under the MIT license

from wifi_connect import *
from LSM6DS3_i2c import LSM6DS3_I2C
from LSM6DS3_const import *
from utime import sleep_ms

connect()
ipaddr=getIPAddress()

lsm6ds3 = LSM6DS3_I2C()
print("Device ID: 0x{:02x}".format(lsm6ds3.getDeviceID))
print("Reset the device")
lsm6ds3.sw_reset()
sleep_ms(10)

print("---------------------------------------------------------")
print("Setting up the accelerometer") 
print("output data rate: 26 Hz, full scale 4g, bw: 50Hz") 
print("---------------------------------------------------------")

lsm6ds3.acc_odr="26 Hz"
print("acc output datarate: 0x{:02x}".format(lsm6ds3.acc_odr))
print("This corresponds to " + lsm6ds3.acc_odr_txt(lsm6ds3.acc_odr))
print("The numerical value is {:6.1f}".format(lsm6ds3.acc_odr_value(
     lsm6ds3.acc_odr_txt(lsm6ds3.acc_odr))))    
print("Setting full scale to 4g")
lsm6ds3.acc_full_scale="4 g"
full_scale = lsm6ds3.acc_full_scale
print("Acc full scale value: {:d}".format(full_scale))
print("Acc full scale: " + lsm6ds3.acc_full_scale_txt(full_scale))

lsm6ds3.acc_bandwidth = "50 Hz"
print("acc bandwidth: 0x{:02x}".format(lsm6ds3.acc_bandwidth))
print("This corresponds to " + lsm6ds3.acc_bandwidth_txt(lsm6ds3.acc_bandwidth))
print("ctrl1_xl: 0x{:02x}".format(lsm6ds3.ctrl1_xl))
      
print("---------------------------------------------------------")
print("Setting up the gyroscope")
print("output data rate: 26 Hz, full scale: 2000 dps") 
print("---------------------------------------------------------")

lsm6ds3.gyro_odr="26 Hz"
print("gyro output datarate: 0x{:02x}".format(lsm6ds3.gyro_odr))
print("This corresponds to " + lsm6ds3.gyro_odr_txt(lsm6ds3.gyro_odr))
print("The numerical value is {:6.1f}".format(lsm6ds3.gyro_odr_value(
     lsm6ds3.gyro_odr_txt(lsm6ds3.gyro_odr))))

print("Setting gyro full scale to 2000 dps")
lsm6ds3.gyro_full_scale="2000 dps"
full_scale = lsm6ds3.gyro_full_scale
print("Gyro full scale value: {:d}".format(full_scale))
print("Gyro full scale: " + lsm6ds3.gyro_full_scale_txt(full_scale))

sleep_ms(40)  # wait for the data to become ready 40ms <=> 25Hz
print("Time Stamp:\t\tacc_x,   acc_y,   acc_z,   gyro_x,  gyro_y,  gyro_z")
while True:
    while not lsm6ds3.acc_data_available:
        sleep_ms(1)
    acc_x = lsm6ds3.acc_x
    acc_y = lsm6ds3.acc_y
    acc_z = lsm6ds3.acc_z

    gyro_x = lsm6ds3.gyro_x
    gyro_y = lsm6ds3.gyro_y
    gyro_z = lsm6ds3.gyro_z
    
    timeStamp=dateString(cetTime())

    print("{:s}, \t{:5.3f},   {:5.3f},  {:5.3f},  {:5.3f},  {:5.3f},   {:5.3f}".format(
        timeStamp,acc_x,acc_y,acc_z,gyro_x,gyro_y,gyro_z))
    sleep_ms(500)
