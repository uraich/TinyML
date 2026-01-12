from microdot import Microdot, send_file
from microdot.websocket import websocket_upgrade 
from wifi_connect import *
from neopixel import NeoPixel
from machine import Pin
import asyncio
import math

import sys
try:
    from hw_esp32_s3_fh4r2 import *
except:
    print("Please make sure hw_esp32_s3_fh4r2.py has been uploaded to /lib")
    sys.exit()

print ("Connecting to the network")
connect()

led = NeoPixel(Pin(NEOPIXEL),NO_OF_NEOPIXELS)
switch = Pin(0,Pin.IN)

oldSwitchState = -1

def writeNeopixel(r,g,b):
    # check if red and green are switched on this neopixel
    try:
        color_switch = GRB
    except:
        color_switch = False
    if color_switch:
        led[0] = (g,r,b)
    else:
        led[0] = (r,g,b)
    led.write()
        
app = Microdot()

@app.route('/')
async def index(request):
    # return send_file('html/led_switch.html')
    return send_file('html/ledAndSwitch.html')
ws = None
@app.route('/led_switch')
async def led_switch(request):
    global ws
    ws = await websocket_upgrade(request)
    print("WebSocket connection established")
    # create a new co-routine to observe the switch
    asyncio.create_task(writeMsg())
    while True:
        if ws == None:
            await asyncio.sleep_ms(100)
            continue
        else:
            print("Waiting for message")
            msg = await ws.receive()
            print("msg received: ",msg)
            colors = msg.split(",")
            red = math.floor(int(colors[0])*INTENSITY/255.0)
            green = math.floor(int(colors[1])*INTENSITY/255.0)
            blue = math.floor(int(colors[2])*INTENSITY/255.0)
            print("red: {:d}, green: {:d}, blue: {:d}".format(red,green,blue))
            writeNeopixel(red,green,blue)
            
async def writeMsg():
    global ws,oldSwitchState
    print("writeMsg task created")
    while True:
        if ws == None:
            await asyncio.sleep_ms(100)
            continue

        switchState = switch.value()
        if switchState != oldSwitchState:
            oldSwitchState = switchState
            if switchState:
                await ws.send("open")
                print("Sending switch state open")
            else:
                await ws.send("closed")
                print("Sending switch state closed")
        else:
            await asyncio.sleep_ms(10)
        
print("Please connect to http://" + getIPAddress())
app.run(debug=2, host = getIPAddress(), port=80)

