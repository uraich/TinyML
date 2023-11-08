#!/bin/bash
# This shell scripts sets up the files for the person detection demo
# The person_detect_model.tflite model goes into the models folder
# the test images into the images folder
# Demo program for the course on the Internet of Things (IoT) at the
# University of Cape Coast (Ghana)
# Copyright (c) U. Raich April 2020
# This program is released under GPL

echo "Setting up the file system for the person detection demo"
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
# check if /models already exists

if [[ $dirs == *"/models"* ]]
then
    echo "/models directory already exists"
    echo "The following HTML files have been uploaded to /html:"
else
    echo "Creating /models directory"
    ampy mkdir /models
fi

echo ""
echo "Uploading the person_detect_model.tflite model file"
ampy put models/person_detect_model.tflite /models/person_detect_model.tflite

# check if /images already exists

if [[ $dirs == *"/images"* ]]
then
    echo "/images directory already exists"
    echo "The following images have been uploaded to /images:"
    images="$(ampy ls /images)"
    for i in $images ; do
	echo ${i#"/images/"}
	done    
else
    echo "Creating /images directory"
    ampy mkdir /images
    echo "Uploading person.dat and no_person.dat to /images"
    ampy put images/no_person.dat /images/no_person.dat
    ampy put images/person.dat /images/person.dat
    echo "Uloading image[0..9] to /images"
    ampy put images/image0.dat /images/image0.dat
    ampy put images/image1.dat /images/image1.dat
    ampy put images/image2.dat /images/image2.dat
    ampy put images/image3.dat /images/image3.dat
    ampy put images/image4.dat /images/image4.dat
    ampy put images/image5.dat /images/image5.dat
    ampy put images/image6.dat /images/image6.dat
    ampy put images/image7.dat /images/image7.dat
    ampy put images/image8.dat /images/image8.dat
    ampy put images/image9.dat /images/image9.dat
    
fi

