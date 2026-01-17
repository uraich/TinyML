# ble_demo.py: A demonstration of BlueTooth Low Energy communication
# to read and write sensors and actuators on the ESP32
# This program can be used either with the Serial BlueTooth terminal or
# nrf Connect on the smart phone or with the led_switch[.html,.css,.js)
# WEB program
# The commands to be used with the mobile phone programs are:
# set LED on : switch the LED on (in blue color)
# set LED off: switches the LED off
# read LED: returns the current state of the LED (on or off)
# LED rgb: r,g,b where r,g,b are values in the range 0..255
#          The LED will switch to the corresponding color
# When you push the boot button, the state change will be reported
# Copyright (c) U. Raich, January 2026
# This prohram is part of the TinyML course at the
# University of Cape Coast, Ghana
# It is released uder the MIT license

from machine import Pin
from neopixel import NeoPixel
from machine import Pin,Timer
from time import sleep_ms
import struct
import bluetooth
from ble_advertising import advertising_payload
from hw_esp32_s3_fh4r2 import *

import sys
try:
    from hw_esp32_s3_fh4r2 import *
except:
    print("Please make sure hw_esp32_s3_fh4r2.py has been uploaded to /lib")
    sys.exit()

_IRQ_CENTRAL_CONNECT = const(1)
_IRQ_CENTRAL_DISCONNECT = const(2)
_IRQ_GATTS_WRITE = const(3)

# Nordic UART Service (NUS)
_NUS_UUID = bluetooth.UUID('6e400001-b5a3-f393-e0a9-e50e24dcca9e')
_BLE_TX   = (
    bluetooth.UUID("6e400003-b5a3-f393-e0a9-e50e24dcca9e"),
    bluetooth.FLAG_NOTIFY,
)
_BLE_RX = (
    bluetooth.UUID("6e400002-b5a3-f393-e0a9-e50e24dcca9e"),
    bluetooth.FLAG_WRITE,
)    
_NUS_SERVICE = (
    _NUS_UUID,
    (_BLE_TX, _BLE_RX,),
)
    
# org.bluetooth.characteristic.gap.appearance.xml
_ADV_APPEARANCE_GENERIC_COMPUTER = const(128)

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
        
    # map values from 0..255 to 0..INTENSITY
    def scale(self,color):
       return int(color*INTENSITY/255.0)
    
    def rgb(self,red,green,blue):
        try:
            color_switch = GRB
        except:
            color_switch = False;
        if color_switch:            
            self.led[0] = (self.scale(green),self.scale(red),self.scale(blue))
        else:
            self.led[0] = (self.scale(red),self.scale(green),self.scale(blue))
        self.led.write()
        if red+green+blue <= 0:
            self.state = False
        else:
            self.state = True
        
    def toggle(self):
        if self.state:
            self.off()
        else:
            self.on()
            
    def state(self):
        return self.state

