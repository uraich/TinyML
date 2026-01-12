# acc_gyro.py: sends accelerometer and gyroscope data to the browser 
# a new set of values is sent every 100 ms
# This program demonstrates the use of server side events for communication
# between a web server running on the ESP32 and a browser running JavaScript
# Copyright (c) U. Raich, Jan. 2026
# This program is part of a course on TinyML at the
# University of Cape Coast, Ghana
# It is released under the MIT license

import asyncio
from microdot import Microdot, send_file
from microdot.sse import with_sse
from wifi_connect import *
from LSM6DS3_i2c import LSM6DS3_I2C
from LSM6DS3_const import *
from utime import sleep_ms

print ("Connecting to the network")
connect()

# Initialize the LSM6DS3

lsm6ds3 = LSM6DS3_I2C()
print("Device ID: 0x{:02x}".format(lsm6ds3.getDeviceID))
print("Reset the device")
lsm6ds3.sw_reset()
sleep_ms(10)

print("---------------------------------------------------------")
print("Setting up the accelerometer") 
print("output data rate: 26 Hz, full scale 4g, bw: 50Hz") 
print("---------------------------------------------------------")

lsm6ds3.acc_odr="26 Hz"
print("acc output datarate: 0x{:02x}".format(lsm6ds3.acc_odr))
print("This corresponds to " + lsm6ds3.acc_odr_txt(lsm6ds3.acc_odr))
print("The numerical value is {:6.1f}".format(lsm6ds3.acc_odr_value(
     lsm6ds3.acc_odr_txt(lsm6ds3.acc_odr))))    
print("Setting full scale to 4g")
lsm6ds3.acc_full_scale="4 g"
full_scale = lsm6ds3.acc_full_scale
print("Acc full scale value: {:d}".format(full_scale))
print("Acc full scale: " + lsm6ds3.acc_full_scale_txt(full_scale))

lsm6ds3.acc_bandwidth = "50 Hz"
print("acc bandwidth: 0x{:02x}".format(lsm6ds3.acc_bandwidth))
print("This corresponds to " + lsm6ds3.acc_bandwidth_txt(lsm6ds3.acc_bandwidth))
print("ctrl1_xl: 0x{:02x}".format(lsm6ds3.ctrl1_xl))
      
print("---------------------------------------------------------")
print("Setting up the gyroscope")
print("output data rate: 26 Hz, full scale: 2000 dps") 
print("---------------------------------------------------------")

lsm6ds3.gyro_odr="26 Hz"
print("gyro output datarate: 0x{:02x}".format(lsm6ds3.gyro_odr))
print("This corresponds to " + lsm6ds3.gyro_odr_txt(lsm6ds3.gyro_odr))
print("The numerical value is {:6.1f}".format(lsm6ds3.gyro_odr_value(
     lsm6ds3.gyro_odr_txt(lsm6ds3.gyro_odr))))

print("Setting gyro full scale to 2000 dps")
lsm6ds3.gyro_full_scale="2000 dps"
full_scale = lsm6ds3.gyro_full_scale
print("Gyro full scale value: {:d}".format(full_scale))
print("Gyro full scale: " + lsm6ds3.gyro_full_scale_txt(full_scale))

sleep_ms(40)  # wait for the data to become ready 40ms <=> 25Hz

print("Starting accelerometer/gyroscope WEB server")

app = Microdot()

@app.route("/")
async def main(request):
    return send_file('html/acc_gyro.html')


@app.route('/events')
@with_sse
async def events(request, sse):
    print('Client connected')
    try:
        while True:
            await asyncio.sleep_ms(500)

            while not lsm6ds3.acc_data_available:
                sleep_ms(1)
            acc_x = lsm6ds3.acc_x
            acc_y = lsm6ds3.acc_y
            acc_z = lsm6ds3.acc_z

            gyro_x = lsm6ds3.gyro_x
            gyro_y = lsm6ds3.gyro_y
            gyro_z = lsm6ds3.gyro_z
                
            timeStamp=dateString(cetTime())
            msg = "{:s},{:5.3f},{:5.3f},{:5.3f},{:5.3f},{:5.3f},{:5.3f}".format(
                timeStamp,acc_x,acc_y,acc_z,gyro_x,gyro_y,gyro_z)
            print("Sending: ",msg)
            await sse.send(msg)
            
    except asyncio.CancelledError:
        pass
    print('Client disconnected')

import ulogging as logging
logging.basicConfig(level=logging.INFO)

print("Please connect to http://" + getIPAddress())
app.run(debug=2, host = getIPAddress(), port=80)
