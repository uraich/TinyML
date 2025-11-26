import microlite
import sys

mode = 1

test_image = bytearray(784)

def input_callback (microlite_interpreter):
    
    inputTensor = microlite_interpreter.getInputTensor(0)

    for i in range (0, len(test_image)):
        inputTensor.setValue(i, test_image[i])
    
    print ("setup %d bytes on the inputTensor." % (len(test_image)))

def output_callback (microlite_interpreter):

    outputTensor = microlite_interpreter.getOutputTensor(0)

    for i in range(10):
        print(outputTensor.getValue(i),end=", ")
    print("")

mnist_model_file = open ('models/number_model_quant.tflite', 'rb')

mnist_model = bytearray (13952)

mnist_model_file.readinto(mnist_model)
if len(mnist_model) != 13952:
    print("Reading the model failed")
mnist_model_file.close()

interp = microlite.interpreter(mnist_model,50*1024, input_callback, output_callback)

print("Classify Numbers")

test_image_file = open ('samples/sample0.bin', 'rb')

test_image_file.readinto(test_image)

test_image_file.close()

interp.invoke()

print("Classify numbers")

test_image_file = open ('samples/sample1.bin', 'rb')

test_image_file.readinto(test_image)

test_image_file.close()

interp.invoke()

try:
    while True:
        pass
except KeyboardInterrupt:
    sys.exit()
