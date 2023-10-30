# imu_lsm6ds3.py: replacement of the LSM9DS1 arduino class using the LSM6DS3
# since there is no magnetometer and it is not used by the magic wand
# these functions are removed.
# Copyright (c) U. Raich Oct 2023
# This program is part of the TinyML course at the
# University of Cape Coast, Ghana
# It is released under the MIT license

from LSM6DS3_i2c import LSM6DS3_I2C
from LSM6DS3_const import *
from utime import sleep_ms

class LSM6DS3_IMU(object):
    def __init__(self,debug=False):
        self.debug = debug
        if self.debug:
            print("LSM6DS3_IMU debugging enabled")
        else:
            print("LSM6DS3_IMU debugging disabled")
            
        self.lsm6ds3 = LSM6DS3_I2C()
        # reset the imu
        self.lsm6ds3.sw_reset()
        sleep_ms(19)
        self.lsm6ds3.if_add_inc = LSM6DS3_ENABLE # automatic address increment
        # set gyro output data rate to 26 Hz, full scale to 2000 dps
        self.lsm6ds3.gyro_odr = "26 Hz"
        self.lsm6ds3.gyro_full_scale = "2000 dps"
        # set acc output data rate to 26 Hz, full scale to 4g
        self.lsm6ds3.acc_odr = "26 Hz"
        self.lsm6ds3.acc_full_scale = "4g"
        self.lsm6ds3.acc_bandwidth = "50 Hz"

    @property
    def debugging(self):
        return self.debug
    @ debugging.setter
    def debugging(self,onOff):
        self.debug = onOff
        
    def setContinuousMode(self):
        self.lsm6ds3.fifo_odr = "26 Hz" # this enables the fifo
        self.lsm6ds3.fifo_mode = "continuous"
        self.lsm6ds3.fifo_acc_dec_factor  = 1
        self.lsm6ds3.fifo_gyro_dec_factor = 1
        if self.debug:
            print("fifo mode: {}".format(self.lsm6ds3.fifo_mode_txt(self.lsm6ds3.fifo_mode)))
            print("fifo odr : {}".format(self.lsm6ds3.fifo_odr_txt(self.lsm6ds3.fifo_odr)))
            print("fifo acc decimation factor: {:d}".format(
                self.lsm6ds3.fifo_acc_dec_factor_txt(self.lsm6ds3.fifo_acc_dec_factor)))
            print("fifo gyro decimation factor: {:d}".format(
                self.lsm6ds3.fifo_gyro_dec_factor_txt(self.lsm6ds3.fifo_gyro_dec_factor)))
        self.continuousMode = True

    def setOneShotMode(self):
        self.lsm6ds3.fifo_odr = "power down"
        self.lsm6ds3.fifo_mode = "bypass"
        lsm6ds3.fifo_gyro_dec_factor = 0
        lsm6ds3.fifo_gyro_dec_factor = 0
        self.continuousMode = False

    def accelerationAndGyroscopeAvailable(self):
        if self.debug:
            if not self.lsm6ds3.fifo_empty:
                print("Data available")
            else:
                print("fifo is empty")
        return (not self.lsm6ds3.fifo_empty)
            
    # Gyroscope and accelerometer must be read together
    # First the 3 values of the gyroscope
    # followed by the 3 values of the accelerometer

    def readGyroscope(self):
        gyro_x_raw =  lsm6ds3.fifo_data
        gyro_y_raw =  lsm6ds3.fifo_data
        gyro_z_raw =  lsm6ds3.fifo_data
        return (lsm6ds3.gyro_to_physical(gyro_x_raw),
                lsm6ds3.gyro_to_physical(gyro_y_raw),
                lsm6ds3.gyro_to_physical(gyro_z_raw))
                
    def readAcceleration(self):
        return
        acc_x_raw =  lsm6ds3.fifo_data
        acc_y_raw =  lsm6ds3.fifo_data
        acc_z_raw =  lsm6ds3.fifo_data
        return (lsm6ds3.acc_to_physical(acc_x_raw),
                lsm6ds3.acc_to_physical(acc_y_raw),
                lsm6ds3.acc_to_physical(acc_z_raw))
                
    def readAccelerationAndGyroscope(self):
        # Read no of values in fifo
        data_count = self.lsm6ds3.words_in_fifo // 6 # 3 acceleration + 3 gyroscope       
        gyro_samples = []
        acc_samples  = []
        for i in range(data_count):
            gyro_samples.append((self.lsm6ds3.gyro_to_physical(self.lsm6ds3.fifo_data),
                                 self.lsm6ds3.gyro_to_physical(self.lsm6ds3.fifo_data),
                                 self.lsm6ds3.gyro_to_physical(self.lsm6ds3.fifo_data)))
            acc_samples.append((self.lsm6ds3.acc_to_physical(self.lsm6ds3.fifo_data),
                                self.lsm6ds3.acc_to_physical(self.lsm6ds3.fifo_data),
                                self.lsm6ds3.acc_to_physical(self.lsm6ds3.fifo_data)))
        # returns the new samples as physical values in form of x,y,z tuples
        return data_count,gyro_samples,acc_samples
    
    def accelerationSampleRate(self):
        return self.lsm6ds3.acc_odr_value(self.lsm6ds3.acc_odr_txt(self.lsm6ds3.acc_odr))
    
    def gyroscopeSampleRate(self):
        return self.lsm6ds3.gyro_odr_value(self.lsm6ds3.gyro_odr_txt(self.lsm6ds3.gyro_odr))
    
