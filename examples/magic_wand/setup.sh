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

echo ""
# check if /samples already exists

if [[ $dirs == *"/samples"* ]]
then
    echo "/samples directory already exists"
else
    echo "Creating /samples directory"
    ampy mkdir /samples
fi

echo "Uploading sample files"
ampy put test_data/0.bin /samples/0.bin
ampy put test_data/1.bin /samples/1.bin
ampy put test_data/2.bin /samples/2.bin
ampy put test_data/3.bin /samples/3.bin
ampy put test_data/4.bin /samples/4.bin
ampy put test_data/5.bin /samples/5.bin
ampy put test_data/6.bin /samples/6.bin
ampy put test_data/7.bin /samples/7.bin
ampy put test_data/8.bin /samples/8.bin
ampy put test_data/9.bin /samples/9.bin

if [[ $dirs == *"/models"* ]]
then
    echo "/models directory already exists"
else
    echo "Creating /models directory"
    ampy mkdir /models
fi
echo "Uploading the tensorflow lite model: number_model_quant.tflite"
ampy put model/magic_wand_model_quant.tflite models/magic_wand_model_quant.tflite
