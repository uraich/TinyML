#!/bin/bash
# Prepares the ESP32 for the person detection example
# Demo program for the course on the TinyML at the
# University of Cape Coast (Ghana)
# Copyright (c) U. Raich October 2023
# This program is released under the MIT license

echo "Setting up the file system for the person detection  demo"
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
# check if /images already exists

if [[ $dirs == *"/images"* ]]
then
    echo "/images directory already exists"
else
    echo "Creating /images directory"
    ampy mkdir /images
    echo "Uploading image files"
    ampy put images/person_image_data.dat /images/person_image_data.dat
    ampy put images/no_person_image_data.dat /images/no_person_image_data.dat
fi

if [[ $dirs == *"/models"* ]]
then
    echo "/models directory already exists"
else
    echo "Creating /models directory"
    ampy mkdir /models
fi
echo ""    
echo "Uploading the tensorflow lite model: person_detect_model.tflite"
ampy put models/person_detect_model.tflite models/person_detect_model.tflite
