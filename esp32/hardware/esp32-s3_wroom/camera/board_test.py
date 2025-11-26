import camera
import os
osVersion=os.uname()

if osVersion.machine.find('Octal-SPIRAM') != -1:
  print("We are on the ESP32S3-WROOM")
  cam_init_result = camera.init(0, d0=11, d1=9, d2=8, d3=10, d4=12, d5=18, d6=17, d7=16,
                                format=camera.JPEG, framesize=camera.FRAME_VGA, 
                                xclk_freq=camera.XCLK_20MHz,
                                href=7, vsync=6, reset=-1, pwdn=-1,
                                sioc=5, siod=4, xclk=15, pclk=13)
elif osVersion.machine.find('8MB SPI RAM') != -1:
  print("We are on the ESP32-S3-FN8");
  cam_init_result = camera.init(0, d0=5, d1=3, d2=2, d3=4, d4=6, d5=8, d6=9, d7=11,
                                format=camera.JPEG, framesize=camera.FRAME_VGA, 
                                xclk_freq=camera.XCLK_20MHz,
                                href=12, vsync=13, reset=-1, pwdn=-1,
                                sioc=14, siod=21, xclk=10, pclk=7)
else:
  print("We are on an ESP32-CAM")

if cam_init_result:
  print("Camera successfully initialized")
else :
  print("Camera initialization failed")