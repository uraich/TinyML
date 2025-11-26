#!/usr/bin/env python3
# an i2c scanner
# Scans all addresses on the I2C bus and prints the addresses of connected
# modules
# copyright U. Raich 19.3.2019
# This program is released under GPL
# It was written for a workshop on IoT networks at the
# AIS conference 2019, Kampala, Uganda

from machine import *
import sys,time
import os


print("Scanning the I2C bus")
print("Program written for the workshop on IoT at the")
print("African Internet Summit 2019")
print("Copyright: U.Raich")
print("Released under the Gnu Public License")

print("Running on ESP32") 
scl = Pin(12)   # on the wemos d1 mini (esp32) scl is connected to GPIO 12
sda = Pin(13)   # on the wemos d1 mini (esp32) sda is connected to GPIO 13
i2c = I2C(1,scl=scl,sda=sda)

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
                  

