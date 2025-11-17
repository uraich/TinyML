# check_sampling_freq.py: Sets up the LSM6DS3 for FIFO use
# sets the sampling frequency and takes data for 10s
# defined by a timer
# Checks the no of samples received
# Copyright (c) U. Raich, Oct, 2023
# This program is part of the TinyML course at the
# University of Cape Coast, Ghana
# Change the FREQ constant between the values 26, 52, 104 and 208 and observe
# the no of samples seen

from LSM6DS3_i2c import LSM6DS3_I2C
from LSM6DS3_const import *
from utime import sleep_ms
from machine import Timer

def stop_data_taking():
    # This function is called when the timer expires
    global data_taking
    data_taking = False
    print("Data taking finished")
    
# create a timer
timer = Timer(0)

lsm6ds3 = LSM6DS3_I2C()
print("Device ID: 0x{:02x}".format(lsm6ds3.getDeviceID))
print("Reset the device")
lsm6ds3.sw_reset()
sleep_ms(2)

gyro_data = []
acc_data  = []
FREQ      = 208
print("---------------------------------------------------------")
print("Setting up the accelerometer")
print("output data rate: {:d} Hz, full scale: 4g".format(FREQ)) 
print("---------------------------------------------------------")

lsm6ds3.acc_odr="{:d} Hz".format(FREQ)
print("acc output datarate: 0x{:02x}".format(lsm6ds3.acc_odr))
print("This corresponds to " + lsm6ds3.acc_odr_txt(lsm6ds3.acc_odr))

print("Setting full scale to 4g")
lsm6ds3.acc_full_scale="4g"
full_scale = lsm6ds3.acc_full_scale
print("Acc full scale value: {:d}".format(full_scale))
print("Acc full scale: " + lsm6ds3.acc_full_scale_txt(full_scale))

print("---------------------------------------------------------")
print("Setting up the gyroscope")
print("output data rate: {:d} Hz, full scale: 2000 dps".format(FREQ)) 
print("---------------------------------------------------------")

lsm6ds3.gyro_odr="{:d} Hz".format(FREQ)
print("gyro output datarate: 0x{:02x}".format(lsm6ds3.gyro_odr))
print("This corresponds to " + lsm6ds3.gyro_odr_txt(lsm6ds3.gyro_odr))

print("Setting gyro full scale to 2000 dps")
lsm6ds3.gyro_full_scale="2000 dps"
full_scale = lsm6ds3.gyro_full_scale
print("Gyro full scale value: {:d}".format(full_scale))
print("Gyro full scale: " + lsm6ds3.gyro_full_scale_txt(full_scale))

print("---------------------------------------------------------")
print("Setting up FIFO")
print("---------------------------------------------------------\n")
print("Set watermark threshold")
lsm6ds3.fifo_threshold = 0x200
print("Fifo threshold set to 0x{:04x}".format(lsm6ds3.fifo_threshold))
print("Set fifo odr")
lsm6ds3.fifo_odr = "{:d} Hz".format(FREQ)
print("Fifo odr is set to {}".format(lsm6ds3.fifo_odr_txt(lsm6ds3.fifo_odr)))

print("Set the acc and gyro decimation factor to no decimation (factor = 1)")
lsm6ds3.fifo_acc_dec_factor  = 1
lsm6ds3.fifo_gyro_dec_factor = 1
print("acc decimation factor: {:d}".format(lsm6ds3.fifo_acc_dec_factor_txt(
    lsm6ds3.fifo_acc_dec_factor)))
print("gyro decimation factor: {:d}".format(lsm6ds3.fifo_gyro_dec_factor_txt(
    lsm6ds3.fifo_gyro_dec_factor)))
print("Set fifo mode to continuous")
lsm6ds3.fifo_mode = "continuous"
print("Fifo mode is set to 0x{:02x}".format(lsm6ds3.fifo_mode))
print("which corresponds to {}".format(lsm6ds3.fifo_mode_txt(lsm6ds3.fifo_mode)))

data_taking = True
print("Start data taking")
timer.init(period=10000,mode=Timer.ONE_SHOT, callback = lambda src : stop_data_taking())

no_of_samples = 0
while data_taking:
    while lsm6ds3.fifo_empty:
        sleep_ms(1)
    # Read no of values in fifo
    data_count = lsm6ds3.words_in_fifo
    # print("{:d} values in fifo".format(data_count))
    if data_count %6 :
        print("wrong data in FIFO")
    no_of_samples += data_count // 6
    for i in range(data_count // 6):
        gyro_x_raw = lsm6ds3.fifo_data
        gyro_y_raw = lsm6ds3.fifo_data
        gyro_z_raw = lsm6ds3.fifo_data
        gyro_data.append((gyro_x_raw,gyro_y_raw,gyro_z_raw))
        # print(no_of_samples,len(gyro_data))
        acc_x_raw  = lsm6ds3.fifo_data
        acc_y_raw  = lsm6ds3.fifo_data
        acc_z_raw  = lsm6ds3.fifo_data
        acc_data.append((acc_x_raw,acc_y_raw,acc_z_raw))
        if lsm6ds3.fifo_overrun:
            print("FiFo overrun error")
print("no of samples: {:d}".format(no_of_samples)) 
print("length of data array: acc: {:d}, gyro: {:d}".format(len(acc_data),len(gyro_data)))
