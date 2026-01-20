# magic_wand_ble_led_from_file.py: Reads a json file with stroke data for each digit
# Rasterized the stroke and prints it.
# This program tests the rasterization algorithm
# Copyright (c) U. Raich Jan 2026
# This program is part of the TinyML course at the
# University of Cape Coast, Ghana
# It is released under the MIT license

import sys
from micropython import const
import json, math
from time import sleep_ms

# gets the stroke points for a particular digit

def findStroke(digit_no):
    for i in range(10):
        if strokes["strokes"][i]["label"] == str(digit_no):
            print("Stroke {:d} found!".format(digit_no))
    return strokes["strokes"][digit_no]["strokePoints"]

def toFloatArray(strokePoints):
    # takes stroke points in form of dictionaries:
    # {"x": "x_value","y": "y_value"}
    # and converts them into a list of float values of the form:
    # x0_value,y0_value,x1_value,y1_value ...
    pointArray = []
    for i in range(len(strokePoints)):
        pointArray.append(float(strokePoints[i]["x"]))
        pointArray.append(float(strokePoints[i]["y"]))
    return pointArray
    
#rasterizes the stroke

FIXED_POINT = const(256)
RASTER_WIDTH = const(32)
RASTER_HEIGHT = const(32)
RASTER_CHANNELS = const(3)
RANGE_X = const(0.6)
RANGE_Y = const(0.6)

def mul_fp(a, b):
    return (a * b) / FIXED_POINT

def div_fp(a, b):
    if b == 0:
        b = 1
    return (a * FIXED_POINT) / b

def float_to_fp(a):
    # print("float_to_fp: type(a):",type(a))
    return math.floor(a * FIXED_POINT)

def norm_to_coord_fp(a, range_fp, half_size_fp):
    a_fp = float_to_fp(a)
    norm_fp = div_fp(a_fp, range_fp)
    return mul_fp(norm_fp, half_size_fp) + half_size_fp

def round_fp_to_int(a):
    return math.floor((a + (FIXED_POINT / 2)) / FIXED_POINT)

def gate(a, min, max):
    if a < min:
        return min
    elif a > max:
        return max
    else:
        return a

