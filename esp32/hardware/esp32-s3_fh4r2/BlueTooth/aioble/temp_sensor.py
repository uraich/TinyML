import sys

# ruff: noqa: E402
sys.path.append("")

from micropython import const

import asyncio
import aioble
import bluetooth

import random
import struct
from machine import Pin,Timer
import onewire, ds18x20

led = Pin(2,Pin.OUT)
def toggle_led(src):
    led.toggle()
# create a timer to blink the LED rapidely
timer = Timer(0)
timer.init(period=100,mode=Timer.PERIODIC, callback = toggle_led)

# the device is on GPIO21
# dat = Pin(35)  # this corresponds to D2 on esp32s3-mini
dat = Pin(21)  # this corresponds to D2 on esp32s3-mini

# create the onewire object
ds = ds18x20.DS18X20(onewire.OneWire(dat))

# scan for devices on the bus

roms = ds.scan()
if len(roms) == 0:
    print("No ds18b20 found, using random temperature values around 24.5°")
    no_ds18x20 = True
else:
    print("No of devices: ",len(roms))
    print('found devices:', roms)
    no_ds18x20 = False
    
# org.bluetooth.service.environmental_sensing
_ENV_SENSE_UUID = bluetooth.UUID(0x181A)
# org.bluetooth.characteristic.temperature
_ENV_SENSE_TEMP_UUID = bluetooth.UUID(0x2A6E)
# org.bluetooth.characteristic.gap.appearance.xml
_ADV_APPEARANCE_GENERIC_THERMOMETER = const(768)

# How frequently to send advertising beacons.
_ADV_INTERVAL_US = 250_000


# Register GATT server.
temp_service = aioble.Service(_ENV_SENSE_UUID)
temp_characteristic = aioble.Characteristic(
    temp_service, _ENV_SENSE_TEMP_UUID, read=True, notify=True
)
aioble.register_services(temp_service)

# Helper to encode the temperature characteristic encoding (sint16, hundredths of a degree).
def _encode_temperature(temp_deg_c):
    return struct.pack("<h", int(temp_deg_c * 100))


# This would be periodically polling a hardware sensor.
async def sensor_task():
    if no_ds18x20: 
        t = 24.5

        while True:
            temp_characteristic.write(_encode_temperature(t), send_update=True)
            t += random.uniform(-0.5, 0.5)
            await asyncio.sleep_ms(1000)
    else:
        while True: # use the temperature from the ds28b20
            ds.convert_temp()
            await asyncio.sleep_ms(1000)
            t = ds.read_temp(roms[0])
            print("Temperature: ",t)
            temp_characteristic.write(_encode_temperature(t), send_update=True)            

# Serially wait for connections. Don't advertise while a central is
# connected.
async def peripheral_task():

    while True:
        async with await aioble.advertise(
            _ADV_INTERVAL_US,
            name="mpy-temp",
            services=[_ENV_SENSE_UUID],
            appearance=_ADV_APPEARANCE_GENERIC_THERMOMETER,
        ) as connection:
            print("Connection from", connection.device)
            # stop the timer frlom blinking
            timer.deinit()
            # and switch the LED permanently on
            led.on()
            await connection.disconnected(timeout_ms=None)
            # have the led blink again
            print("BlueTooth central has disconnected")
            timer.init(period=100,mode=Timer.PERIODIC, callback = toggle_led)

# Run both tasks.
async def main():
    t1 = asyncio.create_task(sensor_task())
    t2 = asyncio.create_task(peripheral_task())
    await asyncio.gather(t1, t2)


asyncio.run(main())
