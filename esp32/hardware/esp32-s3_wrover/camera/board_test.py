import camera
import os,sys

try:
    from hw_esp32_cam import *
except:
    print("Please make sure hw_esp32_cam.py has been uploaded to /lib")
    sys.exit()

print("We are on the ESP32-CAM");

cam_init_result = camera.init(0,                              
                              format=camera.JPEG, framesize=camera.FRAME_VGA, 
                              xclk_freq=camera.XCLK_20MHz)

"""
cam_init_result = camera.init(0, d0=CAM_D0, d1=CAM_D1, d2=CAM_D2, d3=CAM_D3,
                              d4=CAM_D4, d5=CAM_D5, d6=CAM_D6, d7=CAM_D7,
                              format=camera.JPEG, framesize=camera.FRAME_VGA, 
                              xclk_freq=camera.XCLK_20MHz,
                              href=CAM_HREF, vsync=CAM_VSYNC,
                              reset=CAM_RESET, pwdn=CAM_PWDN,
                              sioc=CAM_SIOC, siod=CAM_SIOD,
                              xclk=CAM_XCLK, pclk=CAM_PCLK)
"""
if cam_init_result:
  print("Camera successfully initialized")
else :
  print("Camera initialization failed")
