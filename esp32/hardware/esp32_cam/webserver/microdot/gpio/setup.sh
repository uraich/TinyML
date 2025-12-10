#!/bin/bash
# This shell scripts sets up the picoweb server to run the Hello World
# WEB server. It uses picoweb to provide the Hello World WEB page.
# Demo program for the course on the Internet of Things (IoT) at the
# University of Cape Coast (Ghana)
# Copyright (c) U. Raich April 2020
# This program is released under GPL

echo "Setting up the file system for the WEB server"
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
echo "Uploading hw_esp32_cam.py to /lib"
rshell -p /dev/ttyUSB0 --quiet cp ../../../hw_esp32_cam.py /pyboard/lib/hw_esp32_cam.py

echo ""
# check if /html already exists

if [[ $dirs == *"html/"* ]]
then
    echo "/html directory already exists"
    echo "The following HTML files have been uploaded to /html:"
    htmlFiles="$(rshell -p /dev/ttyUSB0 --quiet ls /pyboard/html)"
    for i in $htmlFiles ; do
	echo ${i#"/html/"}
	done
else
    echo "Creating /html directory"
    rshell -p /dev/ttyUSB0 --quiet mkdir /pyboard/html
fi
echo ""
echo "Uploading gpio.html"
rshell -p /dev/ttyUSB0 --quiet cp html/gpio.html /pyboard/html/gpio.html
