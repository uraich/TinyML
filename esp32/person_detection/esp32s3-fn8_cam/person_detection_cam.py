# Run the person detection model
# This version reads the images from the ov2640 camera on the
# esp32s3-fn8_cam board
# Copyright (c) U. Raich Dec 2025
# This program is part of the TinyML course at the
# University of Cape Coast, Ghana
# It is released under the MIT license

import sys
import microlite
import camera
from machine import Pin
from neopixel import NeoPixel


def clearPixel():
    neopixel[0] = (0,0,0)
    
try:
    from hw_esp32_s3_fn8 import *
except:
    print("Please make sure hw_esp32_s3_fn8.py has been uploaded to /lib")
    sys.exit()

# Make sure the camera is not already initialized, which may give problems
camera.deinit()
print("We are running on the esp32s3-fn8_cam board")
# initialize the camera to read 96x96 pixel gray scale images

cam_init_result = camera.init(0, d0=CAM_D0, d1=CAM_D1, d2=CAM_D2, d3=CAM_D3,
                              d4=CAM_D4, d5=CAM_D5, d6=CAM_D6, d7=CAM_D7,
                              format=camera.JPEG, framesize=camera.FRAME_VGA, 
                              xclk_freq=camera.XCLK_20MHz,
                              href=CAM_HREF, vsync=CAM_VSYNC, reset=-1, pwdn=-1,
                              sioc=CAM_SIOC, siod=CAM_SIOD, xclk=CAM_XCLK, pclk=CAM_PCLK)
  
if (cam_init_result):
  print("Camera successfully initialized")
else:
  print("Initialization of camera failed")
  sys.exit(-1)

# initialize ws2812 LED
pin = Pin(NEOPIXEL)                      # define the pin onto which the neopixel is connected
neopixel = NeoPixel(pin,NO_OF_NEOPIXELS) # there is a single neopixel on the esp32s3-fn8_cam
# switch it off
clearPixel()

test_image = bytearray(9612)

def handle_output(person):
    if person > 10:
        # set the neopixel to green
        neopixel[0] = (0,INTENSITY,0)
        neopixel.write()
    else:
        # set the neopixel to red
        neopixel[0] = (INTENSITY,0,0)
        neopixel.write()
        
def input_callback (microlite_interpreter):    
	inputTensor = microlite_interpreter.getInputTensor(0)
	for i in range (0, len(test_image)):
		inputTensor.setValue(i, test_image[i])
	print ("setup %d bytes on the inputTensor." % (len(test_image)))

def output_callback (microlite_interpreter):
	outputTensor = microlite_interpreter.getOutputTensor(0)
	not_a_person = outputTensor.getValue(0)
	person = outputTensor.getValue(1)
	print ("'not a person' = %d, 'person' = %d" % (not_a_person, person))
	handle_output(person)

# read the model
print("Reading the mode from the models directory on the esp32s3-fn8_cam")
person_detection_model_file = open ('models/person_detect_model.tflite', 'rb')
person_detection_model = bytearray (300568)
person_detection_model_file.readinto(person_detection_model)
person_detection_model_file.close()

# create the interpreter
print("Creating the interpreter")
interp = microlite.interpreter(person_detection_model,136*1024, input_callback, output_callback)

# Permanently read images from the camera and pass them into the model for
# inference

while True:
    try:
	test_image = camera.capture()
	interp.invoke()
    except KeyboardInterrupt:
        break
camera.deinit()
sys.exit(0)
