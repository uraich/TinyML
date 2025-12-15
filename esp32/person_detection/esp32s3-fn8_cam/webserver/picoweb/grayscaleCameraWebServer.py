import picoweb
import time
import network
import camera
import uasyncio as asyncio
from machine import Pin, PWM
from wifi_connect import connect, getIPAddress
import struct
import sys

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
print("Running picoweb on the ESP32-S3-FN8")

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

html = '''<!doctype html>
<html>
  <head>
    <title>PicoWeb Video Streaming</title>
    <meta charset="UTF-8">
  </head>
  <body>
    <h1>picoweb Video Streaming</h1>
    <img src="/video_feed">
  </body>
</html>'''

print("Starting the WEB server")
app = picoweb.WebApp("__main__")

@app.route('/')
async def index(req,resp):
    yield from resp.awrite(html)
    print("Starting video stream")

@app.route('/video_feed')
async def video_feed(req,resp):
    global frame_index
    headers= """resp.Connection: keep-alive
Cache-Control: no-cache, no-store, max-age=0, must-revalidate
Expires: Thu, Jan 01 2024 00:00:00 GMT
Pragma: no-cache
"""
    frame="""--frame
Content-Type: image/bmp
"""
    print("start stream")    
    yield from picoweb.start_response(resp, content_type='multipart/x-mixed-replace; boundary=frame')  
    while True:
        yield from resp.awrite(next(send_frame()))
        gc.collect()
    
def send_frame():
    # print("in send_frame")
    # get a new image from the camera
    pixel_data = camera.capture()
    # concatenate file header, info header, palette and pixel_data and write the bmp file
    frame = hdr + infoHdr + palette + pixel_data 
    yield  (b'--frame\r\n'
           b'Content-Type: image/jpeg\r\n\r\n'
           + frame + b'\r\n')

    
if __name__ == '__main__':
    app.run(debug=2,host=getIPAddress(), port=80)
