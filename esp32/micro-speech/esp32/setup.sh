#!/bin/bash
# Prepares the ESP32 for the micro-speech example
# Demo program for the course on the TinyML at the
# University of Cape Coast (Ghana)
# Copyright (c) U. Raich December 2025
# This program is released under the MIT license

echo "Setting up the file system for the micro-speech demo"
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

echo "Upload the hardware description file"
ampy put ../../hardware/esp32s3-fn8_cam/hw_esp32_s3_fn8.py /lib/hw_esp32_s3_fn8.py
echo "Upload micro_speech.py"
ampy put micro_speech.py /lib/micro_speech.py

echo ""
# check if /audio already exists

if [[ $dirs == *"/audio"* ]]
then
    echo "/audio directory already exists"
    echo "The following modules have been uploaded to /audio:"
    modules="$(ampy ls /audio)"
    for i in $modules ; do
	echo ${i#"/audio/"}
	done    
else
    echo "Creating /audio directory"
    ampy mkdir /audio
fi

echo "Uploading sound files"
echo "no_1000ms.wav"
ampy put ../wav_files/no_1000ms.wav /audio/no_1000ms.wav
echo "yes_1000ms.wav"
ampy put ../wav_files/yes_1000ms.wav /audio/yes_1000ms.wav
echo "noise_1000ms.wav"
ampy put ../wav_files/noise_1000ms.wav /audio/noise_1000ms.wav
echo "silence_1000ms.wav"
ampy put ../wav_files/silence_1000ms.wav /audio/silence_1000ms.wav

if [[ $dirs == *"/models"* ]]
then
    echo "/models directory already exists"
else
    echo "Creating /models directory"
    ampy mkdir /models
fi
echo ""    
echo "Uploading the tensorflow lite model: micro-speech_model.tflite"
ampy put models/micro_speech_model.tflite models/micro_speech_model.tflite
