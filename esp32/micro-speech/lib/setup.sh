#!/bin/bash
# This shell scripts sets up the picoweb server to run the Hello World
# WEB server. It uses picoweb to provide the Hello World WEB page.
# Demo program for the course on the Internet of Things (IoT) at the
# University of Cape Coast (Ghana)
# Copyright (c) U. Raich April 2020
# This program is released under GPL

echo "Setting up the file system for the micro-speech tflite-micro example"
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
echo "Uploading micro_speech.py to /lib"
ampy put ../esp32/micro_speech.py /lib/micro_speech.py

echo ""
# check if /audio already exists
if [[ $dirs == *"/audio"* ]]
then
    echo "/audio directory already exists"
    echo "The following audio files have been uploaded to /audio:"
    audioFiles="$(ampy ls /audio)";
    for i in $audioFiles ; do
	echo ${i#"/audio/"}
	done
else
    echo "Creating /audio directory"
    ampy mkdir /audio
fi

echo ""
echo "Uploading yes_1000ms.wav, no_1000ms.wav, noise_1000ms.wav, silence_1000ms.wav"
ampy put wav_files/yes_1000ms.wav audio/yes_1000ms.wav
ampy put wav_files/no_1000ms.wav audio/no_1000ms.wav
ampy put wav_files/noise_1000ms.wav audio/noise_1000ms.wav
ampy put wav_files/silence_1000ms.wav audio/silence_1000ms.wav

# check if /models already exists
if [[ $dirs == *"/models"* ]]
then
    echo "/models directory already exists"
    echo "The following model files have been uploaded to /models:"
    modelFiles="$(ampy ls /models)";
    for i in $modelFiles ; do
	echo ${i#"/models/"}
	done
else
    echo "Creating /models directory"
    ampy mkdir /models
fi

echo ""
echo "Uploading micro-speech-model.tflite"
ampy put model.tflite models/micro-speech-model.tflite

