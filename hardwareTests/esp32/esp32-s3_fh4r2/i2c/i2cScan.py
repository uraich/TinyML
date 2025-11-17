#!/usr/bin/env python3
# an i2c scanner
# Scans all addresses on the I2C bus and prints the addresses of connected
# modules
# copyright U. Raich 19.3.2019
# This program is released under GPL
# It was written for a workshop on IoT networks at the
# AIS conference 2019, Kampala, Uganda

from machine import Pin,I2C
import sys,time
try:
    from hw_esp32_s3_fh4r2 import *
except:
    print("Please make sure hw_esp32_s3_fh4r2.py has been uploaded to /lib")
    sys.exit()
   
print("Scanning the I2C bus")
print("Program written for the workshop on IoT at the")
print("African Internet Summit 2019")
print("Copyright: U.Raich")
print("Released under the Gnu Public License")

print("Running on ESP32S3FH4R2") 

i2c = I2C(1,scl=Pin(SCL),sda=Pin(SDA))

addr = i2c.scan()

print("     0  1  2  3  4  5  6  7  8  9  a  b  c  d  e  f")

j=0
for i in range (0,8):
    print('%02x'%(16*i),end=': ')
    for j in range(0,16):
        if 16*i+j in addr:
            print('%02x'%(16*i+j),end=' ')
        else:
            print("--",end=' ')
    time.sleep(0.1)
    print()
                  



