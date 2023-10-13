# add_numbers.py
# Demonstrates a simple TF model with resource variables adding 4 numbers
# Coypright U. Raich 13.Oct. 2023
# This program is part of a course on TinyML at the
# University of Cape Coast, Ghana
# It is released under the MIT license

import microlite
from ulab import numpy as np
import sys

mode = 1

numbersToAdd=[1.6,2.4,3.7,2.5]

def input_callback (microlite_interpreter):
    
    for i in range(4):
        inputTensor = microlite_interpreter.getInputTensor(i)
        inputTensor.setValue(0,numbersToAdd[i])
        if i == 3:
            print("{:4.2f} = ".format(numbersToAdd[i]),end="")
        else:
            print("{:4.2f} + ".format(numbersToAdd[i]),end="")            
        
def output_callback (microlite_interpreter):
    outputTensor = microlite_interpreter.getOutputTensor(0)
    # print(outputTensor)
    print("{:4.2f}".format(outputTensor.getValue(0)))
          
mnist_model_file = open ('models/add.tflite', 'rb')

mnist_model = bytearray (1284)

mnist_model_file.readinto(mnist_model)
if len(mnist_model) != 1284:
    print("Reading the model failed")
mnist_model_file.close()

interp = microlite.interpreter(mnist_model,2*1024, input_callback, output_callback)

print("Add four numbers")
interp.invoke()

try:
    while True:
        pass
except KeyboardInterrupt:
    sys.exit()
