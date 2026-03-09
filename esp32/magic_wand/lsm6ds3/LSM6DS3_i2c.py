from LSM6DS3 import LSM6DS3
from LSM6DS3_const import *
from machine import Pin,I2C
import ustruct as struct
import sys

class LSM6DS3_I2C(LSM6DS3) :
    def __init__(self,address=LSM6DS3_I2C_ADDR,bus=1,scl=12,sda=13,debug=False) :
        self.i2c_address = address
        self.debug = debug
        if self.debug:
            print("LSM6DS3_I2C debugging enabled")
        else:
            print("LSM6DS3_I2C debugging disabled")
            
        if self.debug:
            print("I2C address of LSM6DS3: 0x{:02x}".format(self.i2c_address))
        
        # Create an I2C object
        # Check if can use the hardware I2C interface, if not, create a software I2C interface
        if bus == 1:
            if self.debug:
                print("Running on I2C hardware interface with bus = ",bus, "scl = ",scl, " sda = ",sda)
            self.i2c = I2C(bus,scl=Pin(scl),sda=Pin(sda))
        else:
            if self.debug:
                print("Running on I2C bus ",bus, "scl = ",scl, " sda = ",sda)
            self.i2c = SoftI2C(scl,sda)
            
        i2c_slaves = self.i2c.scan()
        # Check if there is an LSM6DS3 on the I2C bus
        if self.i2c_address not in i2c_slaves:
            raise Exception("No LSM6DS3 found on I2C bus. Please connect the module first.")            

        # init the super class
        super().__init__()
        who_am_i = self.getDeviceID
        if self.debug :
            print("who am i: 0x{:02x}".format(who_am_i))
        
    
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

