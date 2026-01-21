# magic_wand_ble_led_from_file_ws.py: Reads a json file with stroke data for each digit
# Sends the data to the Web server written in JavaScript using Web sockets as
# communication vehicle
# This program allows to test the data communication between the magic wand program and
# the BlueTooth Central
# Copyright (c) U. Raich Jan 2026
# This program is part of the TinyML course at the
# University of Cape Coast, Ghana
# It is released under the MIT license

import asyncio
import sys
import errno
from micropython import const
from machine import Pin, Timer
from neopixel import NeoPixel
import json
from struct import pack
from micropython import const
from microdot import Microdot, send_file
from microdot.websocket import websocket_upgrade
from wifi_connect import connect, getIPAddress

try:
    from hw_esp32_s3_fh4r2 import *
except:
    print("Please install hw_esp32_s3_fh4r2 before running this program!")
    sys.exit

# connect to wifi
connect()

class BLE_led():
    
    def __init__(self):
        self.state = False
        self.led = NeoPixel(Pin(NEOPIXEL),NO_OF_NEOPIXELS)

    def off(self):
        # switch LED off
        self.led[0] = (0,0,0)
        self.led.write()
        self.state = False

    def on(self):
        # switch LED on (blue color)
        self.led[0] = (0,0,INTENSITY)
        self.led.write()
        self.state = True

    def toggle(self):
        if self.state:
            self.off()
        else:
            self.on()
            
    def state(self):
        return self.state
    
# create a timer to blink the LED rapidely
def toggle(src):
    ble_led.toggle()
    
ble_led = BLE_led()
timer = Timer(0)
timer.init(period=100,mode=Timer.PERIODIC, callback = toggle)
            
strokes = {}

# states
WAITING = const(0)
DRAWING = const(1)
DONE    = const(2)
STROKE_TRANSMIT_STRIDE = const(2)
STROKE_LENGTH = const(160)

# Read the strokes json file
print("Reading digits.json")
try:
    jsonFile = open("strokes/digits.json","r")
    strokes = json.load(jsonFile)
except:
    print("Please make sure that digits.json has been uploaded to /strokes")
    sys.exit()
        
# gets the stroke points for a particular digit
def findStroke(digit_no):
    for i in range(10):
        if strokes["strokes"][i]["label"] == str(digit_no):
            print("Stroke {:d} found!".format(digit_no))
    return strokes["strokes"][digit_no]["strokePoints"]

def printTransmitBuffer(transmitBuffer):
    print("--------------------- Transmit Buffer ------------------------")
    print("No of stroke points: ",(len(transmitBuffer)-8)//STROKE_TRANSMIT_STRIDE)
    print("State:",end=" ")
    for i in range(3):
        print("0x{:02x},".format(transmitBuffer[i]),end=" ")
    print("0x{:02x}".format(transmitBuffer[3]))
    print("Stroke Length:",end=" ")
    for i in range(4,8):
        print("0x{:02x},".format(transmitBuffer[i]),end=" ")
    print("0x{:02x}".format(transmitBuffer[7]))
    
    for i in range(8,len(transmitBuffer)-1):
        if i == 0:
            print("0x{:04x}: ".format(i),end="" )
        elif not i%16:
            print("\n0x{:04x}: ".format(i),end="" )            
        print("0x{:02x},".format(transmitBuffer[i]),end=" ")
    print("0x{:02x}".format(transmitBuffer[len(transmitBuffer)-1]))

def createTransmitBuffer(digit_no):
    status = DONE
    strokePoints = findStroke(digit_no)
    byteStrokePoints = bytearray([])
    
    print(strokePoints[0])
    for i in range(len(strokePoints)):
        tmp_x = round(float(strokePoints[i]["x"])*128.0)
        if i == 0:
            print("type of x[0]: ",type(tmp_x))
        if tmp_x < -128:
            tmp_x = -128
        if tmp_x > 127:
            tmp_x = 127
        byteStrokePoints += tmp_x.to_bytes()
        
        tmp_y = round(float(strokePoints[i]["y"])*128.0)
        if tmp_y < -128:
            tmp_y = -128
        if tmp_y > 127:
            tmp_y = 127
        byteStrokePoints += tmp_y.to_bytes()

    print("x[0]: ",byteStrokePoints[0])
    print("y[0]: ",byteStrokePoints[1])

    transmitBufferHeader = pack("<ii",status,len(byteStrokePoints)//STROKE_TRANSMIT_STRIDE)
    padding = bytearray(STROKE_LENGTH*STROKE_TRANSMIT_STRIDE - len(byteStrokePoints))
    print("Padding length: ",len(padding))
    transmitBuffer = transmitBufferHeader + byteStrokePoints + padding
    print("Length of transmit buffer: ",len(transmitBuffer))
    print("Should be: ",160*2+8)
    # printTransmitBuffer(transmitBuffer)
    return transmitBuffer

app = Microdot()

@app.route('/')
async def index(request):
    return send_file('html/magic_wand.html')

ws = None
@app.route('/magic_wand')
async def magic_wand(request):
    global ws
    try:
        asyncio.create_task(writeMsg())
        ws = await websocket_upgrade(request)
        while ws == None:
            await asyncio.sleep_ms(100)
        print("WebSocket connection established")
        timer.deinit()
        ble_led.on()
        # the client cancelled the connection
    except asyncio.CancelledError:
        print("CancelledError seen. Client disconnected")
        # start blinking the LED again
        ws = None
        timer.init(period=100,mode=Timer.PERIODIC, callback = toggle)
        return
    while True:
        await asyncio.sleep_ms(100)
        if ws == None:
            break

async def writeMsg():
    global ws,oldSwitchState
    print("writeMsg task created")
    print("ws: ",ws)
    try:
        while True:
            if ws == None:
                await asyncio.sleep_ms(100)
                continue
            else:
                await ws.send("Hello")
                await asyncio.sleep_ms(1000)
    except OSError as err:
        # print("Error code: ",errno.errorcode[err.errno])
        # print("errno: ",err.errno," ECONNRESET: ",errno.ECONNRESET)
        if err.errno == errno.ECONNRESET:
            print("Client has disconnected")
            ws = None
            timer.init(period=100,mode=Timer.PERIODIC, callback = toggle)
            # exit the writeMsg task
            return
            
print("Please connect to http://" + getIPAddress())
app.run(debug=2, host = getIPAddress(), port=80)
