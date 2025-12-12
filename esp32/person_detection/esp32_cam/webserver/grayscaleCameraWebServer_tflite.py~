# grayscale_camera_tflite.py: Takes a grayscale 96x96 picture from the camera
# and transforms it into a bmp file. The bmp file can be observed with a
# web browser
# The raw image data is passed to the trained person detection neural network
# to find out, if a person is in sight. If this is the case, then the neopixel
# turns green, otherwise it is red.
# Copyright (c) U. Raich Dec. 2025
# This program is part of the TinyML course
# at the University of Cape Coast, Ghana
# It is released under the MIT license

import sys
import asyncio
from microdot import Microdot
from wifi_connect import connect, getIPAddress
import camera
import struct
import microlite
from machine import Pin
from neopixel import NeoPixel

def clearPixel():
    neopixel[0] = (0,0,0)
 
# connect to WiFi
connect()
app = Microdot()

try:
    from hw_esp32_s3_fn8 import *
except:
    print("Please make sure hw_esp32_s3_fn8.py has been uploaded to /lib")
    sys.exit()

# connect to WiFi
connect()

print("Init camera")
# Disable camera initialization
camera.deinit()

# Enable camera initialization
print("We are on the ESP32-S3-FN8")

cam_init_result = camera.init(0, d0=CAM_D0, d1=CAM_D1, d2=CAM_D2, d3=CAM_D3,
                              d4=CAM_D4, d5=CAM_D5, d6=CAM_D6, d7=CAM_D7,
                              format=camera.GRAYSCALE,
                              framesize=camera.FRAME_96X96, 
                              xclk_freq=camera.XCLK_20MHz,
                              href=CAM_HREF, vsync=CAM_VSYNC,
                              reset=CAM_RESET, pwdn=CAM_PWDN,
                              sioc=CAM_SIOC, siod=CAM_SIOD,
                              xclk=CAM_XCLK, pclk=CAM_PCLK)

if cam_init_result:
  print("Camera was successfully initialized")
else:
  print("Camera initialization failed");
  sys.exit(-1)

# flip the image as bmps work bottom up
camera.set_vflip(True)

# initialize ws2812 LED
pin = Pin(NEOPIXEL)                      # define the pin onto which
                                         # the neopixel is connected
neopixel = NeoPixel(pin,NO_OF_NEOPIXELS) # there is a single neopixel
                                         # on the esp32s3-fn8_cam
# switch it off
clearPixel()

# Create the headers and palette needed to transform the grayscale video
# image info a bmp file
# start with the info header
BI_RGB = 0
infoHeader = bytearray(40)
infoHdrSize = len(infoHeader)
imageWidth = 96
imageHeight = 96
noOfPlanes = 1
noOfBitsPerPixel = 8
compression = BI_RGB                    # no compression
imageSize = 0                           # this works for uncompressed images
imageSize = imageWidth * imageHeight * 2
hor_resolution = 0                      # no preference
ver_resolution = 0                      # no preference
noOfColors = 256                        # only used with color maps
importantColors = 0
infoHdr = struct.pack("3i2h6i",infoHdrSize,imageWidth,imageHeight,noOfPlanes,
                      noOfBitsPerPixel,compression,imageSize,
                      hor_resolution,ver_resolution,
                      noOfColors,importantColors)

# Now the color palette
palette = bytearray(256*4)
for i in range(256):
    palette[4*i]   = i
    palette[4*i+1] = i
    palette[4*i+2] = i
    palette[4*i+3] = 0xff

# ...and finally the file header
fileHdrSize = 14
magic = 'BM'.encode('ascii')
fileSize = fileHdrSize + len(infoHdr) + len(palette) + 96*96
reserved = 0
offset = fileHdrSize + len(infoHdr) + len(palette)
hdr = magic + struct.pack('ihhi',fileSize,reserved,reserved,offset)

print("Starting the WEB server")

@app.route('/')
async def index(request):
    return '''<!doctype html>
<html>
  <head>
    <title>Person Detection Video Streaming</title>
    <meta charset="UTF-8">
  </head>
  <body>
    <h1>Person Detection Video Streaming</h1>
    <img src="/video_feed">
  </body>
</html>''', 200, {'Content-Type': 'text/html'}


@app.route('/video_feed')
async def video_feed(request):

    print('Starting video stream.')

    # MicroPython can only use class-based async generators
    class stream():
        def __init__(self):
            self.i = 0
            self.test_image = bytearray(96*96)
            # setup the tensorflow interpreter
            print("person detection demo using images from the camera")
            print("read the model")
            person_detection_model_file = open ('models/person_detect_model.tflite', 'rb')
            person_detection_model = bytearray (300568)
            person_detection_model_file.readinto(person_detection_model)
            person_detection_model_file.close()
            
            print("Create the interpreter")
            self.interp = microlite.interpreter(person_detection_model,136*1024,
                                                self.input_callback, self.output_callback)
               
        def input_callback (self,microlite_interpreter):
            inputTensor = microlite_interpreter.getInputTensor(0)
            for i in range (0, len(self.test_image)):
                inputTensor.setValue(i, self.test_image[i])
            print ("setup %d bytes on the inputTensor." % (len(self.test_image)))

        def output_callback (self,microlite_interpreter):
            outputTensor = microlite_interpreter.getOutputTensor(0)
            not_a_person = outputTensor.getValue(0)
            person = outputTensor.getValue(1)
            print ("'not a person' = %d, 'person' = %d" % (not_a_person, person))
            '''
            if person > 10:
                neopixel[0] = (0,INTENSITY,0)   # green
            else:
                neopixel[0] = (INTENSITY,0,0)   # red
            neopixel.write()
            '''    

        def __aiter__(self):
            return self
            
        async def __anext__(self):
            await asyncio.sleep_ms(10)
            # concatenate file header, info header,
            # palette and pixel_data and write the bmp file
            self.test_image = camera.capture()
            self.interp.invoke()    
            frame = hdr + infoHdr + palette + self.test_image 
            return b'Content-Type: image/jpeg\r\n\r\n' + \
                frame + b'\r\n--frame\r\n'
            
        async def aclose(self):
            print('Stopping video stream.')
    
    print("Type of stream(): ",type(stream()))
    return stream(), 200, {'Content-Type':
                           'multipart/x-mixed-replace; boundary=frame'}


if __name__ == '__main__':
    app.run(debug=True,host=getIPAddress(), port=80)
