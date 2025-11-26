# gpio.py: controls the on board devices connected to GPIO lines
# The ESP32-CAM main board has a switch connected to GPIO 0, which can be used to set the module
# into flash programming mode. If a normal user program is running, the switch can be used
# The flash LED is connected to GPIO 4. At its max light intensity it is
# extremely bright. For this reason we turn down the intensity to less than 50%
# of its maximum using PWM. Please put a paper onto the flash LED to protect your eyes.
#
# Copyright (c) U. Raich, Mar, 2024
# This program is part of a course on tinyML for the
# African Internet Summit 2024
# It is released under the MIT license

import machine
from microdot.microdot import Microdot, redirect, send_file
from wifi_connect import connect, getIPAddress

try:
    from hw_esp32_cam import *
except:
    print("Please make sure hw_esp32_cam.py has been uploaded to /lib")
    sys.exit()

print ("Connecting to the network")
connect()

app = Microdot()
global flash_intensity

led1 = machine.Signal(machine.Pin(USER_LED,machine.Pin.OUT),invert=True)
led1.off()                                   # switch user led off 
flashPin=machine.Pin(FLASH,machine.Pin.OUT)  # create PWM object from pin4, Set Pin4 to output
flash = machine.PWM(flashPin)
flash.duty(0)                                # switch the flash light off as well
flash_intensity = '0%'

@app.route('/', methods=['GET', 'POST'])
def index(request):
    global flash_intensity
    form_cookie = None
    message_cookie = None
    print(request.form)

    if request.method == 'POST':
        print("post request")
        form_cookie = '{device},{intensity}'.format(device=request.form['device'],
                                            intensity=request.form['intensity'])
        
        if 'read' in request.form:
            print("Read request")
            if request.form["device"] == "SW1":
                pin = machine.Pin(USER_SWITCH, machine.Pin.IN, machine.Pin.PULL_UP)
                message_cookie = 'Switch GPIO 0 is {state}.'.format(
                    state='open' if pin.value() else 'closed')
            elif request.form["device"] == "userLED":
                message_cookie = 'User LED is now {state}.'.format(
                    state='on' if led1.value() else 'off')
            elif request.form["device"] == "flashLight":
                message_cookie = 'The Flash light is now {state}.'.format(state=flash_intensity)                
        else:
            if request.form["device"] == "userLED":
                print("Setting SW1")
                if 'set-low' in request.form:
                    led1.off()
                    current_state="off"
                else:
                    led1.on()
                    current_state="on"
                message_cookie = 'User LED is now {state}.'.format(state=current_state)
                
            elif request.form["device"] == "flashLight":
                print("Setting Flash Light")
                if 'set-low' in request.form:
                    flash.duty(0)
                    flash_intensity = '0%'
                else:
                    if request.form["intensity"] == "5%":
                        dutyCycle = 1024*5//100
                        print("Duty Cycle: ",dutyCycle)
                        flash.duty(dutyCycle)
                        flash_intensity = '5%'
                    elif request.form["intensity"] == "10%":
                        flash.duty(1024*10//100)
                        flash_intensity = '10%'
                    elif request.form["intensity"] == "20%":
                        flash.duty(1024*20//100)
                        flash_intensity = '20%'
                    elif request.form["intensity"] == "30%":
                        flash.duty(1024*30//100)
                        flash_intensity = '30%'
                    elif request.form["intensity"] == "40%":
                        flash.duty(1024*40//100)
                        flash_intensity = '40%'
                    elif request.form["intensity"] == "50%":
                        flash.duty(1024*50//100)
                        flash_intensity = '50%'

                message_cookie = 'The Flash Light is now {state}.'.format(state=flash_intensity)

                
        response = redirect('/')
    else:
        if 'message' not in request.cookies:
            message_cookie = 'Select a device and an operation below.'
        response = send_file('html/gpio.html')
    if form_cookie:
        response.set_cookie('form', form_cookie)
    if message_cookie:
        response.set_cookie('message', message_cookie)
    return response
    

app.run(debug=True, host=getIPAddress(), port=80)
