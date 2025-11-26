#!/bin/bash
# Prepares the lsm6ds3 driver. It copies the files
# LSM6DS3_i2c.py, LSM6DS3_const.py, LSM6DS3_i2c.py to the /lib folder
# on the ESP32
# Demo program for the course on the TinyML at the
# University of Cape Coast (Ghana)
# Copyright (c) U. Raich October 2023
# This program is released under the MIT license

echo "Prepares the LSM6DS3 driver, uploading all the needed files"
dirs="$(ampy ls)"
echo $dirs

#check if /lib already exists

if [[ $dirs == *"/lib"* ]]
then
    echo "/lib directory already exists"
    echo "The following modules have been uploaded to /lib:"
    modules="$(ampy ls /lib)"
    for i in $modules ; do
	echo ${i#"/lib/"}
	done    
else
    echo "Creating /lib directory"
    ampy mkdir /lib
fi

echo "Uploading LSM6DS3_i2c.py"
ampy put LSM6DS3_i2c.py /lib/LSM6DS3_i2c.py
echo "Uploading LSM6DS3_const.py"
ampy put LSM6DS3_const.py /lib/LSM6DS3_const.py
echo "Uploading LSM6DS3.py"
ampy put LSM6DS3.py /lib/LSM6DS3.py
