#!/bin/bash
# Prepares the ESP32 for the hello world example generating sin values
# Demo program for the course on the TinyML at the
# University of Cape Coast (Ghana)
# Copyright (c) U. Raich October 2023
# This program is released under the MIT license

echo "Setting up the file system for the hello world demo"
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

echo "Uploading the hardwware definition file  hw_esp32_s3_fh4r2.py"
ampy put ../../hardware/esp32-s3_fh4r2/hw_esp32_s3_fh4r2.py /lib/hw_esp32_s3_fh4r2.py

echo "Uploading the hello_world.py program to /lib"
echo "This is needed to get the run.sh script to work, capturing the sine values output be the model"
ampy put hello_world.py hello_world.py

if [[ $dirs == *"/models"* ]]
then
    echo "/models directory already exists"
else
    echo "Creating /models directory"
    ampy mkdir /models
fi
echo "Uploading the tensorflow lite model: hello_world_model.tflite"
ampy put ../models/hello_world_model.tflite models/hello_world_model.tflite
