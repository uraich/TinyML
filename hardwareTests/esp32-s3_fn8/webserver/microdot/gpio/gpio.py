import machine
from neopixel import NeoPixel
from microdot.microdot import Microdot, redirect, send_file
from wifi_connect import connect, getIPAddress

print ("Connecting to the network")
connect()

app = Microdot()

SW1  = 38
LED1 = 34
LED3 = 33 # the neopixel
INTENSITY = 0x1f

led1 = machine.Signal(machine.Pin(LED1,machine.Pin.OUT),invert=True)
neopixel = NeoPixel(machine.Pin(LED3),1)
# switch neopixel off
neopixel[0] = (0,0,0)
neopixel.write()

@app.route('/', methods=['GET', 'POST'])
def index(request):
    form_cookie = None
    message_cookie = None
    print(request.form)

    if request.method == 'POST':
        print("post request")
        form_cookie = '{device},{color}'.format(device=request.form['device'],
                                            color=request.form['color'])
        
        if 'read' in request.form:
            print("Read request")
            if request.form["device"] == "SW1":
                pin = machine.Pin(SW1, machine.Pin.IN, machine.Pin.PULL_UP)
                message_cookie = 'Switch 1 is {state}.'.format(
                    state='open' if pin.value() else 'closed')
            elif request.form["device"] == "userLED":
                message_cookie = 'LED1 is now {state}.'.format(
                    state='on' if led1.value() else 'off')
            elif request.form["device"] == "neopixel":
                try:
                    message_cookie = 'The NeoPixel is now {state}.'.format(state=neopixel_color)                
                except:
                    message_cookie = 'The NeoPixel is now {state}.'.format(state="off")
        else:
            if request.form["device"] == "userLED":
                print("Setting SW1")
                if 'set-low' in request.form:
                    led1.off()
                    current_state="off"
                else:
                    led1.on()
                    current_state="on"
                message_cookie = 'LED1 is now {state}.'.format(state=current_state)
                
            elif request.form["device"] == "neopixel":
                print("Setting NeoPixel")
                if 'set-low' in request.form:
                    neopixel[0] = (0,0,0)
                    neopixel_color = "off"
                else:
                    if request.form["color"] == "red":
                        neopixel[0] = (INTENSITY,0,0)
                        neopixel_color = "red"
                    elif request.form["color"] == "green":
                        neopixel_color = "green"
                        neopixel[0] = (0,INTENSITY,0)
                    elif request.form["color"] == "blue":
                        neopixel_color = "blue"
                        neopixel[0] = (0,0,INTENSITY)
                message_cookie = 'The NeoPixel is now {state}.'.format(state=neopixel_color)
                neopixel.write()
                
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
