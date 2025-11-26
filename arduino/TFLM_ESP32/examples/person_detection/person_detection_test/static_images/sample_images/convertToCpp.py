#!/usr/bin/python3
import sys
if len(sys.argv) != 2:
    print("Usage: {} name of binary file".format(sys.argv[0]))
    sys.exit()
# read the image file

image_file = sys.argv[1]
# read the file
f = open(image_file,"rb")
bin_image = bytearray()
bin_image = f.read()
f.close

cc_filename = image_file + '.cpp'
h_filename = image_file + '.h'

# Create the .cc file
cc_file = open(cc_filename,"w")
cc_file.write("#include <cstdint>\n\n")
cc_file.write('#include "' + h_filename  + '"\n\n')
cc_file.write("alignas(16) const unsigned char g_" + image_file + "_data[] = {\n")
for pixel in bin_image[:len(bin_image)-1]:
    cc_file.write("0x{:02x},".format(pixel))
cc_file.write("0x{:02x}".format(bin_image[len(bin_image)-1]) + "};\n")
cc_file.write("const unsigned int g_" + image_file + "_data_size=" + str(len(bin_image)) + ";\n")
cc_file.close()

# Create the .h file
h_file = open(h_filename,"w")
h_file.write("#include <cstdint>\n\n")
h_file.write("extern const unsigned int g_" + image_file + "_data_size;\n")
h_file.write("extern const unsigned char g_" + image_file + "_data[];\n")
h_file.close()
