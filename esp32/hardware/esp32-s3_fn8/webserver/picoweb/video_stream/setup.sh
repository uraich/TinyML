#!/bin/bash
# This shell scripts sets up the picoweb server to run the Hello World
# WEB server. It uses picoweb to provide the Hello World WEB page.
# Demo program for the course on the Internet of Things (IoT) at the
# University of Cape Coast (Ghana)
# Copyright (c) U. Raich April 2020
# This program is released under GPL

echo "Setting up the file system for the WEB server"
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
    echo "The following image files have been uploaded to /images:"
    htmlFiles="$(ampy ls /images)";
    for i in $htmlFiles ; do
	echo ${i#"/images/"}
	done
else
    echo "Creating /images directory"
    ampy mkdir /images
fi
echo ""
echo "Uploading 1.jpg"
ampy put images/1.jpg /images/1.jpg
echo "Uploading 2.jpg"
ampy put images/2.jpg /images/2.jpg
echo "Uploading 3.jpg"
ampy put images/3.jpg /images/3.jpg
echo "Uploading 1.bmp"
ampy put images/1.bmp /images/1.bmp
echo "Uploading 2.bmp"
ampy put images/2.bmp /images/2.bmp
echo "Uploading 3.jpg"
ampy put images/3.bmp /images/3.bmp