def rasterizeStroke(stroke_points, x_range, y_range, width, height):
    num_channels = 3
    buffer_byte_count = height * width * num_channels
    buffer = bytearray(buffer_byte_count)

    width_fp = width * FIXED_POINT
    height_fp = height * FIXED_POINT
    half_width_fp = width_fp / 2
    half_height_fp = height_fp / 2
    x_range_fp = float_to_fp(x_range)
    y_range_fp = float_to_fp(y_range)
    
    t_inc_fp = FIXED_POINT / (len(stroke_points)//2)
    
    one_half_fp = (FIXED_POINT / 2)

    # Go through all the stroke points and extract the start x,y, end x,y and the distance in x and y
    # The start point is the point at the current point index, end point is the next point
    for point_index in range(len(stroke_points)//2 - 2):
        start_point_x = stroke_points[2*point_index]
        start_point_y = stroke_points[2*point_index + 1]
        end_point_x = stroke_points[2*point_index + 2]
        end_point_y = stroke_points[2*point_index + 3]
        start_x_fp = norm_to_coord_fp(start_point_x, x_range_fp, half_width_fp)
        start_y_fp = norm_to_coord_fp(-start_point_y, y_range_fp, half_height_fp)
        end_x_fp = norm_to_coord_fp(end_point_x, x_range_fp, half_width_fp)
        end_y_fp = norm_to_coord_fp(-end_point_y, y_range_fp, half_height_fp)
        delta_x_fp = end_x_fp - start_x_fp
        delta_y_fp = end_y_fp - start_y_fp
        t_fp = point_index * t_inc_fp
        # if point_index == 0:
            # print("start_point x: {:5.3f}, y: {:5.3f}, endpoint x: {:5.3f}, y: {:5.3f}".format(
            # start_x_fp,start_y_fp,end_x_fp,end_y_fp))
        if t_fp < one_half_fp:
            local_t_fp = div_fp(t_fp, one_half_fp)
            one_minus_t_fp = FIXED_POINT - local_t_fp
            red = round_fp_to_int(one_minus_t_fp * 255)
            green = round_fp_to_int(local_t_fp * 255)
            blue = 0
        else:
            local_t_fp = div_fp(t_fp - one_half_fp, one_half_fp)
            one_minus_t_fp = FIXED_POINT - local_t_fp
            red = 0
            green = round_fp_to_int(one_minus_t_fp * 255)
            blue = round_fp_to_int(local_t_fp * 255)
        
        red = gate(red, 0, 255)
        green = gate(green, 0, 255)
        blue = gate(blue, 0, 255)

        # if (point_index == 0):
        #     print("red,green,blue: ",red, green, blue)

        if abs(delta_x_fp) > abs(delta_y_fp):
            line_length = abs(round_fp_to_int(delta_x_fp))
            if delta_x_fp > 0:
                x_inc_fp = 1 * FIXED_POINT
                y_inc_fp = div_fp(delta_y_fp, delta_x_fp)
            else:
                x_inc_fp = -1 * FIXED_POINT
                y_inc_fp = -div_fp(delta_y_fp, delta_x_fp)
        else:
            line_length = abs(round_fp_to_int(delta_y_fp))
            if delta_y_fp > 0:
                y_inc_fp = 1 * FIXED_POINT
                x_inc_fp = div_fp(delta_x_fp, delta_y_fp)
            else:
                y_inc_fp = -1 * FIXED_POINT
                x_inc_fp = -div_fp(delta_x_fp, delta_y_fp)
          
        for i in range(line_length + 1):
            x_fp = start_x_fp + (i * x_inc_fp)
            y_fp = start_y_fp + (i * y_inc_fp)
            x = round_fp_to_int(x_fp)
            y = round_fp_to_int(y_fp)
            if (x < 0) or (x >= width) or (y < 0) or (y >= height):
                continue
            buffer_index = (y * width * num_channels) + (x * num_channels)
            # if point_index == 0:
            #     print("buffer index: ",buffer_index," length of buffer: ",len(buffer))
            #     print("Color value at buffer index: ({:d},{:d},{:d})".format(red,green,blue))
            buffer[buffer_index + 0] = red
            buffer[buffer_index + 1] = green
            buffer[buffer_index + 2] = blue

    return buffer
          
# Read the json file with 10 digit example strokes
try:
    jsonFile = open("strokes/digits.json","r")
    strokes = json.load(jsonFile)
except:
    print("Please make sure that digits.json has been uploaded to /strokes")
    sys.exit()
    
# get at the stroke points

for digit in range(10):
    strokePoints = findStroke(digit)
    pointArray = toFloatArray(strokePoints)
    # print("x0: {:5.3f}, y0: {:5.3f}".format(pointArray[0],pointArray[1]))
    rasterBuffer = rasterizeStroke(pointArray, RANGE_X, RANGE_Y, RASTER_WIDTH,RASTER_HEIGHT)
    '''
    print("Colors:")
    for i in range(4):
        for j in range(3):
            print("({:d},{:d},{:d}), ".format(rasterBuffer[3*i*4 + 3*j],
                                              rasterBuffer[3*i*4 + 3*j+1],
                                              rasterBuffer[3*i*4 + 3*j+2]),end="")
            
            print("({:d},{:d},{:d})".format(rasterBuffer[3*i*4 + 3*3],
                                            rasterBuffer[3*i*4 + 3*3+1],
                                            rasterBuffer[3*i*4 + 3*3+2]))
    '''                                        
                                              
    for y in range(RASTER_HEIGHT):
        line = ""
        for x in range(RASTER_WIDTH):
            pixel_index = y * RASTER_WIDTH * RASTER_CHANNELS + x * RASTER_CHANNELS
            red = rasterBuffer[pixel_index]
            green = rasterBuffer[pixel_index+1]
            blue = rasterBuffer[pixel_index+2]

            if red > 0 or green > 0 or blue > 0:
                line += '#'
            else:
                line +='.'
        print(line)
    sleep_ms(3000)
