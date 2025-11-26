# Decode the wav file header
# Copyright (c) U.Raich Nov 2023
# This program is part of the course of TinyML at the
# University of Cape Coast, Ghana
# It is released under the MIT license

def decode_wav_header(filename):
    try:
        f = open(f,'rb')
    except:
        print("Cannot open {}".format(filename))
        return
    audio_buffer = f.read()
    f.close()

    print("Show the wav header information")
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
