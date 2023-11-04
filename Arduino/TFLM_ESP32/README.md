# TFLM_ESP32

https://www.tensorflow.org/lite/microcontrollers/overview

https://github.com/espressif/tflite-micro-esp-examples

## Overview

This library runs TensorFlow machine learning models on microcontrollers, allowing you to build AI/ML applications powered by deep learning and neural networks. 

With the included examples, you can recognize speech, detect people using a camera, and recognise "magic wand" gestures using an accelerometer.

The examples work best with the M5StickC(ESP32) board, which has a microphone and accelerometer.

## Examples

### hello_world

Outputs sine waves to serial outputs and build-in LEDs.

### micro_speech

This is a sample of speech recognition.
The audio_provider and command_responder must be modified according to the environment in which they are used.

### person_detection

It is a person detection using a camera.
The image_provider and detection_responder must be modified according to the environment in which they are used.


### magic_wand

This is gesture recognition using acceleration.
The accelerometer_handler and output_handler must be modified according to the environment in which they are used.

