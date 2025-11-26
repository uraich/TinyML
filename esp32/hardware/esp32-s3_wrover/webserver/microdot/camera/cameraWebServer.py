import sys
import asyncio
import camera
from machine import Pin
from microdot import Microdot, send_file
from wifi_connect import connect, getIPAddress

try:
    from hw_esp32_cam import *
except:
    print("Please make sure hw_esp32_s3_fn8.py has been uploaded to /lib")
    sys.exit()

# connect to WiFi
connect()
app = Microdot()

print("Init camera")
# Disable camera initialization
# camera.deinit()

# Enable camera initialization
print("We are on the ESP32-CAM")

cam_init_result = camera.init(0,format=camera.JPEG, framesize=camera.FRAME_VGA, 
                              xclk_freq=camera.XCLK_20MHz)
if cam_init_result:
  print("Camera was successfully initialized")
else:
  print("Camera initialization failed");

print("Starting the WEB server")

@app.route('/')
async def index(request):
    return send_file("html/camera.html",status_code=200, content_type="text/html")

@app.route("/status")
def index(req):
  print("status route")
  print(camera.get_framesize())
  jsonDict={}
  jsonDict.update({"framesize":camera.get_framesize()})
  jsonDict.update({"quality":camera.get_quality()})
  jsonDict.update({"brightness":camera.get_brightness()})
  jsonDict.update({"contrast":camera.get_contrast()})
  jsonDict.update({"saturation":camera.get_saturation()})
  jsonDict.update({"special_effect":camera.get_speffect()})
  jsonDict.update({"wb_mode":camera.get_wb_mode()})
  jsonDict.update({"awb":camera.get_whitebal()})
  jsonDict.update({"awb_gain":camera.get_awb_gain()})
  jsonDict.update({"aec":camera.get_exposure_ctrl()})
  jsonDict.update({"aec2":camera.get_aec2()})
  jsonDict.update({"ae_level":camera.get_aelevel()})
  jsonDict.update({"agc":camera.get_gain_ctrl()})
  jsonDict.update({"agc_gain":camera.get_agc_gain()})
  jsonDict.update({"gainceiling":camera.get_gainceiling()})
  jsonDict.update({"bpc":camera.get_bpc()})
  jsonDict.update({"wpc":camera.get_wpc()})
  jsonDict.update({"raw_gma":camera.get_raw_gma()})
  jsonDict.update({"lenc":camera.get_lenc()})
  jsonDict.update({"vflip":camera.get_vflip()})
  jsonDict.update({"hmirror":camera.get_hmirror()})
  jsonDict.update({"dcw":camera.get_dcw()})
  jsonDict.update({"colorbar":camera.get_colorbar()})
  print(jsonDict)
  return jsonDict              
 
@app.route('/video_feed')
async def video_feed(request):
    print('Starting video stream.')

    # MicroPython can only use class-based async generators
    class stream():
        def __init__(self):
            self.i = 0
            
        def __aiter__(self):
            return self
            
        async def __anext__(self):
            await asyncio.sleep_ms(50)
            buf=camera.capture()
            # self.i = (self.i + 1) % len(frames)
            # return b'Content-Type: image/jpeg\r\n\r\n' + \
            #    frames[self.i] + b'\r\n--frame\r\n'
            return b'Content-Type: image/jpeg\r\n\r\n' + \
               buf + b'\r\n--frame\r\n'
            
        async def aclose(self):
            print('Stopping video stream.')
    
    print("Type of stream(): ",type(stream()))
    return stream(), 200, {'Content-Type':
                           'multipart/x-mixed-replace; boundary=frame'}

