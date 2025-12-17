#!/bin/sh
# runs the hello world model on the ESP32 and saves the results onto the file
# file sin.txt
# U. Raich April 2025
# This script is part of a course on tinyML at the University of Cape Coast
# It is released under the MIT license

ampy run hello_world.py | tee sin.txt 
sed -i '1,2d' sin.txt  # remove the first 2 lines, which are just text
sed -i 's/,/ /g' sin.txt # replace all commas by blanks
