# test the person detection model using test images
# Copyright (c) U. Raich, Dec. 2025
# This program is part of the TinyML course at the
# University of Cape Coast,Ghana
# It is released under the MIT license

import microlite

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
    print ("'not a person' = %d, 'person' = %d" % (not_a_person, person))
    
print("person detection test program using test images")
print("read the model")
person_detection_model_file = open ('models/person_detect_model.tflite', 'rb')
person_detection_model = bytearray (300568)
person_detection_model_file.readinto(person_detection_model)
person_detection_model_file.close()
print("Create the interpreter")
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
