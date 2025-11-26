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
    echo "Uploading "
    ampy put samples/sample0.bin /samples/sample0.bin
    ampy put samples/sample1.bin /samples/sample1.bin
    ampy put samples/sample2.bin /samples/sample2.bin
    ampy put samples/sample3.bin /samples/sample3.bin
    ampy put samples/sample4.bin /samples/sample4.bin
    ampy put samples/sample5.bin /samples/sample5.bin
    ampy put samples/sample6.bin /samples/sample6.bin
    ampy put samples/sample7.bin /samples/sample7.bin
    ampy put samples/sample8.bin /samples/sample8.bin
    ampy put samples/sample9.bin /samples/sample9.bin
fi

if [[ $dirs == *"/models"* ]]
then
    echo "/models directory already exists"
else
    echo "Creating /models directory"
    ampy mkdir /models
    echo "Uploading the tensorflow lite model: number_model_quant.tflite"
    ampy put models/number_model_quant.tflite models/number_model_quant.tflite
fi