@app.route("/control")
async def control(req):
  print("control route")
  
  if req.args["var"] == "framesize":
    framesize = int(req.args["val"])
    print("Setting frame size to: %d"%framesize)
    camera.set_framesize(framesize)
    
  if req.args["var"] == "quality":
    quality = int(req.args["val"])
    print("Setting quality to %d"%quality)
    camera.set_quality(quality)
    
  if req.args["var"] == "brightness":
    brightness = int(req.args["val"])
    print("Setting brightness to %d"%brightness)
    camera.set_brightness(brightness)
    
  if req.args["var"] == "contrast":
    contrast = int(req.args["val"])
    print("Setting contrast to: %d"%contrast)
    camera.set_contrast(contrast)
    
  if req.args["var"] == "saturation":
    saturation = int(req.args["val"])
    print("Setting saturation to: %d",saturation)
    camera.set_saturation(saturation)

  if req.args["var"] == "special_effect":
    effect = int(req.args["val"])
    print("Setting special effect: %d"%effect)
    camera.set_speffect(effect)
    
  if req.args["var"] == "awb":
    awb = int(req.args["val"])
    if awb:
      print("Enabling white ballance")
    else:
      print("Disabling white ballance")
    camera.set_whitebal(awb)
    
  if req.args["var"] == "awb_gain":
    awb_gain = int(req.args["val"])
    print("Setting white ballance gain to %d"%awb)
    camera.set_awb_gain(awb_gain)
    
  if req.args["var"] == "wb_mode":
    wb_mode = int(req.args["val"])
    print("Setting white ballance mode to %d"%wb_mode)
    camera.set_wb_mode(wb_mode)
    
  if req.args["var"] == "aec":
    aec = int(req.args["val"])
    if aec:
      print("Enabling aec sensor")
    else:
      print("Disabling aec sensor")
    camera.set_aec(aec)
    
  if req.args["var"] == "aec2":
    aec2 = int(req.args["val"])
    if aec2:
      print("Enabling aec dsp")
    else:
      print("Disabling aec dsp")
    camera.set_aec2(aec2)
    
  if req.args["var"] == "aec_value":
    ae_level = int(req.args["val"])
    print("Setting ae level to %d"%ae_level)
    camera.set_ae_level(ae_level)
    
  if req.args["var"] == "agc":
    agc = int(req.args["val"])
    print("Setting agc to %d"%agc)
    camera.set_agc(agc)
    
  if req.args["var"] == "agc_gain":
    agc_gain = int(req.args["val"])
    print("Setting agc_gain to %d"%agc_gain)
    camera.set_agc_gain(agc_gain)
    
  if req.args["var"] == "gainceiling":
    gainceiling = int(req.args["val"])
    print("Setting gain_ceiling to %d"%gain_ceiling)
    camera.set_gainceiling(gainceiling)
    
  if req.args["var"] == "bpc":
    bpc = int(req.args["val"])
    print("Setting bpc to %d"%bpc)
    camera.set_bpc(bpc)
    
  if req.args["var"] == "wpc":
    wpc = int(req.args["val"])
    print("Setting wpc to %d"%wpc)
    camera.set_wpc(wpc)
    
  if req.args["var"] == "raw_gma":
    raw_gma = int(req.args["val"])
    print("Setting raw_gma to %d"%raw_gma)
    camera.set_raw_gma(raw_gma)
    
  if req.args["var"] == "lenc":
    lenc = int(req.args["val"])
    if lenc:
      print("Switching lens correction on")
    else:
      print("Switching lens correction off")
    camera.set_lenc(lenc)
    
  if req.args["var"] == "dcw":
    dcw = int(req.args["val"])
    if dcw:
      print("Enabling downsizing")
    else:
      print("Disabling downsizing")      
    camera.set_dcw(dcw)
        
  if req.args["var"] == "colorbar":
    print("Setting colorbar mode")
    cb = int(req.args["val"])
    if (cb):
      print("Colorbar is enabled")
    else:
      print("Colorbar is disabled")      
    camera.set_colorbar(cb)
    
  if req.args["var"] == "vflip":
    print("Setting vertical flip")
    vflip = int(req.args["val"])
    if (vflip):
      print("Vertical flip is enabled")
    else:
      print("Vertical flip is disabled")      
    camera.set_vflip(vflip)

  if req.args["var"] == "hmirror":
    print("Setting horizontal mirror")
    hmirror = int(req.args["val"])
    if (hmirror):
      print("Horizontal mirror is enabled")
    else:
      print("Horizontal mirror is disabled")      
    camera.set_hmirror(hmirror)
    
  if req.args["var"] == "awb":
    print("Setting white ballance")
    awb = int(req.args["val"])
    camera.set_whitebal(awb)
    
  #yield from resp.awrite("control")
  return ("control")


@app.route("/capture")
def capture(req):
  print("capture route")
  print("Taking image")
  buf = camera.capture()
    
  if len(buf) > 0:
    print("Image successfully taken")
    return buf, 202, {'Content-Type': 'image/jpeg'}

  else:      
    return 'Capture Error', 503

if __name__ == '__main__':
    app.run(debug=True,host=getIPAddress(), port=80)
