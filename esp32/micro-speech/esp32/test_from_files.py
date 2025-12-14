#
# For microspeech in unix we need to use a wav sample to invoke the tensorflow model
import micro_speech
from ulab import numpy as np
import microlite

micro_speech_model = bytearray(18712)
print("Reading the micro-speech model")
model_file = open('models/micro_speech_model.tflite', 'rb')
model_file.readinto(micro_speech_model)
model_file.close()
print("model successfully read")

currentFeatureData = None

def input_callback (microlite_interpreter):

    # print ("input callback")
    # can't print the tensor directly because it is not an mp_obj_t
    # we probably need to define a container object that will hold the TfLiteTensor pointer
    # we may be able to put the pointer directly as a field in the interpreter class
    # print (input_tensor)

    inputTensor = microlite_interpreter.getInputTensor(0)

    currentFeatureData.setInputTensorValues(inputTensor)

    

kSilenceIndex = 0
kNoiseIndex = 1
kYesIndex = 2
kNoIndex = 3

resultLabel = {}

resultLabel[0] = "Silence"
resultLabel[1] = "Noise"
resultLabel[2] = "Yes"
resultLabel[3] = "No"

inferenceResult = {}

def maxIndex ():

    maxValue = 0
    maxIndex = 0

    for index in range (4):
        value = inferenceResult[index]

        if (value > maxValue):
            maxValue = value
            maxIndex = index

    print ("maxIndex=%d,maxValue=%d" %(maxIndex, maxValue))

    return maxIndex

def output_callback (microlite_interpreter):
    # print ("output callback")

    outputTensor = microlite_interpreter.getOutputTensor(0)

    # we expect there to be a category

    for index in range (4):
        result = outputTensor.getValue(index)
        print ("results at %d = result = %d" % (index, result))
        inferenceResult[index] = result

print("Configuring the audio frontend")
af = microlite.audio_frontend()
af.configure()

# read the wav files for yes and no
f = open("audio/no_1000ms.wav","rb")
no_1000ms_array = f.read()
f.close()
no_1000ms_array = np.frombuffer(no_1000ms_array[44:],dtype=np.int16)

f = open("audio/yes_1000ms.wav","rb")
yes_1000ms_array = f.read()
f.close()
yes_1000ms_array = np.frombuffer(yes_1000ms_array[44:],dtype=np.int16)

# read the wav files for noise and silence
f = open("audio/noise_1000ms.wav","rb")
noise_1000ms_array = f.read()
f.close()
noise_1000ms_array = np.frombuffer(noise_1000ms_array[44:],dtype=np.int16)

f = open("audio/silence_1000ms.wav","rb")
silence_1000ms_array = f.read()
f.close()
silence_1000ms_array = np.frombuffer(silence_1000ms_array[44:],dtype=np.int16)

interp = microlite.interpreter(micro_speech_model,20480, input_callback, output_callback)

no_pcm_input = no_1000ms_array
print ("Process 'No' input of length = %d" % (len (no_pcm_input)))
noFeatureData = micro_speech.FeatureData()
trailing_10ms = np.zeros(160, dtype=np.int16)
trailing_10ms = micro_speech.segmentAudio(noFeatureData, no_pcm_input, trailing_10ms)
currentFeatureData = noFeatureData

interp.invoke()
foundIndex = maxIndex()
if foundIndex != kNoIndex:
    raise ValueError("Error: Expected inference to match the 1 second no sample to no.")

print (resultLabel[foundIndex])

yes_pcm_input = yes_1000ms_array
print ("\nProcess 'Yes' input of length = %d" % (len (yes_pcm_input)))
yesFeatureData = micro_speech.FeatureData()
trailing_10ms = np.zeros(160, dtype=np.int16)

micro_speech.segmentAudio(yesFeatureData, yes_pcm_input, trailing_10ms)
currentFeatureData = yesFeatureData

interp.invoke()
foundIndex = maxIndex()

if foundIndex != kYesIndex:
    raise ValueError("Error: Expected inference to match the 1 second yes sample to yes.")

print (resultLabel[foundIndex])

noise_pcm_input = noise_1000ms_array
print ("\nProcess 'Noise' input of length = %d" % (len (noise_pcm_input)))
noiseFeatureData = micro_speech.FeatureData()
trailing_10ms = np.zeros(160, dtype=np.int16)

micro_speech.segmentAudio(noiseFeatureData, noise_pcm_input, trailing_10ms)
currentFeatureData = noiseFeatureData

interp.invoke()
foundIndex = maxIndex()

if foundIndex != kNoiseIndex:
    raise ValueError("Error: Expected inference to match the 1 second noise sample to noise.")

print (resultLabel[foundIndex])

silence_pcm_input = silence_1000ms_array
print ("\nProcess 'Silence' input of length = %d" % (len (silence_pcm_input)))
silenceFeatureData = micro_speech.FeatureData()
trailing_10ms = np.zeros(160, dtype=np.int16)

micro_speech.segmentAudio(silenceFeatureData, silence_pcm_input, trailing_10ms)
currentFeatureData = silenceFeatureData

interp.invoke()
foundIndex = maxIndex()

if foundIndex != kSilenceIndex:
    raise ValueError("Error: Expected inference to match the 1 second silence sample to silence.")

print (resultLabel[foundIndex])

while True:
    pass
