# magic_wand_ble_led_from_file.py: Reads a json file with stroke data for each digit
# Sends the data to the Web server written in JavaScript using BlueTooth Low Energy as
# communication vehicle
# This program allows to test the data communication between the magic wand program and
# the BlueTooth Central
# Copyright (c) U. Raich Jan 2026
# This program is part of the TinyML course at the
# University of Cape Coast, Ghana
# It is released under the MIT license

import asyncio
import aioble
import bluetooth
import struct
import time
import sys
from micropython import const
from machine import Pin, Timer
from neopixel import NeoPixel
import json
from struct import pack
from micropython import const

try:
    from hw_esp32_s3_fh4r2 import *
except:
    print("Please install hw_esp32_s3_fh4r2 before running this program!")
    sys.exit
    
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
    
def MAGIC_WAND_UUID(val):
    return "4798e0f2-" + val + "-4d68-af64-8a8f5258404e"

stroke_struct_byte_count = 1288

_MAGIC_WAND_SERVICE_UUID =  bluetooth.UUID(MAGIC_WAND_UUID("0000"))
_MAGIC_WAND_CHARACTERISTIC_UUID = (bluetooth.UUID(MAGIC_WAND_UUID("300a")))

# How frequently to send advertising beacons.
_ADV_INTERVAL_US = 250_000

# Register GATT server.
magic_wand_service = aioble.Service(_MAGIC_WAND_SERVICE_UUID)
magic_wand_characteristic = aioble.Characteristic(
    magic_wand_service, _MAGIC_WAND_CHARACTERISTIC_UUID, read=True)

aioble.register_services(magic_wand_service)
global connected
connected = False

print("service UUID: ",_MAGIC_WAND_SERVICE_UUID)
print("characteristic UUID: ",_MAGIC_WAND_CHARACTERISTIC_UUID)

    
# create a timer to blink the LED rapidely
def toggle(src):
    ble_led.toggle()
    
ble_led = BLE_led()
timer = Timer(0)
timer.init(period=100,mode=Timer.PERIODIC, callback = toggle)

# Serially wait for connections. Don't advertise while a central is
# connected.
async def peripheral_task():

    while True:
        global connected
        async with await aioble.advertise(
            _ADV_INTERVAL_US,
            name="magicWand",
            services=[_MAGIC_WAND_SERVICE_UUID],
            manufacturer=(0x5552, b" Uli"), # corresponds to ascii UR
        ) as connection:
            print("Connection from", connection.device)
            # stop the timer from blinking
            timer.deinit()
            # and switch the LED permanently on
            ble_led.on()
            connected = True
            await connection.disconnected(timeout_ms=None)
            connected = False
            # have the led blink again
            print("BlueTooth central has disconnected")
            timer.init(period=100,mode=Timer.PERIODIC, callback = toggle)

global stokes            
strokes = {}
# states
WAITING = const(0)
DRAWING = const(1)
DONE    = const(2)
STROKE_TRANSMIT_STRIDE = const(2)
STROKE_LENGTH = const(160)
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
    printTransmitBuffer(transmitBuffer)
    return transmitBuffer

async def sensor_task():
    # Read the strokes json file
    global strokes
    try:
        jsonFile = open("strokes/digits.json","r")
        strokes = json.load(jsonFile)
    except:
        print("Please make sure that digits.json has been uploaded to /strokes")
        sys.exit()
        
    while True:
        if not connected:
            print("Not connected yet")
            await asyncio.sleep_ms(2000)
            continue
        for digit in range(10):
            transmitBuffer = createTransmitBuffer(digit)
            # Send this transmit buffer to the BlueTooth central
            magic_wand_characteristic.write(transmitBuffer, send_update=True)
            await asyncio.sleep_ms(5000)
        
# Run both tasks.
async def main():
    t1 = asyncio.create_task(sensor_task())
    t2 = asyncio.create_task(peripheral_task())
    await asyncio.gather(t1, t2)


asyncio.run(main())
