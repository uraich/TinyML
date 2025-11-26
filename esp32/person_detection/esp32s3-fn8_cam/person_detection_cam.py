# Run the person detection model
# This version reads the images from the ov2640 camera
# on the esp32s3 wroom board
# with minor changes this also works for the m5 timer camera

import sys
import microlite
import camera
import hw_esp32_s3_fn8
from machine import Pin
from neopixel import NeoPixel

n=1
intensity = 0x1f

def clearPixel():
    neoPixel[0] = (0,0,0)
    neoPixel.write()

# initialize the camera to read 96x96 pixel gray scale images

# try:
#        camera.init(0,d0=CAM_D0, d1=CAM_D1, d2=CAM_D2, d3=CAM_D3,
#                    d4=CAM_D4, d5=CAM_D5, d6=CAM_D6, d7=CAM_D7,
#                    format=camera.GRAYSCALE, framesize=camera.FRAME_96X96, 
#                    xclk_freq=camera.XCLK_20MHz,
#                    href=CAM_HREF, vsync=CAM_VSYNC, reset=CAM_RESET,
#                    pwdn=CAM_PWDN, sioc=CAM_SIOC, siod=CAM_SIOD,
#                    xclk=CAM_XCLK, pclk=CAM_PCLK)    
# except:
#	print("Error when initializing the camera")
cam_init_result = camera.init(0, d0=CAM_D0, d1=CAM_D1, d2=CAM_D2, d3=CAM_D3,
                              d4=CAM_D4, d5=CAM_D5, d6=CAM_D6, d7=CAM_D7,
                              format=camera.JPEG, framesize=camera.FRAME_VGA, 
                              xclk_freq=camera.XCLK_20MHz,
                              href=CAM_HREF, vsync=CAM_VSYNC,
                              reset=CAM_RESET, pwdn=CAM_PWDN,
                              sioc=CAM_SIOC, siod=CAM_SIOD,
                              xclk=CAM_XCLK, pclk=CAM_PCLK)

if cam_init_result:
  print("Camera successfully initialized")
else :
  print("Camera initialization failed")
  sys.exit()

# initialize the neopixel connected to GPIO 48
neopixel = NeoPixel(Pin(48),n)

# switch it off
clearPixel()

# change for m5 timer camera
# # initialize the flash-light LED, it is connected to GPIO 4
#  flash_light = Pin(2,Pin.OUT)
# switch it off
# flash_light.off()

mode = 1
test_image = bytearray(9612)

def handle_output(person):
	if person > 10:
		neopixel[0] = (0,intensity,0) # green
                neopixel.write() 
		# if m5 timer camera
        # flash_light.on()
	else:
		neopixel[0] = (intensity,0,0) # red
		# if m5 timer camera
        # flash_light.off()
        
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
person_detection_model_file = open ('models/person_detect_model.tflite', 'rb')
person_detection_model = bytearray (300568)
person_detection_model_file.readinto(person_detection_model)
person_detection_model_file.close()

# create the interpreter
interp = microlite.interpreter(person_detection_model,136*1024, input_callback, output_callback)

# Permanently read images from the camera and pass them into the model for
# inference

while True:
	test_image = camera.capture()
	interp.invoke()

camera.deinit()
