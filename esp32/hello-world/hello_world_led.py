# Microlite implementation of the tensorflow hello-world example
# https://github.com/tensorflow/tensorflow/tree/master/tensorflow/lite/micro/examples/hello_world
# This is a slightly modified version where the output of the model is
# displayed on the on-board LED

import microlite
import io
from machine import Pin
from neopixel import NeoPixel
from math import pi

kXrange = 2.0 * pi
steps = 1000
current_input = None

def input_callback (microlite_interpreter):
    global current_input
    inputTensor = microlite_interpreter.getInputTensor(0)
    # print (inputTensor)
    position = counter*1.0
    # print ("position %f" % position)
    x = position * kXrange/steps
    current_input = x
    # print ("x: %f, " % x)
    x_quantized = inputTensor.quantizeFloatToInt8(x)
    inputTensor.setValue(0, x_quantized)

def output_callback (microlite_interpreter):
    global current_input
    # print ("output callback")
    outputTensor = microlite_interpreter.getOutputTensor(0)
    # print (outputTensor)
    y_quantized = outputTensor.getValue(0)
    y = outputTensor.quantizeInt8ToFloat(y_quantized)
    print ("%f,%f" % (current_input,y))   # these values can be used for offline plotting
    
    # convert the output of the model (values -1 .. +1) to values that can be used
    # as light intensity for the neopixel (0 .. maxIntensity)
    intens = int(((y+1)/2)*maxIntensity)
    
    # The y values from the model may become slightly smaller than -1 leading to negative
    # intensity values. This results in bright flashes on the LED
    # To avoid this spurious effect, we make sure that the intensity is always bigger or equal zero    
    if intens < 0:
        intens = 0
        
    # print(intens)
    neopixel[0] = (0,0,intens)
    neopixel.write()
    
def led_off():
    neopixel[0] = (0,0,0)
    neopixel.write()
    
# check if  the hardware definition file is already loaded
try:
    from hw_esp32_s3_fh4r2 import *
except:
    print("Please make sure hw_esp32_s3_fh4r2.py has been uploaded to /lib")
    sys.exit()

# NEOPIXEL and NO_OF_NEOPIXELS is defined in the
# hardware definition file hw_esp32_s3_fh4r2.py

neopixel = NeoPixel(Pin(NEOPIXEL),NO_OF_NEOPIXELS)
maxIntensity = 100  # the NeoPixel is very bright, therefore we limit the light intensity

hello_world_model = bytearray(2488)

model_file = io.open('/models/hello_world_model.tflite', 'rb')
model_file.readinto(hello_world_model)
model_file.close()

interp = microlite.interpreter(hello_world_model,2048, input_callback, output_callback)

print ("time step,y")

try:
    while True:
        counter = 0
        for c in range(steps):
            interp.invoke()
            counter = counter + 1
        
except KeyboardInterrupt:
    led_off()
