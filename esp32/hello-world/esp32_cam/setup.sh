#!/bin/bash
# This shell scripts sets up the files for the hello world demo
# Demo program for the course on the Internet of Things (IoT) at the
# University of Cape Coast (Ghana)
# Copyright (c) U. Raich April 2020
# This program is released under GPL

echo "Setting port to /dev/ttyUSB0"
export AMPY_PORT=/dev/ttyUSB0

echo "Setting up the hardware file for the esp32_cam"
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

echo ""
echo "Uploading hw_esp32_s3_fn8.py"
ampy put ../../hardware/esp32_cam/hw_esp32_cam.py /lib/hw_esp32_cam.py

if [[ $dirs == *"/models"* ]]
then
    echo "/models directory already exists"
else
    echo "Creating /models directory"
    ampy mkdir /models
fi
echo "Uploading the tensorflow lite model: hello_world_model.tflite"
ampy put ../models/hello_world_model.tflite models/hello_world_model.tflite
