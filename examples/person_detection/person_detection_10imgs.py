# person_detection_10imgs.py: This is the person_detection program ported from Arduino SDK to
# MicroPython
# Copyright (c) U.Raich
# The program is part of the TinyML course at the University of Cape Coast, Ghana
# It is released under the MIT license

import microlite

mode = 1
test_image = bytearray(9612)

def input_callback (microlite_interpreter):    
    inputTensor = microlite_interpreter.getInputTensor(0)
    for i in range (0, len(test_image)):
        inputTensor.setValue(i, (test_image[i] ^ 0x80))    
    print ("setup %d bytes on the inputTensor." % (len(test_image)))

def output_callback (microlite_interpreter):
    outputTensor = microlite_interpreter.getOutputTensor(0)
    not_a_person = outputTensor.getValue(0)
    person = outputTensor.getValue(1)
    print ("'not a person' = %d, 'person' = %d" % (not_a_person, person))
    prob_person = outputTensor.quantizeInt8ToFloat(person)
    prob_no_person = outputTensor.quantizeInt8ToFloat(not_a_person)
    print("'not a person' = %5.2f, 'person' = %5.2f" % (prob_person,prob_no_person))
    results.append((person,not_a_person,int(prob_person*100+0.5),int(prob_no_person*100+0.5)))
    
person_detection_model_file = open ('models/person_detect_model.tflite', 'rb')
person_detection_model = bytearray (300568)

person_detection_model_file.readinto(person_detection_model)
person_detection_model_file.close()

interp = microlite.interpreter(person_detection_model,136*1024, input_callback, output_callback)
results = []
img_shows=["Thorvalds","dog","person","monkey","di Caprio","cat","person with smart phone",
           "Louis XVI","lady","lady"]

for img in range(10):
    print("Classify Image {:d}".format(img))
    filename = "images/image{:d}.dat".format(img)
    test_image_file = open (filename, 'rb')
    test_image_file.readinto(test_image)
    test_image_file.close()
    interp.invoke()

# print the result in form of a table
print("The results of the person detection for the 10 test images from the esp-idf version of the demo")
print("image no, person score, no person score, probability person, probability no person, real image content")
for i in range(10):
    print("   {:4d}       {:4d}         {:4d}               {:3d}%                 {:3d}%                {:s}".format(
        i,results[i][0],results[i][1],results[i][2],results[i][3],img_shows[i]))
