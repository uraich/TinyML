# lsm6ds3_imu.py: replacement of the LSM9DS1 arduino class using the LSM6DS3
# since there is no magnetometer and it is not used by the magic wand
# these functions are removed.
# Copyright (c) U. Raich Dec 2025
# This program is part of the TinyML course at the
# University of Cape Coast, Ghana
# It is released under the MIT license

from machine import Pin,I2C
from time import sleep_ms
import sys
from micropython import const

LSM6DS3_I2C_ADDR               = const(0x6b)
LSM6DS3_WHO_AM_I               = const(0x0f)
LSM6DS3_WHO_AM_I_CODE          = const(0x69)
LSM6DS3_CTRL1_XL               = const(0x10) 
LSM6DS3_CTRL2_G                = const(0x11)
LSM6DS3_CTRL3_C                = const(0x12)
LSM6DS3_BDU                    = const(0x40)
LSM6DS3_FIFO_STATUS1           = const(0x3a)
LSM6DS3_FIFO_STATUS2           = const(0x3b)
LSM6DS3_FIFO_STATUS3           = const(0x3c)
LSM6DS3_FIFO_STATUS4           = const(0x3d)
LSM6DS3_FIFO_CTRL1             = const(0x06)
LSM6DS3_FIFO_CTRL2             = const(0x07)
LSM6DS3_FIFO_CTRL3             = const(0x08)
LSM6DS3_FIFO_CTRL4             = const(0x09)
LSM6DS3_FIFO_CTRL5             = const(0x0a)
LSM6DS3_FIFO_DATA_OUT_L        = const(0x3e)

LSM6DS3_SW_RESET               = const(1)
LSM6DS3_FIFO_EMPTY             = const(0x10)
LSM6DS3_FIFO_FULL              = const(0x20)
LSM6DS3_FIFO_OVERRUN           = const(0x40)

