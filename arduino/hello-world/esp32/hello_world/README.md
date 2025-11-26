# Hello World Example

This example is designed to demonstrate the absolute basics of using [TensorFlow
Lite for Microcontrollers](https://www.tensorflow.org/lite/microcontrollers).
It includes the full end-to-end workflow of training a model, converting it for
use with TensorFlow Lite for Microcontrollers for running inference on a
microcontroller.

The model is trained to replicate a `sine` function and generates a pattern of
data to either blink LEDs or control an animation, depending on the capabilities
of the device.

## Modifications to the original code
The original code calculates some 20 sine points using the trained hello world model. The model is integrated into the source code as a C include file (model.h) and a constant C array (model.cpp). The code is generated from the Tensorflow Lite Micro model (just an array of byte values) using the xdd program. You may have to install this program on your computer.
The new version extends the calculations to 1000 values and it uses the WS2812 LED on the ESP32-S3 board as a visual indicator. The sin(x) values from the model are mapped onto a (0..maxIntensity) light intensity range, which is fed to the LED.

## Analysing the results
The results are output to the Arduino serial port and they can be captured with a program like minicom or tio: 
```
minicom -t | tee output.txt
```
After resetting the ESP32 the output will be captured on the file output.txt
The _analyse_output.ipynb_ jupyter notebook or the _analyse_output.py_ program will plot the data, as well as a regular sine function for comparison.
![hello_world.png](output_data/images/hello_world.png "The hello world analysis screen dump")


