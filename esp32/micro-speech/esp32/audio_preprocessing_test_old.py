# audio_preprocessing_test.py: Read a time signal (wav file) from the file system
# and pre-process it, converting it into a spectrogram.
# Write this spectrogram onto a file for transfer to the PC and inspection
# Copyright (c) U. Raich, Dec, 2023
# This program is part of the TinyML course at the
# University of Cape Coast, Ghana
# It is released under the MIT license

from ulab import numpy as np
import micro_speech
import microlite

def decode_wav_header(audio_buffer):
    print("-------------------------------------------------------------------------")
    print("Show the wav header information")
    print("-------------------------------------------------------------------------")
    
    riff = audio_buffer[:4].decode()
    print("File type: {}".format(riff))

    file_size = audio_buffer[7] << 24 | audio_buffer[6] << 16 | audio_buffer[5] << 8 | audio_buffer[4] 
    print("File size: 0x{:d}".format(file_size))

    audio_type = audio_buffer[8:12].decode()
    print("Audio type: {}".format(audio_type))

    format_marker = audio_buffer[12:15].decode()
    print("Format marker: {}".format(format_marker))

    data_length = audio_buffer[17] << 8 | audio_buffer[16]
    print("Data length in bits: {:d}".format(data_length))

    type_format = audio_buffer[21] << 8 | audio_buffer[20]
    if type_format == 1:
        print("PCM - 2 byte integer")
    else:
        print("Unknown format: {d}".format(type_format))

    no_of_channels = audio_buffer[23] << 8 | audio_buffer[22]
    print("No of channels: {:d}".format(no_of_channels))

    sample_rate = audio_buffer[27] << 24 | audio_buffer[26] << 16 | audio_buffer[25] << 8 | audio_buffer[24]
    print("Sample rate: {:d} Hz".format(sample_rate))

    s_rate_bps_ch = audio_buffer[31] << 24 | audio_buffer[30] << 16 | audio_buffer[29] << 8 | audio_buffer[28]
    print("(Sample rate * Bits per sample * Channels)/8: {:d}".format(s_rate_bps_ch))

    bts_ch = audio_buffer[35] << 8 | audio_buffer[34]
    print("(Bits per sample * channels)/8: {:d}".format(bts_ch))

    bits_per_sample = audio_buffer[35] << 8 | audio_buffer[34]
    print("Bits per sample: {:d}".format(bits_per_sample))

    data_section = audio_buffer[36:40].decode()
    print("Start of data section: {}".format(data_section))

    data_section_length = audio_buffer[43] << 24 | audio_buffer[42] << 16 | audio_buffer[41] << 8 | audio_buffer[40]
    print("Length of data section: {:d}".format(data_section_length))
    return sample_rate

# read the wav file

f = open("audio/yes-example.wav","rb")
audio_data = f.read()
f.close()

sample_rate = decode_wav_header(audio_data)

audio_data = audio_data[44:]
print("\nLength of audio data: {:d}".format(len(audio_data)))
                                            
# convert the int8 data info int16 (we have 16 bit samples)
trailing_10ms = np.zeros(160, dtype=np.int16)
audio_samples = np.frombuffer(audio_data,dtype=np.int16)

featureData = micro_speech.FeatureData()
micro_speech.segmentAudio(featureData,audio_samples,trailing_10ms)
print("Slices: ")
print(featureData.slices)
print("Total number of slices: {:d}",featureData.totalSlices)

f = open("/audio/yes_spectrogram.txt","w")
featureData.writeSpectrogramValues("yes",f)
f.close()

# print("Reading the model into memory")
# micro_speech_model = bytearray(18712)
# model_file = open('models/micro-speech-model.tflite', 'rb')
# model_file.readinto(micro_speech_model)
# model_file.close()