class LSM6DS3_IMU(object):
    decimation = {1 : 1,
                  2 : 2,
                  3 : 3,
                  4 : 4,
                  5 : 8,
                  6 : 16,
                  7 : 32}
    
    odr = {1 : 12.5,
           2 : 26,
           3 : 52,
           4 : 104,
           5 : 208,
           6 : 416,
           7 : 833,
           8 : 1660,
           9 : 3330,
           10 : 6669}

    bandwidth = {0 : 400,
                 1 : 200,
                 2 : 100,
                 3 : 50}
    
    acc_fullScale = {0 : 2,
                     1 : 16,
                     2 : 4,
                     3 : 8}
    
    gyro_fullScale = {0 : 250,
                      1 : 500,
                      2 : 1000,
                      3 : 2000}

    def __init__(self,address=LSM6DS3_I2C_ADDR,bus=1,scl=12,sda=13,debug=False):
        self.debug = debug
        self.i2c_address = address
        if self.debug:
            print("LSM6DS3_IMU debugging enabled")
        else:
            print("LSM6DS3_IMU debugging disabled")
            
        if self.debug:
            print("I2C address of LSM6DS3: 0x{:02x}".format(self.i2c_address))

        # Create an I2C object
        # Check if can use the hardware I2C interface, if not, create a software I2C interface
        if bus == 1:
            if self.debug:
                print("Running on I2C hardware interface with bus = ",bus,
                      "scl = ",scl, " sda = ",sda)
            self.i2c = I2C(bus,scl=Pin(scl),sda=Pin(sda))
        else:
            if self.debug:
                print("Running on I2C bus ",bus, "scl = ",scl, " sda = ",sda)
            self.i2c = SoftI2C(scl,sda)

        i2c_slaves = self.i2c.scan()
        # Check if there is an LSM6DS3 on the I2C bus
        if self.i2c_address not in i2c_slaves:
            raise Exception("No LSM6DS3 found on I2C bus. Please connect the module first")

        who_am_i = self.getDeviceID()
        if self.debug:
            print("who am i: 0x{:02x}".format(who_am_i))

        # reset the device
        self.reset()
        # set the BDU bit (block data update until hi and low byte are both read
        self.setBDU()
        
        # set acc odr to 104 HZ
        # set full scale to 4 g
        # set band width to 50 Hz
        
        self.writeByte(LSM6DS3_CTRL1_XL,0x4b)
        if self.debug:
            tmp = self.readByte(LSM6DS3_CTRL1_XL)
            if tmp == 0x4b:
                print("LSM6DS3_CTRL1_XL was correctly set")
            else:
                print("Read 0x{:02x} instead 0x 0x4b from LSM6DS3_CTRL1:XL".format(tmp))
        self.accFullScale = 4
        self.gyroFullScale = 2000
        
        # set gyro odr to 104 HZ
        # set full scale to 2000 dps
        self.writeByte(LSM6DS3_CTRL2_G,0x4c)        
            
    def readByte(self,register):
        try:
            tmp = bytearray(self.i2c.readfrom_mem(self.i2c_address,register,1))
        except:
            print("Cannot read a byte from register 0x{:02x}".format(register))
        return tmp[0]
    
    def readBytes(self,register,no_of_bytes) :
        try:
            tmp = bytearray(self.i2c.readfrom_mem(self.i2c_address,register,no_of_bytes))
        except:
            print("Cannot read {:d} bytes from register 0x{:02x}".format(no_of_bytes,register))
            return
        if self.debug :
            print("Read {:d} bytes from 0x{:02x}".format(no_of_bytes,register))
            print("Returned {:d} bytes: ".format(len(tmp)),end="")
            for i in range(len(tmp)) :
                print("0x{:02x} ".format(tmp[i]),end="")
            print("")
            
        return tmp

    def writeByte(self,register,value):
        tmp = bytearray(1)
        tmp[0]=value
        if self.debug :            
            print("Write {:02x} to register 0x{:02x}".format(value,register))
        try:
            self.i2c.writeto_mem(self.i2c_address,register,tmp)
        except:
            print("Cannot write {:02x} to register 0x{:02x}".format(value,register))
            
    def writeBytes(self,register,values) :
        if self.debug :            
            print("Write {:d} bytes to 0x{:02x}".format(len(values),register))
            for i in range(len(values)) :
                print("0x{:02x} ".format(values[i]),end="")
            print("")
        try:
            self.i2c.writeto_mem(self.i2c_address,register,values)
        except:
            print("Cannot write {:d} bytes to register 0x{:02x}".format(len(values),register))            
    def getDeviceID(self):
        return self.readByte(LSM6DS3_WHO_AM_I)

    def setDebug(self,onOff):
        self.debug = onOff
    
    def reset(self):
        tmp = self.readByte(LSM6DS3_CTRL3_C)
        tmp |= LSM6DS3_SW_RESET
        self.writeByte(LSM6DS3_CTRL3_C,tmp)
        # wait until the reset bit flips back to 0
        tmp = self.readByte(LSM6DS3_CTRL3_C)
        while tmp & LSM6DS3_SW_RESET :
            tmp = self.readByte(LSM6DS3_CTRL3_C)
            if self.debug:
                print("Waiting for reset to complete")

    def setBDU(self):
        tmp = self.readByte(LSM6DS3_CTRL3_C)
        tmp |= LSM6DS3_BDU
        self.writeByte(LSM6DS3_CTRL3_C,tmp)

        
    def accelerationFullScale(self):
        tmp = self.readByte(LSM6DS3_CTRL1_XL)
        if self.debug:
            print("CTRL1_XL register value: 0x{:02x}".format(tmp))

        fs = (tmp & 0xc) >> 2
        if self.debug:
            print("Accelerometer Full Scale code: {:d}".format(fs))
        return self.acc_fullScale[fs]
    
    def accelerationBandwidth(self):
        tmp = self.readByte(LSM6DS3_CTRL1_XL)
        if self.debug:
            print("CTRL1_XL register value: 0x{:02x}".format(tmp))
        bw_code = tmp & 0x3
        if self.debug:
            print("Accelerometer Bandwidth code: {:d}".format(bw_code))        
        return self.bandwidth[bw_code]

    def accelerationSampleRate(self):
        tmp = self.readByte(LSM6DS3_CTRL1_XL)
        if self.debug:
            print("CTRL1_XL register value: 0x{:02x}".format(tmp))
        odr_code = tmp >> 4
        if self.debug:
            print("Accelerometer ODR code: {:d}".format(odr_code))        
        return self.odr[odr_code]        

    def gyroscopeFullScale(self):
        tmp = self.readByte(LSM6DS3_CTRL2_G)
        if self.debug:
            print("CTRL2_G register value: 0x{:02x}".format(tmp))

        fs_code = (tmp & 0xc) >> 2
        if self.debug:
            print("Gyroscope Full Scale code: {:d}".format(fs_code))
        return self.gyro_fullScale[fs_code]
    
    def gyroscopeSampleRate(self):
        tmp = self.readByte(LSM6DS3_CTRL2_G)
        if self.debug:
            print("CTRL2_G register value: 0x{:02x}".format(tmp))
        odr_code = tmp >> 4
        if self.debug:
            print("Gyroscope ODR code: {:d}".format(odr_code))        
        return self.odr[odr_code]        

    def setContinuousMode(self):
        # set fifo watermark to 0x200
        tmp = bytearray(2)
        tmp[0] = 0
        tmp[1] = 0x02
        self.writeBytes(LSM6DS3_FIFO_CTRL1,tmp)
        # set the decimation to 1g
        self.writeByte(LSM6DS3_FIFO_CTRL3,0x9)
        # set fifo odr to 104 Hz and fifo mode to continuous
        self.writeByte(LSM6DS3_FIFO_CTRL5,0x26)
        # The first few samples are strange. Therefore we skip them
        self.skipFirst()
        
    def fifoWatermark(self):
        tmp = self.readBytes(LSM6DS3_FIFO_CTRL1,2)
        return ((tmp[1] & 0x0f )<< 8) | tmp[0] 

    def accelerationDecimationFactor(self):
        tmp = self.readByte(LSM6DS3_FIFO_CTRL3)
        return self.decimation[tmp & 0x7]
    
    def gyroscopeDecimationFactor(self):
        tmp = self.readByte(LSM6DS3_FIFO_CTRL3)
        if self.debug:
            print("Gyro decimation code: {:02x}".format((tmp >> 3) & 7))
        return self.decimation[(tmp >> 3) & 0x7]

    def fifoSampleRate(self):
        tmp =  self.readByte(LSM6DS3_FIFO_CTRL5)
        return self.odr[tmp >> 3]

    def fifoMode(self):
        tmp = self.readByte(LSM6DS3_FIFO_CTRL5) & 0x7
        if self.debug:
            if tmp == 0x6:
                print("FIFO is in continuous mode")
        return tmp
    
    def fifoStatus(self):
        return self.readByte(LSM6DS3_FIFO_STATUS2)
    
    def fifoCtrl_5(self):
        return self.readByte(LSM6DS3_FIFO_CTRL5)
    
    def fifoEmpty(self):
        return self.readByte(LSM6DS3_FIFO_STATUS2) & LSM6DS3_FIFO_EMPTY

    def accelerationAndGyroscopeAvailable(self):
        fifo_status = self.readByte(LSM6DS3_FIFO_STATUS2)
        if self.debug:
            print("fifo_status2 register: 0x:{:02x}".format(fifo_status))
            if fifo_status & LSM6DS3_FIFO_EMPTY:
                print("FIFO empty")
            else:
                print("Data available")
        if fifo_status & LSM6DS3_FIFO_FULL:
            raise Exception("Fifo is full: status2 reg: 0x{:02x}".format(fifo_status))
        return not fifo_status & LSM6DS3_FIFO_EMPTY
        
    def noOfSamplesInFifo(self):
        tmp = bytearray(2)
        tmp = self.readBytes(LSM6DS3_FIFO_STATUS1,2)
        return(tmp[1] & 0xf) << 8 | tmp[0]
    
    def skipFirst(self):
        i = 0
        while i < 10:
            while not self.accelerationAndGyroscopeAvailable():
                continue
            tmp = self.readBytes(LSM6DS3_FIFO_DATA_OUT_L,12) # 6 bytes gyroscope + 6 bytes accelerometer
            i +=1
            
    def readAccelerationAndGyroscope(self):
        tmp = bytearray(12)
        value = bytearray(2)
        gyro_result = []
        acc_result = []
        tmp = self.readBytes(LSM6DS3_FIFO_DATA_OUT_L,12) # 6 bytes gyroscope + 6 bytes accelerometer
        for i in range(3):
            value[0] = tmp[2*i]
            value[1] = tmp[2*i+1]
            gyro_result.append(self.bytesToShort(value)*self.gyroFullScale/32768.0)
        for i in range(3):
            value[0] = tmp[2*i+6]
            value[1] = tmp[2*i+7]
            acc_result.append(self.bytesToShort(value)*self.accFullScale/32768.0)
        
        return (tuple(gyro_result),tuple(acc_result))

    def resetFifo(self):
        tmp = self.readByte(LSM6DS3_FIFO_CTRL5)
        # set the fifo to bypass mode
        # this will clear the fifo
        tmp &= 0xf8
        self.writeByte(LSM6DS3_FIFO_CTRL5,tmp)
        sleep_ms(1)
        # set the fifo back to continuous mode
        self.setContinuousMode()
        # tmp |= 0x4
        # self.writeByte(LSM6DS3_FIFO_CTRL5,tmp)
    
    def bytesToShort(self,bytes):

        # The lsm6Ds3 returns 16 bit signed values in 2 bytes.
        # The bytes are joined and the resulting value
        # converted to a Python integer

        val = (bytes[1] << 8 ) | bytes[0]
        # if self.debug:
        #     print("value: 0x{:04x}".format(val))
        if not val & 0x8000:           # positive 16 bit value
            # if self.debug:
            #     print ("positive value: {:d}".format(val))
            return val
        else:
            val = -((val ^ 0xffff) + 1)
            # if self.debug:
            #     print("negative value: {:d} ".format(val)) 
            return val
        
    def printRegisterSettings(self):
        print("------------------------------------------------------------------")
        print("Verifying all IMU calls made by magic_wand.ino on the lsm6ds3")
        print("------------------------------------------------------------------")
        
        print("Acceleration data rate:     ",self.accelerationSampleRate()," Hz")
        print("Acceleration full scale:    +-",self.accelerationFullScale()," g")
        print("Gyroscope data rate:        ",self.gyroscopeSampleRate()," Hz")
        print("Gyroscope full scale:       ",self.gyroscopeFullScale(),"dps")
        # print("FIFO water mark:             0x{:03x}".format(self.fifoWatermark()))
        # print("FIFO odr:                   ",self.fifoSampleRate()," Hz")
        # print("Acceleration decimation factor: ",self.accelerationDecimationFactor())
        # print("Gyroscope decimation factor:    ",self.gyroscopeDecimationFactor())
        # print("FIFO CTRL5:                   0x{:02x}".format(self.fifoCtrl_5()))

    def printFifoRegisterSettings(self):
        print("------------------------------------------------------------------")
        print("Verifying all FIFO control and status registers")
        print("------------------------------------------------------------------")

        ctrl1 = self.readByte(LSM6DS3_FIFO_CTRL1)
        ctrl2 = self.readByte(LSM6DS3_FIFO_CTRL2) 
        print("FIFO CTRL1 and 2: 0x{:02x}, 0x{:02x}".format(ctrl1,ctrl2))
        print("FIFO water mark: 0x{:03x}".format(self.fifoWatermark()))
        ctrl3 = self.readByte(LSM6DS3_FIFO_CTRL3)
        print("FIFO CTRL3: 0x{:02x}".format(ctrl3))
        print("Acceleration decimation factor: ",self.accelerationDecimationFactor())
        print("Gyroscope decimation factor:    ",self.gyroscopeDecimationFactor())
        ctrl4 = self.readByte(LSM6DS3_FIFO_CTRL4)
        print("FIFO CTRL4: 0x{:02x}".format(ctrl4))
        ctrl5 = self.readByte(LSM6DS3_FIFO_CTRL4)
        print("FIFO CTRL5: 0x{:02x}".format(ctrl5))
        status1 = self.readByte(LSM6DS3_FIFO_STATUS1)
        status2 = self.readByte(LSM6DS3_FIFO_STATUS2)
        print("FIFO STATUS1 and 2: 0x{:02x}, 0x{:02x}".format(status1,status2))
        print("No of words in FIFO: {:d}".format(((status2 & 0xf) << 8) | status1))
        status3 = self.readByte(LSM6DS3_FIFO_STATUS3)
        status4 = self.readByte(LSM6DS3_FIFO_STATUS4)
        print("FIFO pattern: 0x{:02x}".format((status4 << 8) | status3))
        
