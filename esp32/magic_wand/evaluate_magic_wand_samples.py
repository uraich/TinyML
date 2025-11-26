# evaluate_magic_wand_samples.py: Uses test  data extracted from the png files
# generated when training the model with data from
# https://github.com/petewarden/magic_wand_digit_data

import microlite
from ulab import numpy as np
import sys

# mode = 1

# The test sample consists or 32x32 rgb values
test_image = bytearray(32*32*3)

def input_callback (microlite_interpreter):
    
    inputTensor = microlite_interpreter.getInputTensor(0)
    
    for i in range (0, len(test_image)):
        inputTensor.setValue(i, test_image[i])

    print(inputTensor)
    print ("setup %d bytes on the inputTensor." % (len(test_image)))

def output_callback (microlite_interpreter):

    outputTensor = microlite_interpreter.getOutputTensor(0)

    for i in range(10):
        print(outputTensor.getValue(i),end=", ")
    print("")


print("Reading model file models/magic_wand_model_quant.tflite")
magic_wand_model_file = open ('models/magic_wand_model_quant.tflite', 'rb')

magic_wand_model = bytearray (31304)

magic_wand_model_file.readinto(magic_wand_model)
if len(magic_wand_model) != 31304:
    print("Reading the model failed")
else:
    print("Model succesfully read")        
magic_wand_model_file.close()

interp = microlite.interpreter(magic_wand_model,150*1024, input_callback, output_callback)

print("Classify Strokes")

for i in range(10):
    filename = "samples/{:d}.bin".format(i)
    print("Reading sample file: " + filename)
    test_image_file = open (filename, 'rb')
    test_image_file.readinto(test_image)
    test_image_file.close()
    print(test_image[:10])
    interp.invoke()

try:
    while True:
        pass
except KeyboardInterrupt:
    sys.exit()
