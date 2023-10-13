#!/bin/bash
# Prepares the ESP32 for the addFourNumbers example
# Demo program for the course on the TinyML at the
# University of Cape Coast (Ghana)
# Copyright (c) U. Raich October 2023
# This program is released under the MIT license

echo "Setting up the file system for the addFourNumbers demo"
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

if [[ $dirs == *"/models"* ]]
then
    echo "/models directory already exists"
else
    echo "Creating /models directory"
    ampy mkdir /models
fi

echo "Uploading the tensorflow lite model: add.tflite"
ampy put models/add.tflite models/add.tflite

