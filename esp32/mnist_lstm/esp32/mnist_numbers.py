# microlite is the tensorflow library for the micro-controller
import microlite
import sys

# a byte array containing all the 28x28 pixels of the digit image
test_image = bytearray(784)

# find the index of the biggest number in the list
def max(list):
    max = -128
    index = 0
    for i in range(len(list)):
        if max < list[i]:
            max = list[i]
            index = i
    return index

# this function is called when the interpreter needs new input data
def input_callback (microlite_interpreter):

    inputTensor = microlite_interpreter.getInputTensor(0)

    for i in range (0, len(test_image)):
        inputTensor.setValue(i, test_image[i])
    
    # print ("setup %d bytes on the inputTensor." % (len(test_image)))

# the interpreter outputs the output tensor with the results
# these are 10 probabilities for the 10 digits coded in int8 format
def output_callback (microlite_interpreter):
    res   = [None]*10
    probs = [None]*10
    outputTensor = microlite_interpreter.getOutputTensor(0)

    for i in range(10):
        res[i] = outputTensor.getValue(i)
    results[sample] = res
# here we dequantize the output back into a floating point value in the range of 0..1
    for i in range(10):
        probs[i] = outputTensor.quantizeInt8ToFloat(outputTensor.getValue(i))
    probabilities[sample] = probs
    
# read the trained and quantized model
mnist_model_file = open ('models/number_model_quant.tflite', 'rb')

mnist_model = bytearray (13952)

mnist_model_file.readinto(mnist_model)
if len(mnist_model) != 13952:
    print("Reading the model failed")
mnist_model_file.close()

# now we instantiate the Tensorflow lite micro interpreter
interp = microlite.interpreter(mnist_model,50*1024, input_callback, output_callback)

results = [None]*10
probabilities = [None]*10

# we read the sample file for each digit 0..9 and invoke the interpreter on these data
for sample in range(10):
    sample_filename = "samples/sample{:d}.bin".format(sample)
    test_image_file = open (sample_filename, 'rb')
    
    test_image_file.readinto(test_image)
    test_image_file.close()
    interp.invoke()

print("Raw results:")
for i in range(10):
    for j in range(10):
        print("{:4d}".format(results[i][j]),end=", ")
    print("")
    
print("Probabilities:")
for i in range(10):
    for j in range(10):
        print("{:6.4f}".format(probabilities[i][j]),end=", ")
    print("")

print("digits found: ",end="")
for digit in range(9):
    print("{:d}, ".format(max(results[digit])),end="")
print("{:d}".format(max(results[digit+1])))

print("added probabilities: ")
for i in range(9):
    sum = 0
    for j in range(10):
        sum += probabilities[i][j]
    print("{:6.4f}, ".format(sum), end="")
sum = 0
for j in range(10):
    sum += probabilities[i+1][j]
print("{:6.4f}".format(sum))


try:
    while True:
        pass
except KeyboardInterrupt:
    sys.exit()
