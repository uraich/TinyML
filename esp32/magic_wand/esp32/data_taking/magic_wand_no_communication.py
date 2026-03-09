# magic_wand_no_communication.py: Run the magic wand algorithm and print
# the result as a 32x32 pixel array
# Ported from magic_wand.iso
# Makes use of numpy maths
# This program saves strokes into a file named /data/stroke_data.txt, which can be read back
# with the jupyter notebook analyse_stroke_v2.ipynb
# Copyright (c) U. Raich, March 2026
# This program is part of the TinyML course at the University of Cape Coast, Ghana
# It is released under the MIT license
#

from lsm6ds3_imu import LSM6DS3_IMU
from micropython import const
from time import sleep_ms
import math
import sys
from ulab import numpy as np

class MagicWand(object):
    # stroke state
    eWaiting = 0
    eDrawing = 1
    eDone    = 2

    FIXED_POINT = const(256)
    RASTER_WIDTH = const(32)
    RASTER_HEIGHT = const(32)
    RASTER_CHANNELS = const(3)
    RANGE_X = const(0.6)
    RANGE_Y = const(0.6)
    MEAS_BUFFER_SIZE = const(600)
    
    def __init__(self,debug=False):
        self.debug = debug
        self.stroke_transmit_stride = const(2)
        self.stroke_transmit_max_length = const(160)
        self.strokePoints = np.empty((self.stroke_transmit_max_length,2),dtype=np.int8)
        self.stroke_max_length = self.stroke_transmit_max_length * self.stroke_transmit_stride
        self.data_index = 0
        self.data_length = MEAS_BUFFER_SIZE
        self.acceleration_data = np.empty((MEAS_BUFFER_SIZE,3),dtype=np.float)        
        self.gyroscope_data = np.empty((MEAS_BUFFER_SIZE,3),dtype=np.float)
        self.orientation_data = np.empty((MEAS_BUFFER_SIZE,3),dtype=np.float)
        self.stroke_struct_buffer = bytearray(self.stroke_transmit_stride*self.stroke_transmit_max_length)

        print("acceleration byte count : {:d}".format(self.acceleration_data.size))

        # for debugging only:
        self.velocity = np.empty((MEAS_BUFFER_SIZE,3),dtype=np.float)
        self.position = np.empty((MEAS_BUFFER_SIZE,3),dtype=np.float)
        self.gyroscope_drift = np.empty((MEAS_BUFFER_SIZE,3),dtype=np.float)
        self.corrected_gyroscope_data = np.empty((MEAS_BUFFER_SIZE,3),dtype=np.float)
        self.acc_minus_gravity = np.empty((MEAS_BUFFER_SIZE,3),dtype=np.float)
        self.gravity = np.empty((MEAS_BUFFER_SIZE,3),dtype=np.float)
        
        self.current_velocity = np.empty((3,),dtype=np.float)
        self.current_position = np.empty((3,),dtype=np.float)
        self.current_gyroscope_drift = np.array([0, 0, 0]) # measured through a calibration procedure
        self.current_gravity = np.array([0, 0, 0])
        self.raster_buffer = np.empty((RASTER_WIDTH*RASTER_HEIGHT*RASTER_CHANNELS,),dtype=np.int8)
        print("raster  buffer size: {:d}".format(self.raster_buffer.size))
        
        self.moving_sample_count = const(50)
        self.mag_squared = np.empty((self.moving_sample_count,), dtype=np.float)
        self.mag_total = 0
        self.moving_total = 0
        self.stroke_state = self.eWaiting
        self.stroke_length = 0
        
    def setup(self):
        if self.debug:
            print("Setup started")
        self.IMU = LSM6DS3_IMU(debug=False)
        self.sample_rate = self.IMU.accelerationSampleRate()
        if self.debug:
            print("sample rate: {:4.1f}".format(self.sample_rate))
        self.SetupIMU()

    def loop(self):
        print("Waiting... ")
        for i in range(1000):
            while not self.IMU.accelerationAndGyroscopeAvailable():
                # print("Waiting for data")
                continue
            noOfSamplesInFifo = self.IMU.noOfSamplesInFifo()
            # print("no of samples in fifo: {:d}".format(noOfSamplesInFifo))
            
            result = self.IMU.readAccelerationAndGyroscope()
            # save the measured gyroscope and accelerometer data in the data arrays
            self.gyroscope_data[self.data_index % self.data_length] = result[0]
            self.acceleration_data[self.data_index % self.data_length] = result[1]
            self.data_index += 1

            self.debug = False
            self.EstimateGyroscopeDrift()
            self.UpdateOrientation()
            self.UpdateStroke()
            
            # for debugging only
            self.corrected_gyroscope_data[self.data_index % self.data_length] = result[0] - self.current_gyroscope_drift
            self.UpdateMoving()

            # accelerator updates
            self.EstimateGravityDirection()
            self.UpdateVelocity()

            if self.done_just_triggered:
                self.rasterizeStroke()
                self.plotStroke()
                
    def SetupIMU(self): 
        self.IMU.setContinuousMode()

    def EstimateGyroscopeDrift(self) :
        if self.debug:
            print("Estimate Gyroscope Drift")
        # print("vel_ampl: {:5.3f}".format(np.linalg.norm(self.current_velocity)))  
        isMoving = np.linalg.norm(self.current_velocity) > 0.1
        if self.debug:
            print("velocity: ",np.linalg.norm(self.current_velocity))
        if isMoving:
            # print("Is moving, amplitude: ",np.linalg.norm(self.current_velocity))
            return 
        samples_to_average = 20
        if samples_to_average >= self.data_index:
            samples_to_average = self.data_index

        if self.debug:
            print("samples_to_average {:d}, data_index: {:d}".format(samples_to_average,
                                                                     self.data_index))
        start_index = (self.data_index + (self.data_length - samples_to_average)) % self.data_length
        if self.debug:
            print("start index: {:d}, data_index: {:d}".format(
                start_index,self.data_index))

        total = np.empty((3,),dtype=np.float)
        for i in range(samples_to_average):
            index = (start_index + i) % self.data_length            
            total += self.gyroscope_data[index]
            
        self.current_gyroscope_drift = total / samples_to_average
        self.gyroscope_drift[(self.data_index -1) % self.data_length] = self.current_gyroscope_drift
        if self.debug:
            print("drift: {:4.3f}, {:4.3f}, {:4.3f}".format(self.current_gyroscope_drift[0],
                                                            self.current_gyroscope_drift[1],
                                                            self.current_gyroscope_drift[2]))
        return

    def EstimateGravityDirection(self):
        # samples_to_average = 100
        samples_to_average = 20

        if samples_to_average >= self.data_index:
            samples_to_average = self.data_index
        else:
            samples_to_average = 20

        start_index = (self.data_index + \
            (self.data_length - samples_to_average)) % self.data_length

        self.debug = False
        if self.debug:
            print("samples to average: {:d}".format(samples_to_average))
            print("acceleration data index: {:d}".format(self.data_index))
            print("start index: {:d}".format(start_index))
            print("samples to average: ",samples_to_average)
        total = np.empty((3,), dtype=np.float)

        for i  in range(samples_to_average):
            index = start_index % self.data_length
            total += self.acceleration_data[index]
        self.current_gravity = total / samples_to_average
       
        if self.debug:
            print("current gravity: {:4.3f}, {:4.3f}, {:4.3f}".format(self.current_gravity[0],
                                                                      self.current_gravity[1],
                                                                      self.current_gravity[2]))
        self.debug = False
        # for debugging only
        self.gravity[(self.data_index -1) % self.data_length] = self.current_gravity
        return
    
    def UpdateVelocity(self):
        # let the system settle
        if self.data_index < 50:
            return
        # print("{:4.3f}, {:4.3f}, {:4.3f}".format(gravity_x,gravity_y,gravity_z))
        index = (self.data_index + (self.data_length - 1)) % self.data_length
        friction_fudge = 0.98
 
        if self.debug:    
            print("index: ",index, "acc entry: ",acceleration[index])
        
        # Try to remove gravity from the raw acceleration values.
        acc_minus_gravity = self.acceleration_data[index] - self.current_gravity
        self.acc_minus_gravity[index] = acc_minus_gravity
        
        # Update velocity based on the normalized acceleration.
        self.current_velocity += acc_minus_gravity
        if self.debug:
            print("current_velocity: ", self.current_velocity)
        
        # Dampen the velocity slightly with a fudge factor to stop it exploding.
        self.current_velocity *= friction_fudge
        
        # for debugging only
        self.velocity[index] = self.current_velocity

        # Update the position estimate based on the velocity.
        self.current_position += self.current_velocity
        
        # for debugging only
        self.position[index] = self.current_position
        
        # self.debug=True
        if self.debug:
            print("current_velocity: {:4.3f}, {:4.3f}, {:4.3f}".format(self.current_velocity[0],
                                                                       self.current_velocity[1],
                                                                       self.current_velocity[2]))
            print("{:4.3f}, {:4.3f}, {:4.3f}".format(self.current_position[0],
                                                     self.current_position[1],
                                                     self.current_position[2]))
    def  UpdateOrientation(self) :
        # wait until the gyroscope drift settles
        if self.data_index < 20:
            return
        # The gyroscope values are in degrees-per-second, so to approximate
        # degrees in the integrated orientation, we need to divide each value
        # by the number of samples each second.
        
        dt = 1.0 / self.sample_rate       
        if self.debug:
            print("Update orientation")

        index = (self.data_index -1) % self.data_length
        # Try to remove sensor errors from the raw gyroscope values.
        # print("current gyroscope drift: ",self.current_gyroscope_drift)
        gyro_minus_drift = np.array(self.gyroscope_data[index]) - self.current_gyroscope_drift
         
        # Convert from degrees-per-second to appropriate units for this
        # time interval.
        gyro_normalized = gyro_minus_drift * dt

        
        # Update orientation based on the gyroscope data.
        previous_index = (index - 1) % self.data_length
        self.orientation_data[index] = self.orientation_data[previous_index] + np.array(gyro_normalized)
        
        if self.debug:
            print("previous orientation: {:d}: {:4.2f},{:4.2f},{:4.2f}".format(previous_index,
                                                                               self.orientation_data[previous_index][0],
                                                                               self.orientation_data[previous_index][1],
                                                                               self.orientation_data[previous_index][2]))
            print("current orientation: {:d}: {:4.2f},{:4.2f},{:4.2f}".format(index,
                                                                              self.orientation_data[index][0],
                                                                              self.orientation_data[index][1],
                                                                              self.orientation_data[index][2]))

    def UpdateMoving(self):
        index = (self.data_index -1) % self.data_length 
        current_orientation = self.orientation_data[index]
        previous_index = (self.data_index -2) % self.data_length        
        previous_orientation = self.orientation_data[previous_index]

        dx = current_orientation[0] - previous_orientation[0]
        dy = current_orientation[1] - previous_orientation[1]
        dz = current_orientation[2] - previous_orientation[2]

        # print("{:4.3f} {:4.3f} {:4.3f}".format(dx,dy,dz)) 
        mag_squared = dx*dx + dy*dy + dz*dz
        mag_index = (self.data_index -1) % self.moving_sample_count
        # remove the last value and add the new one to the total
        self.mag_total = self.mag_total - self.mag_squared[mag_index] + mag_squared
        self.mag_squared[mag_index] = mag_squared

    def IsMoving(self):
        moving_threshold = 10.0
        # if self.mag_total  > moving_threshold:
        #     print("mag_total: ",self.mag_total)
        return self.mag_total > moving_threshold

    def UpdateStroke(self):
        minimum_stroke_length = self.moving_sample_count + 10
        minimum_stroke_size = 0.2

        self.done_just_triggered = False
        # self.debug=True
        if self.debug:
            self.printStrokeState(self.stroke_state)
            # print("new_samples: ",new_samples)
        self.debug = False
        is_moving = self.IsMoving()
        # self.debug = True
        if self.debug:
            if is_moving:
                print("UpdateStroke: is moving")
            else:
                print("UpdateStroke: is not moving")
            
        self.debug = False
        old_state = self.stroke_state
        if old_state == self.eWaiting or old_state == self.eDone:
            if is_moving:
                self.stroke_length = self.moving_sample_count
                self.stroke_state = self.eDrawing
                print("Drawing")
        elif old_state == self.eDrawing:
            if (not is_moving):
                if self.stroke_length > minimum_stroke_length:
                    self.stroke_state = self.eDone
                    print("Done")
                else:
                    # print("Stroke too short: {:5.2f}, waiting".format(self.stroke_length))
                    stroke_length = 0;
                    self.stroke_state = self.eWaiting
  
        if self.stroke_state == self.eWaiting:
           return False
    
        self.stroke_length += 1
        if self.stroke_length > self.stroke_max_length:
            self.stroke_length = self.stroke_max_length
  
        # Only recalculate the full stroke if it's needed.
        # draw_last_point = (i == (new_samples -1)) and (self.stroke_state == self.eDrawing)
        self.done_just_triggered = (old_state != self.eDone) and (self.stroke_state == self.eDone)
        # if (not self.done_just_triggered) or draw_last_point :
        if (not self.done_just_triggered):
            return False

        if self.done_just_triggered:
            print("Done just triggered")
            print("Stroke length: ",self.stroke_length)
            print("data index: ",self.data_index)

        start_index = ((self.data_index + 
                        (self.data_length - self.stroke_length)) % 
                       self.data_length);

        total = np.empty((3,),dtype=np.float)
            
        stroke_file = open("data/stroke_data.txt","w")
        stroke_file.write("stroke_data:\n")
        for j in range(self.stroke_length):
            index = (start_index + j) % self.data_length
            stroke_file.write("{:6.4f}, {:6.4f}, {:6.4f}\n".format(self.orientation_data[index][0],
                                                                 self.orientation_data[index][1],
                                                                 self.orientation_data[index][2]))
            total += self.orientation_data[index] 
        mean = total / self.stroke_length
        
        # This allows to check the algorithm with a jupyter notebook
        stroke_file.write("gravity:\n")
        for j in range(self.stroke_length):
            index = (start_index + j) % self.data_length
            stroke_file.write("{:6.4f}, {:6.4f}, {:6.4f}\n".format(self.gravity[index][0],
                                                                   self.gravity[index][1],
                                                                   self.gravity[index][2]))
            
        # stroke_file.write("{:6.4f}, {:6.4f}, {:6.4f}\n".format(self.current_gravity[0],
        #                                                        self.current_gravity[1],
        #                                                        self.current_gravity[2]))
        stroke_file.close()

        angle_range = 90.0

        # gy = self.current_gravity[1]
        # gz = self.current_gravity[2]
            
        # The orientation of the accelerometer on the ESP32 wand is
        # different from the Arduino Nano 33 BLE sense
        # When held horizontally with the boards facing yourself
        # an up down movement changes y axis
        # a left right movement changes the x axis
        # a forward-backward movement changes the z axis
            
        gy = self.current_gravity[1]
        gz = self.current_gravity[2]

        gmag = math.sqrt((gy * gy) + (gz * gz))
        if gmag < 0.0001:
            gmag = 0.0001
            
        ngy = gy / gmag
        ngz = gz / gmag
                
        xaxisz = -ngz
        xaxisy = -ngy
            
        yaxisz = ngy
        yaxisy = -ngz
    
        self.stroke_transmit_length = self.stroke_length / self.stroke_transmit_stride
        
        for j in range(self.stroke_transmit_length):
            orientation_index = (start_index + j * self.stroke_transmit_stride) % self.data_length

            n = (self.orientation_data[orientation_index] - mean) / angle_range
                
            x_axis = xaxisz * n[2] + xaxisy * n[0] 
            y_axis = yaxisz * n[2] + yaxisy * n[0]    
                
            unchecked_x = round(x_axis * 128.0)
            
            if unchecked_x > 127:
                stored_x = 127
            elif unchecked_x < -128:
                stored_x = -128
            else:
                stored_x = unchecked_x
                    
            unchecked_y = round(y_axis * 128.0)

            if unchecked_y > 127:
                stored_y = 127
            elif unchecked_y < -128:
                stored_y = -128
            else:
                stored_y = unchecked_y
                
            self.strokePoints[j] = [stored_x,stored_y]
            
            self.stroke_struct_buffer[2*j] = stored_x
            self.stroke_struct_buffer[2*j+1] = stored_y
            
            is_first = (j == 0)
            if is_first or x_axis < x_min :
                x_min = x_axis
            if is_first or y_axis < y_min:
                y_min = y_axis;
            if is_first or x_axis > x_max:
                x_max = x_axis
            if is_first or y_axis > y_max:
                y_max = y_axis
                
        # If the stroke is too small, cancel it.
        if self.done_just_triggered:
            x_range = x_max - x_min
            y_range = y_max - y_min
            if x_range < minimum_stroke_size and y_range < minimum_stroke_size: 
                self.done_just_triggered = False
                self.stroke_state = self.eWaiting
                self.stroke_transmit_length = 0
                self.stroke_length = 0
                print("Stroke too small, canceled")          
                print("range: {:4.3f}, {:4.3f}".format(x_range,y_range))
            else:
                print("Stroke ok")
                print(self.strokePoints)
                # for i in range(self.stroke_transmit_length):
                #     print("{:d} {:d}".format(self.strokePoints[i][0],
                #                                  self.strokePoints[i][1]))
                                          
        return
    
    def mul_fp(self, a, b):
        return int((a * b) / FIXED_POINT)

    def div_fp(self, a, b):
        if b == 0:
            b = 1
        return int((a * FIXED_POINT) / b)

    def float_to_fp(self, a):
        # print("float_to_fp: type(a):",type(a))
        return math.floor(a * FIXED_POINT)

    def norm_to_coord_fp(self, a, range_fp, half_size_fp):
        a_fp = self.float_to_fp(a)
        norm_fp = self.div_fp(a_fp, range_fp)
        return self.mul_fp(norm_fp, half_size_fp) + half_size_fp

    def round_fp_to_int(self, a):
        return math.floor((a + (FIXED_POINT / 2)) / FIXED_POINT)

    def gate(self, a, min, max):
        if a < min:
            return min
        elif a > max:
            return max
        else:
            return a

    # def rasterizeStroke(stroke_points, x_range, y_range, width, height):
    def rasterizeStroke(self):
        width = self.RASTER_WIDTH
        height = self.RASTER_HEIGHT
        num_channels = self.RASTER_CHANNELS
        x_range = 0.6
        y_range = 0.6

        buffer_byte_count = height * width * num_channels
        buffer = bytearray(buffer_byte_count)

        width_fp = width * FIXED_POINT
        height_fp = height * FIXED_POINT
        half_width_fp = width_fp // 2
        half_height_fp = height_fp // 2
        x_range_fp = self.float_to_fp(x_range)
        y_range_fp = self.float_to_fp(y_range)
        
        t_inc_fp = FIXED_POINT / (len(self.strokePoints))
        
        one_half_fp = (FIXED_POINT // 2)
        # print(self.strokePoints)
        print(self.strokePoints[0][0])
        print(self.strokePoints[0][1])
        # Go through all the stroke points and extract the start x,y, end x,y and the distance in x and y
        # The start point is the point at the current point index, end point is the next point
        for point_index in range(len(self.strokePoints) - 1):

            '''
            start_point_x = stroke_points[2*point_index]
            start_point_y = stroke_points[2*point_index + 1]
            end_point_x = stroke_points[2*point_index + 2]
            end_point_y = stroke_points[2*point_index + 3]

            start_point_x = self.strokePoints[point_index][0] * FIXED_POINT / 128
            start_point_y = self.strokePoints[point_index][1] * FIXED_POINT / 128
            end_point_x = self.strokePoints[point_index+1][0] * FIXED_POINT / 128
            end_point_y = self.strokePoints[point_index+1][1] * FIXED_POINT / 128
            '''
            start_point_x = self.strokePoints[point_index][0] / 128
            start_point_y = self.strokePoints[point_index][1] / 128
            end_point_x = self.strokePoints[point_index+1][0] / 128
            end_point_y = self.strokePoints[point_index+1][1] / 128
            
            # if point_index < 10:
            #     print("startpoint: ",point_index, start_point_x, start_point_y)
            #     print("x_range_fp, y_range_fp, half_width_fp: ",x_range_fp, y_range_fp, half_width_fp)
                
            start_x_fp = self.norm_to_coord_fp(start_point_x, x_range_fp, half_width_fp)
            start_y_fp = self.norm_to_coord_fp(-start_point_y, y_range_fp, half_height_fp)
            end_x_fp = self.norm_to_coord_fp(end_point_x, x_range_fp, half_width_fp)
            end_y_fp = self.norm_to_coord_fp(-end_point_y, y_range_fp, half_height_fp)          
           
            delta_x_fp = end_x_fp - start_x_fp
            delta_y_fp = end_y_fp - start_y_fp
            t_fp = point_index * t_inc_fp
            
            # if point_index < 10:
            #     print("start_point x: {:d}, y: {:d}, endpoint x: {:d}, y: {:d}".format(
            #     start_x_fp, start_y_fp, end_x_fp, end_y_fp))
            if t_fp < one_half_fp:
                local_t_fp = self.div_fp(t_fp, one_half_fp)
                one_minus_t_fp = FIXED_POINT - local_t_fp
                red = self.round_fp_to_int(one_minus_t_fp * 255)
                green = self.round_fp_to_int(local_t_fp * 255)
                blue = 0
            else:
                local_t_fp = self.div_fp(t_fp - one_half_fp, one_half_fp)
                one_minus_t_fp = FIXED_POINT - local_t_fp
                red = 0
                green = self.round_fp_to_int(one_minus_t_fp * 255)
                blue = self.round_fp_to_int(local_t_fp * 255)
            
            red = self.gate(red, 0, 255)
            green = self.gate(green, 0, 255)
            blue = self.gate(blue, 0, 255)

            # if (point_index < 10):
            #     print("red,green,blue: ",red, green, blue)

            if abs(delta_x_fp) > abs(delta_y_fp):
                line_length = abs(self.round_fp_to_int(delta_x_fp))
                if delta_x_fp > 0:
                    x_inc_fp = 1 * FIXED_POINT
                    y_inc_fp = self.div_fp(delta_y_fp, delta_x_fp)
                else:
                    x_inc_fp = -1 * FIXED_POINT
                    y_inc_fp = -self.div_fp(delta_y_fp, delta_x_fp)
            else:
                line_length = abs(self.round_fp_to_int(delta_y_fp))
                if delta_y_fp > 0:
                    y_inc_fp = 1 * FIXED_POINT
                    x_inc_fp = self.div_fp(delta_x_fp, delta_y_fp)
                else:
                    y_inc_fp = -1 * FIXED_POINT
                    x_inc_fp = -self.div_fp(delta_x_fp, delta_y_fp)

            # print("inc_fp: ",x_inc_fp, y_inc_fp)
            # if (point_index < 10):
            #     print("line length: ",line_length)
                
            for i in range(line_length + 1):
                x_fp = start_x_fp + (i * x_inc_fp)
                y_fp = start_y_fp + (i * y_inc_fp)
                
                x = self.round_fp_to_int(x_fp)
                y = self.round_fp_to_int(y_fp)
                
                # print("x: ",x,", y: ",y)
                if (x < 0) or (x >= width) or (y < 0) or (y >= height):
                    continue
                buffer_index = (y * width * num_channels) + (x * num_channels)
                # if point_index < 10:
                #     print("buffer index: ",buffer_index," length of buffer: ",len(buffer))
                #     print("Color value at buffer index: ({:d},{:d},{:d})".format(red,green,blue))
                self.raster_buffer[buffer_index + 0] = red
                self.raster_buffer[buffer_index + 1] = green
                self.raster_buffer[buffer_index + 2] = blue
        #print(buffer)
        return 

    def plotStroke(self):
        print("plotstroke")
        for y in range(RASTER_HEIGHT):
            line = ""
            for x in range(RASTER_WIDTH):
                pixel_index = y * RASTER_WIDTH * RASTER_CHANNELS + x * RASTER_CHANNELS
                red = self.raster_buffer[pixel_index]
                green = self.raster_buffer[pixel_index+1]
                blue = self.raster_buffer[pixel_index+2]

                if red > 0 or green > 0 or blue > 0:
                    line += '#'
                else:
                    line +='.'
            print(line)
        
magic_wand = MagicWand(debug=True)
magic_wand.setup()
magic_wand.IMU.printRegisterSettings()
magic_wand.IMU.printFifoRegisterSettings()
magic_wand.loop()

'''
for i in range(100):                        
    print("acc_x={:5.3f}, acc_y={:5.3f}, acc_z={:5.3f}".format(
        magic_wand.acceleration_data[i][0],
        magic_wand.acceleration_data[i][1],
        magic_wand.acceleration_data[i][2]))
sleep_ms(1000)
for i in range(100): 
    print("gyro_x={:5.3f}, gyro_y={:5.3f}, gyro_z={:5.3f}".format(
        magic_wand.gyroscope_data[i][0],
        magic_wand.gyroscope_data[i][1],
        magic_wand.gyroscope_data[i][2]))
    
sleep_ms(1000)
for i in range(100): 
    print("gyro_drift_x={:5.3f}, gyro_drift_y={:5.3f}, gyro_drift_z={:5.3f}".format(
        magic_wand.gyroscope_drift[i][0],
        magic_wand.gyroscope_drift[i][1],
        magic_wand.gyroscope_drift[i][2]))

sleep_ms(1000)
for i in range(100): 
    print("corr_gyro_x={:5.3f}, corr_gyro_y={:5.3f}, corr_gyro_z={:5.3f}".format(
        magic_wand.corrected_gyroscope_data[i][0],
        magic_wand.corrected_gyroscope_data[i][1],
        magic_wand.corrected_gyroscope_data[i][2]))

sleep_ms(1000)

for i in range(100): 
    print("orient_x={:5.3f}, orient_y={:5.3f}, orient_z={:5.3f}".format(
        magic_wand.orientation_data[i][0],
        magic_wand.orientation_data[i][1],
        magic_wand.orientation_data[i][2]))
    
for i in range(100): 
    print("gravity_x={:5.3f}, gravity_y={:5.3f}, gravity_z={:5.3f}".format(
        magic_wand.gravity[i][0],
        magic_wand.gravity[i][1],
        magic_wand.gravity[i][2]))
    
for i in range(100): 
    print("velocity_x={:5.3f}, velocity_y={:5.3f}, velocity_z={:5.3f}".format(
        magic_wand.velocity[i][0],
        magic_wand.velocity[i][1],
        magic_wand.velocity[i][2]))
    
for i in range(100): 
    print("pos_x={:5.3f}, pos_y={:5.3f}, pos_z={:5.3f}".format(
        magic_wand.position[i][0],
        magic_wand.position[i][1],
        magic_wand.position[i][2]))

# read digit_1 and put the data into a strokePoints array

digit_1_file = open("strokes/digit_1.txt","r")
lines = []
for line in digit_1_file:
    lines.append(line.strip())
x = []
y = []
stroke_points = np.empty((len(lines),2),dtype=np.int8)
for l in range(len(lines)):
    tmp = lines[l].split(" ")
    # print(tmp)
    stroke_points[l][0] = round(float(tmp[0])*128)
    stroke_points[l][1] = round(float(tmp[1])*128)

# print(stroke_points)

magic_wand.strokePoints = stroke_points
magic_wand.rasterizeStroke()
magic_wand.plotStroke()
'''