class ESP32_BLE():
    def __init__(self,ble,name="ESP32BLE",_rxbuf=100):
        # Create internal objects for the onboard LED
        # blinking when no BLE device is connected
        # stable ON when connected
        self.timer1 = Timer(0)
        self.led = BLE_led()
             
        self._ble = ble
        self._name = name
        self._ble.active(True)
        self._ble.irq(self._irq)
        ((self._tx_handle, self._rx_handle),) = self._ble.gatts_register_services((_NUS_SERVICE,))
        # Increase the size of the rx buffer and enable append mode.
        self._ble.gatts_set_buffer(self._rx_handle, _rxbuf, True)        
        self._connections = set()
        self.ble_msg=""
        self._tmp_msg=bytearray()
        # Optionally add services=[_UART_UUID], but this is likely to make the payload too large.
        self._payload = advertising_payload(name=self._name,services=[_NUS_UUID])
        # self._payload = advertising_payload(name=self._name, appearance=_ADV_APPEARANCE_GENERIC_COMPUTER)        
        # self._payload = bytearray('\x02\x01\x02','UTF-8') + \
        #                 bytearray((len(self._name) + 1, 0x09),'UTF-8') + self._name        
        # get the device address and print it
        addr = self._ble.config("mac")
        mac = addr[1]
        print("Device address: ",end="")
        for i in range(len(mac)-1):
            print("{:02x}:".format(mac[i]),end="")
        print("{:02x}".format(mac[len(mac)-1]))
        self.disconnected()
        self._advertise()

    def irq(self,handler):
        self._handler = handler

    def _irq(self,event,data):
        # Track connections so we can send notifications.
        # print("irq! event = {:d}".format(event))

        if event == _IRQ_CENTRAL_CONNECT :     # IRQ_CENTRAL_CONNECT
            conn_handle, _, _ = data      # A central has connected
            print("A central has connected")
            self._connections.add(conn_handle)
            self.connected()
            
        elif event == _IRQ_CENTRAL_DISCONNECT: # IRQ_CENTRAL_DISCONNECTED
                                               # a central has diconnected
            conn_handle, _, _ = data
            if conn_handle in self._connections:
                self._connections.remove(conn_handle)
            print("The central has disconnected")
            self.disconnected()
            # Start advertising again to allow a new connection.
            self._advertise()
            
        elif event == _IRQ_GATTS_WRITE:        # IRQ_GATTS_WRITE
                                               # A central has written a message
            # print("write event")
            conn_handle, value_handle = data
            # if conn_handle in self._connections:
            #     print("connection found")
            # if value_handle == self._rx_handle:
            #     print("rx handle found")
            if conn_handle in self._connections and value_handle == self._rx_handle:
                print("reading ble")
                tmp = self._ble.gatts_read(self._rx_handle)
                try:
                    self._tmp_msg = tmp.decode()
                except:
                    self.tmp_msg = tmp
                # self._tmp_msg = self._ble.gatts_read(self._rx_handle).decode()
                print("buffer after read: ",self._tmp_msg)
                print("Message type: ",type(self._tmp_msg))
                if '\r' in self._tmp_msg or '\n' in self._tmp_msg:
                    self.ble_msg = self._tmp_msg.strip()
                else:
                     self.ble_msg = self._tmp_msg 
                print("Message received from central: ",self.ble_msg)
                self._tmp_msg = ""

    def any(self):
        if len(self.ble_msg):
            return True
        else:
            return False
        
    def write(self,data):
        for conn_handle in self._connections:
            print("Sending " + data)
            self._ble.gatts_notify(conn_handle, self._tx_handle, data + '\n')
        
    def close(self):
        for conn_handle in self._connections:
            self._ble.gap_disconnect(conn_handle)
        self._connections.clear()
        
    def _advertise(self, interval_us=500000):
        print("advertising " + self._name)
        print("Advertising data: ",self._payload)
        self._ble.gap_advertise(interval_us, adv_data=self._payload)
        
    def connected(self):
        self.timer1.deinit()
        self.led.on()
        print("LED switched to steady on")
        
    def disconnected(self):
        self.timer1.init(period=100,mode=Timer.PERIODIC, callback = lambda src : self.led.toggle())
        
def demo():
    import time
    ble = bluetooth.BLE()
    led_ble = ESP32_BLE(ble)

    button = Pin(USER_SWITCH,Pin.IN)

    def buttons_irq(pin):
        if (button.value()):
            led_ble.write('switch state: open\r\n')
        else:
            led_ble.write('switch state: closed\r\n')            

    button.irq(trigger=Pin.IRQ_FALLING | Pin.IRQ_RISING, handler=buttons_irq)

    try:
        while True:
            # if led_ble.ble_msg != "":
            #     print("new message: ",led_ble.ble_msg)
            if led_ble.any():
                print("Decoding: ",led_ble.ble_msg)
                if led_ble.ble_msg == 'read LED':
                    print("LED is on" if led_ble.led.state else "LED is off")
                    led_ble.write("LED is on\r\n" if led_ble.led.state else "LED is off\r\n")
                elif led_ble.ble_msg == "set LED off":
                    print("Switching LED off")
                    led_ble.led.off()
                    led_ble.write("LED is now off")
                elif led_ble.ble_msg == "set LED on":
                    print("Switching LED on")
                    led_ble.led.on()
                    led_ble.write("LED is now on")
                elif "LED rgb:" in led_ble.ble_msg:
                    print(led_ble.ble_msg)
                    colors = led_ble.ble_msg.split(":")
                    rgb = colors[1].split(",")
                    if len(rgb) == 3:
                        print("red: ",int(rgb[0])," green: ",int(rgb[1]),", blue: ",int(rgb[2]))
                        led_ble.led.rgb(int(rgb[0]),int(rgb[1]),int(rgb[2]))
                    else:
                        print("Invalid message: ",led_ble.ble_msg)
                else:
                    print("Unknown command: {:s}! Skipping".format(led_ble.ble_msg))
                led_ble.ble_msg = ""
            sleep_ms(100)
        
    except KeyboardInterrupt:
        led_ble.close()

if __name__ == "__main__":
    demo()
