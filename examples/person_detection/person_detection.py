# person_detection.py: This is the person_detection program ported from the person_detection
# demo of the tflite-micro examples folder to MicroPython
# Copyright (c) U.Raich
# The program is part of the TinyML course at the University of Cape Coast, Ghana
# It is released under the MIT license

import microlite

mode = 1
test_image = bytearray(9612)

def input_callback (microlite_interpreter):    
    inputTensor = microlite_interpreter.getInputTensor(0)
    for i in range (0, len(test_image)):
        inputTensor.setValue(i, test_image[i])    
    print ("setup %d bytes on the inputTensor." % (len(test_image)))

def output_callback (microlite_interpreter):
    outputTensor = microlite_interpreter.getOutputTensor(0)
    not_a_person = outputTensor.getValue(0)
    person = outputTensor.getValue(1)
    print ("Scores: person = {:4d}, not a person = {:4d}".format(person, not_a_person))
    prob_person = outputTensor.quantizeInt8ToFloat(person)
    prob_no_person = outputTensor.quantizeInt8ToFloat(not_a_person)
    print("person = {:3d}%, not a person' = {:3d}%" .format(int(prob_person*100 + 0.5),
                                                     int(prob_no_person*100 + 0.5)))

person_detection_model_file = open ('models/person_detect_model.tflite', 'rb')
person_detection_model = bytearray (300568)

person_detection_model_file.readinto(person_detection_model)
person_detection_model_file.close()

interp = microlite.interpreter(person_detection_model,136*1024, input_callback, output_callback)

print("Classify No Person Image")
no_person_test_image_file = open ('images/no_person.dat', 'rb')
no_person_test_image_file.readinto(test_image)
no_person_test_image_file.close()
interp.invoke()

print("Classify Person Image")
no_person_test_image_file = open ('images/person.dat', 'rb')
no_person_test_image_file.readinto(test_image)
no_person_test_image_file.close()
interp.invoke()
