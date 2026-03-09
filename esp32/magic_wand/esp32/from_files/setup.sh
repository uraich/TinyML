#!/bin/bash
# Prepares the ESP32 for the MNIST number recognition example
# Demo program for the course on the TinyML at the
# University of Cape Coast (Ghana)
# Copyright (c) U. Raich October 2023
# This program is released under the MIT license

echo "Setting up the file system for the magic_wand demo"
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
echo "Uploading hardware decription file hw_esp32_s3_fh4r2.py"
ampy put ../../../hardware/esp32-s3_fh4r2/hw_esp32_s3_fh4r2.py /lib/hw_esp32_s3_fh4r2.py
echo "Uploading LSM6DS3_i2c.py"
ampy put ../lsm6ds3/LSM6DS3_i2c.py /lib/LSM6DS3_i2c.py
echo "Uploading LSM6DS3_const.py"
ampy put ../lsm6ds3/LSM6DS3_const.py /lib/LSM6DS3_const.py
echo "Uploading LSM6DS3.py"
ampy put ../lsm6ds3/LSM6DS3.py /lib/LSM6DS3.py
echo "Uploading lsm6ds3_imu.py"
ampy put ../lsm6ds3_imu.py /lib/lsm6ds3_imu.py

echo ""
# check if /data already exists

if [[ $dirs == *"/data"* ]]
then
    echo "/data directory already exists"
else
    echo "Creating /data directory"
    ampy mkdir /data
fi
# check if /samples already exists

if [[ $dirs == *"/samples"* ]]
then
    echo "/samples directory already exists"
else
    echo "Creating /samples directory"
    ampy mkdir /samples
fi
echo "Uploading sample files"
ampy put ../../test_data/0.bin /samples/0.bin
ampy put ../../test_data/1.bin /samples/1.bin
ampy put ../../test_data/2.bin /samples/2.bin
ampy put ../../test_data/3.bin /samples/3.bin
ampy put ../../test_data/4.bin /samples/4.bin
ampy put ../../test_data/5.bin /samples/5.bin
ampy put ../../test_data/6.bin /samples/6.bin
ampy put ../../test_data/7.bin /samples/7.bin
ampy put ../../test_data/8.bin /samples/8.bin
ampy put ../../test_data/9.bin /samples/9.bin

# check if /samples already exists

if [[ $dirs == *"/strokes"* ]]
then
    echo "/strokes directory already exists"
else
    echo "Creating /strokes directory"
    ampy mkdir /strokes
fi
echo "Uploading stroke file"
ampy put strokes/digits.json /strokes/digits.json
