#!/bin/bash
# This shell scripts sets up the picoweb server to run the Hello World
# WEB server. It uses picoweb to provide the Hello World WEB page.
# Demo program for the course on the Internet of Things (IoT) at the
# University of Cape Coast (Ghana)
# Copyright (c) U. Raich April 2020
# This program is released under GPL

echo "Setting up the hardware file for the esp32-cam"
dirs="$(rshell -p /dev/ttyUSB0 --quiet ls /pyboard)"
echo $dirs

#check if /lib already exists

if [[ $dirs == *"lib/"* ]]
then
    echo "/lib directory already exists"
    echo "The following modules have been uploaded to /lib:"
    modules="$(rshell -p /dev/ttyUSB0 --quiet ls /pyboard/lib)"
    for i in $modules ; do
	echo ${i#"/lib/"}
	done    
else
    echo "Creating /lib directory"
    rshell -p /dev/ttyUSB0 --quiet mkdir /pyboard/lib
fi

echo ""
echo "Uploading hw_esp32_cam.py"
rshell -p /dev/ttyUSB0 --quiet cp hw_esp32_cam.py /pyboard/lib/hw_esp32_cam.py
