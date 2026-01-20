# magic_wand.py: testing port of the magic wand demo to ESP32 and Python 
# Copyright (c) U. Raich Oct 2023
# This program is part of the TinyML course at the
# University of Cape Coast, Ghana
# It is released under the MIT license

from lsm6ds3_imu import LSM6DS3_IMU
from utime import sleep_ms
from micropython import const
import math, sys

# stroke state
eWaiting = 0
eDrawing = 1
eDone    = 2
    
sizeOfInt8_t  = const(1)
sizeOfInt32_t = const(4)

class MagicWand(object):
    def __init__(self,debug=False):
        self.debug = False
        self.stroke_transmit_stride = const(2)
        self.stroke_transmit_max_length = const(160)
        self.stroke_max_length = const(self.stroke_transmit_max_length * self.stroke_transmit_stride)
        self.stroke_points_byte_count = 2 * sizeOfInt8_t * self.stroke_transmit_max_length
        self.stroke_struct_byte_count = const(self.stroke_points_byte_count) 
        self.moving_sample_count = const(50)
        self.stroke_state = eWaiting

        self.raster_width = const(32)
        self.raster_height = const(32)
        self.raster_channels = const(3)
        self.raster_byte_count = self.raster_height * self.raster_width * self.raster_channels
        self.raster_buffer = bytearray(self.raster_byte_count)

        # A buffer holding the last 600 sets of 3-channel values from the accelerometer.
        self.data_length = const(600)
        self.acceleration_data = [(0.0, 0.0, 0.0)] * self.data_length
        # The next free entry in the data array.
        self.data_index = 0
        self.buffer_full = False # set to true when the data_index reaches 600 for the first time
        
        # A buffer holding the last 600 sets of 3-channel values from the gyroscope.
        # As the data length is the same for accelerometer and gyroscope we use a single constant
        self.gyroscope_data = [(0.0, 0.0, 0.0)] * self.data_length
        self.orientation_data = [(0.0, 0.0, 0.0)] * self.data_length
        # number of samples read in ReadAccelerationAndGyrroscope
        self.samples_read = 0
        
        self.stroke_length = 0
        self.stroke_struct_buffer = [(0,0)] * self.stroke_struct_byte_count # x,y values of stroke

        # int32_t* stroke_transmit_length = reinterpret_cast<int32_t*>(stroke_struct_buffer + sizeof(int32_t));
        # int8_t* stroke_points = reinterpret_cast<int8_t*>(stroke_struct_buffer + (sizeof(int32_t) * 2));

        self.current_velocity = [0.0, 0.0, 0.0]
        self.current_position = [0.0, 0.0, 0.0]
        self.current_gravity  = (0.0, 0.0, 0.0)
        self.current_gyroscope_drift = (0.0, 0.0, 0.0)
        
    def SetupIMU(self):
        self.IMU.setContinuousMode()
    
    # setup
    def setup(self):
        if self.debug:
            print("Setup started")
        self.IMU = LSM6DS3_IMU(debug=True)
        self.sample_rate = self.IMU.accelerationSampleRate()
        if self.debug:
            print("sample rate: {:4.1f}".format(self.sample_rate))
        self.SetupIMU()

    def printRegisterSettings(self):
        print("------------------------------------------------------------------")
        print("Verifying all IMU calls made by magic_wand.ino on the lsm6ds3")
        print("------------------------------------------------------------------")
        
        print("Acceleration data rate:     ",self.IMU.accelerationSampleRate()," Hz")
        print("Acceleration full scale:      +-",self.IMU.accelerationFullScale()," g")
        print("Gyroscope data rate:        ",self.IMU.gyroscopeSampleRate()," Hz")
        print("Gyroscope full scale:        ",self.IMU.gyroscopeFullScale()," dps")
        print("FIFO water mark:             0x{:03x}".format(self.IMU.fifoWaterMark()))
        print("FIFO odr:                   ",self.IMU.fifoSampleRate()," Hz")
        print("Acceleration decimation factor: ",self.IMU.accelerationDecimationFactor())
        print("Gyroscope decimation factor:    ",self.IMU.gyroDecimationFactor())
        print("FIFO CTRL5:                   0x{:02x}".format(self.IMU.fifoCtrl_5()))
        
    def printConstants(self):
        print("stroke_transmit_stride:     ",self.stroke_transmit_stride)
        print("stroke_transmit_max_length: ",self.stroke_transmit_max_length)
        print("stroke_max_length:          ",self.stroke_max_length)
        print("stroke_points_byte_count:   ",self.stroke_points_byte_count)
        print("stroke_struct_byte_count:   ",self.stroke_struct_byte_count)
        print("moving_sample_count:        ",self.moving_sample_count)
        
    @property
    def debugging(self):
        return self.debug

    @debugging.setter
    def debugging(self,onOff):
        self.debug = onOff
        
    def ReadAccelerometerAndGyroscope(self):
        new_samples = 0
        while self.IMU.accelerationAndGyroscopeAvailable():
            current_index = self.data_index % self.data_length
            gyro,acc = self.IMU.readAccelerationAndGyroscope()
            # print("data_index: ",self.data_index)
            self.gyroscope_data[current_index]      = gyro
            self.acceleration_data[current_index]   = acc

            self.data_index += 1
            new_samples += 1
            
            if self.debug: 
                print("data index: {:d}".format(self.data_index))
                print("New gyro values: x: {:4.2f}, y: {:4.2f}, z: {:4.2f}".format(
                    self.gyroscope_data[current_index][0],
                    self.gyroscope_data[current_index-1][1],
                    self.gyroscope_data[current_index-1][2]))
        
                print("New acc values: x: {:4.2f}, y: {:4.2f}, z: {:4.2f}".format(
                    self.acceleration_data[current_index-1][0],
                    self.acceleration_data[current_index-1][1],
                    self.acceleration_data[current_index-1][2]))

            if self.IMU.lsm6ds3.fifo_overrun:
                print("LSM6DS3 FiFo overrun error")
        return new_samples

    def VectorMagnitude(self,vec) :
        # print("Magnitude: ",math.sqrt(vec[0] * vec[0] + vec[1] * vec[1] + vec[2] * vec[2]))
        return math.sqrt(vec[0] * vec[0] + vec[1] * vec[1] + vec[2] * vec[2])

    def NormalizeVector(self,vec) :
        magnitude = VectorMagnitude(in_vec)
        return [vec[0]/magnitude,vec[1]/magnitude,vec[2]/magnitude]

    def DotProduct(self,a, b) :
        return (a[0] * b[0], a[1] * b[1], a[2] * b[2])
    
    def EstimateGyroscopeDrift(self,drift) :
        if self.debug:
            print("Estimate Gyroscope Drift")
        isMoving = self.VectorMagnitude(self.current_velocity) > 0.1
        # print("velocity: ",self.VectorMagnitude(self.current_velocity))
        if isMoving:
            # print("Is moving")
            return drift
        samples_to_average = 20
        if samples_to_average >= self.data_index:
            samples_to_average = self.data_index
            
        if self.debug:
            print("samples_to_average {:d}".format(samples_to_average))
        start_index = (self.data_index + \
                       (self.data_length - samples_to_average)) \
                       % self.data_length
        if self.debug:
            print("start index: {:d}, data_index: {:d}".format(
                start_index,self.data_index))
        x_total = 0.0
        y_total = 0.0
        z_total = 0.0
        for i in range(samples_to_average):
            index = (start_index + i) % self.data_length
            entry = self.gyroscope_data[index]
            x = entry[0]
            y = entry[1]
            z = entry[2]
            x_total += x
            y_total += y
            z_total += z
            
        self.gyroscope_drift = (x_total / samples_to_average,
                                y_total / samples_to_average,
                                z_total / samples_to_average)
        self.debug = False
        if self.debug:
            print("drift: {:4.3f}, {:4.3f}, {:4.3f}".format(self.gyroscope_drift[0],
                                                            self.gyroscope_drift[1],
                                                            self.gyroscope_drift[2]))
        self.debug = False
        return 

    def  UpdateOrientation(self,new_samples, drift) :
    
        drift_x = drift[0]
        drift_y = drift[1]
        drift_z = drift[2]

        start_index = (self.data_index + (self.data_length - new_samples)) % self.data_length

        # The gyroscope values are in degrees-per-second, so to approximate
        # degrees in the integrated orientation, we need to divide each value
        # by the number of samples each second.
        
        recip_sample_rate = 1.0 / self.sample_rate
        if self.debug:
            print("Update orientation")

        for i in range(new_samples):
            index = (start_index + i) % self.data_length
            entry = self.gyroscope_data[index]
            dx = entry[0]
            dy = entry[1]
            dz = entry[2]
    
            # Try to remove sensor errors from the raw gyroscope values.
            dx_minus_drift = dx - drift_x
            dy_minus_drift = dy - drift_y
            dz_minus_drift = dz - drift_z

            # Convert from degrees-per-second to appropriate units for this
            # time interval.
            dx_normalized = dx_minus_drift * recip_sample_rate
            dy_normalized = dy_minus_drift * recip_sample_rate
            dz_normalized = dz_minus_drift * recip_sample_rate

            # Update orientation based on the gyroscope data.
            previous_index = (index + self.data_length - 1) % self.data_length
            self.orientation_data[index] = (self.orientation_data[previous_index][0] + dx_normalized,
                                            self.orientation_data[previous_index][1] + dy_normalized,
                                            self.orientation_data[previous_index][2] + dz_normalized)

            # self.debug = True
            if self.debug:
                 print("dx: {:4.2f}, dy: {:4.2f}, dz: {:4.2f}".format(dx_normalized, dy_normalized, dz_normalized))
        
            if self.debug:
                print("previous orientation: {:d}: {:4.2f},{:4.2f},{:4.2f}".format(previous_index,
                self.orientation_data[previous_index][0],self.orientation_data[previous_index][1],self.orientation_data[previous_index][2]))
                print("current orientation: {:d}: {:4.2f},{:4.2f},{:4.2f}".format(index,
                self.orientation_data[index][0],self.orientation_data[index][1],self.orientation_data[index][2]))
            self.debug = False

        self.debug = False    
        if self.debug:
            print("After UpdateOrientation")
            start_index = (self.data_index + (self.data_length - new_samples)) % self.data_length        
            for i in range(new_samples):
                index = (start_index + i) % self.data_length
                print("current orientation: {:d}: {:4.2f},{:4.2f},{:4.2f}".format(index,
                                                                                  self.orientation_data[index][0],
                                                                                  self.orientation_data[index][1],
                                                                                  self.orientation_data[index][2]))
        self.debug = False
        
    def IsMoving(self,samples_before):
        moving_threshold = 10.0
        # print("data_index: ",self.data_index,", samples_before: ",samples_before)
        if self.data_index - samples_before < self.moving_sample_count:
            return False

        start_index = (self.data_index + (self.data_length - (self.moving_sample_count + samples_before))) % self.data_length

        total = 0.0
        for i in range(self.moving_sample_count):
            index = ((start_index + i) % self.data_length)
            current_orientation = self.orientation_data[index]
            self.debug = False
            if self.debug:
                print("IsMoving")
                print("current orientation: {:d}: {:4.2f}, {:4.2f}, {:4.2f}".format(index,
                                                                                    current_orientation[0],
                                                                                    current_orientation[1],
                                                                                    current_orientation[2]))
            previous_index = (index + (self.data_length - 1)) % self.data_length
            previous_orientation = self.orientation_data[previous_index]
            if self.debug:
                print("previous orientation: {:d}: {:4.2f}, {:4.2f}, {:4.2f}".format(previous_index,
                                                                                    current_orientation[0],
                                                                                    current_orientation[1],
                                                                                    current_orientation[2]))
                                                  
            self.debug = False
            dx = current_orientation[0] - previous_orientation[0]
            dy = current_orientation[1] - previous_orientation[1]
            dz = current_orientation[2] - previous_orientation[2]
            # self.debug = True
            if self.debug:
                print("dx, dy, dz: {:4.3f}, {:4.3f}, {:4.3f}".format(dx,dy,dz))
            self.debug = False
            mag_squared = (dx * dx) + (dy * dy) + (dz * dz);
            total += mag_squared;
            
        # self.debug = True
        if self.debug:
            print("mag_squared: {:4.3f}, moving threshold: {:4.3f}".format(mag_squared,moving_threshold))
            if total > moving_threshold:
                print("Is moving")
            else:
                print("Is not moving")
            self.debug = False
        is_moving = total > moving_threshold
        return is_moving

    def UpdateStroke(self,new_samples):
        minimum_stroke_length = self.moving_sample_count + 10
        minimum_stroke_size = 0.2

        done_just_triggered = False
        # self.debug=True
        if self.debug:
            self.printStrokeState(self.stroke_state)
            # print("new_samples: ",new_samples)
        self.debug = False
        for i in range(new_samples):
            current_head = new_samples - (i + 1)
            is_moving = self.IsMoving(current_head)
            # self.debug = True
            if self.debug:
                if is_moving:
                    print("UpdateStroke: is moving")
                else:
                    print("UpdateStroke: is not moving")
            
            # print("current_head: ",current_head)
            self.debug = False
            old_state = self.stroke_state
            if old_state == eWaiting or old_state == eDone:
                if is_moving:
                    self.stroke_length = self.moving_sample_count
                    self.stroke_state = eDrawing
                    print("Drawing")
            elif old_state == eDrawing:
                if (not is_moving):
                    if self.stroke_length > minimum_stroke_length:
                        self.stroke_state = eDone
                        print("Done")
                    else:
                        print("Stroke too short: {:5.2f}".format(self.stroke_length))
                        stroke_length = 0;
                        self.stroke_state = eWaiting
  
            if self.stroke_state == eWaiting:
                continue
    
            self.stroke_length += 1
            if self.stroke_length > self.stroke_max_length:
                self.stroke_length = self.stroke_max_length
  
            # Only recalculate the full stroke if it's needed.
            draw_last_point = (i == (new_samples -1)) and (self.stroke_state == eDrawing)
            done_just_triggered = (old_state != eDone) and (self.stroke_state == eDone)
            if (not done_just_triggered) or draw_last_point :
                continue;

            if done_just_triggered:
                print("Done just triggered")
                print("Stroke length: ",self.stroke_length)
                print("data index: ",self.data_index)

            start_index = ((self.data_index + 
                            (self.data_length - (self.stroke_length + current_head))) % 
                           self.data_length);

            x_total = 0.0
            y_total = 0.0
            z_total = 0.0
            
            for j in range(self.stroke_length):
                index = (start_index + j) % self.data_length
                entry = self.orientation_data[index]  
                x_total += entry[0]
                y_total += entry[1]
                z_total += entry[2]

            x_mean = x_total / self.stroke_length
            y_mean = y_total / self.stroke_length
            z_mean = z_total / self.stroke_length
            range = 90.0

            gy = self.current_gravity[1]
            gz = self.current_gravity[2];
            gmag = math.sqrt((gy * gy) + (gz * gz))
            if gmag < 0.0001:
                gmag = 0.0001
            
            ngy = gy / gmag
            ngz = gz / gmag
                
            xaxisz = -ngz
            xaxisy = -ngy
            
            yaxisz = -ngy
            yaxisy = ngz
    
            self.stroke_transmit_length = self.stroke_length / self.stroke_transmit_stride


            for j in range(self.stroke_transmit_length):
                orientation_index = (start_index + j * self.stroke_transmit_stride) % self.data_length
                orientation_entry = self.orientation_data[orientation_index] 
            
                orientation_x = orientation_entry[0]
                orientation_y = orientation_entry[1]
                orientation_z = orientation_entry[2]
            
                nx = (orientation_x - x_mean) / range
                ny = (orientation_y - y_mean) / range
                nz = (orientation_z - z_mean) / range
                
                x_axis = xaxisz * nz + xaxisy * ny
                y_axis = yaxisz * nz + yaxisy * ny    
                
                unchecked_x = round(x_axis * 128.0)
            
                if unchecked_x > 127:
                    stored_x = 127
                elif unchecked_x < -128:
                    stored_x = -128
                else:
                    stored_x = unchecked_x
                    # stroke_entry[0] = stored_x;
                    
                unchecked_y = round(y_axis * 128.0)

                if unchecked_y > 127:
                    stored_y = 127
                elif unchecked_y < -128:
                    stored_y = -128
                else:
                    stored_y = unchecked_y
                    
                self.stroke_struct_buffer[j] = (stored_x,stored_y)
                
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
            if done_just_triggered:
                x_range = x_max - x_min
                y_range = y_max - y_min
                if x_range < minimum_stroke_size and y_range < minimum_stroke_size: 
                    done_just_triggered = False
                    self.stroke_state = eWaiting
                    self.stroke_transmit_length = 0
                    self.stroke_length = 0
                    print("Stroke too small, canceled")          
                    print("range: {:4.3f}, {:4.3f}".format(x_range,y_range))
                else:
                    print("Stroke ok")
                    for i in range(self.stroke_transmit_length):
                        print("{:d} {:d}".format(self.stroke_struct_buffer[i][0],
                                                 self.stroke_struct_buffer[i][1]))
                                          
        return done_just_triggered
        
    def EstimateGravityDirection(self):
        samples_to_average = 100

        if samples_to_average >= self.data_index and not self.buffer_full:
            samples_to_average = self.data_index
        else:
            samples_to_average = 100

        start_index = (self.data_index + \
            (self.data_length - samples_to_average)) % self.data_length
        if self.debug:
            print("samples to average: {:d}".format(samples_to_average))
            print("acceleration data index: {:d}".format(self.data_index))
            print("start index: {:d}".format(start_index))
        x_total = 0.0
        y_total = 0.0
        z_total = 0.0
 
        for i  in range(samples_to_average):
            index = (start_index + i ) % self.data_length

            entry = self.acceleration_data[index]
            x = entry[0]
            y = entry[1]
            z = entry[2]
            x_total += x
            y_total += y
            z_total += z
            
        self.current_gravity = (x_total / samples_to_average,
                                y_total / samples_to_average,
                                z_total / samples_to_average)
        self.debug = False
        if self.debug:
            print("current gravity: {:4.3f}, {:4.3f}, {:4.3f}".format(self.current_gravity[0],
                                                                      self.current_gravity[1],
                                                                      self.current_gravity[2]))
        self.debug = False
        return 

    def UpdateVelocity(self,new_samples, gravity):
        gravity_x = gravity[0]
        gravity_y = gravity[1]
        gravity_z = gravity[2]

        start_index = self.data_index + \
            (self.data_length - new_samples) % self.data_length

        friction_fudge = 0.98

        for i in range(new_samples):
            index = (start_index + i) % self.data_length
            entry = self.acceleration_data[index]
            # print("index: ",index, "acc entry: ",entry)
            ax = entry[0]
            ay = entry[1]
            az = entry[2]
            
            # Try to remove gravity from the raw acceleration values.
            ax_minus_gravity = ax - gravity_x
            ay_minus_gravity = ay - gravity_y
            az_minus_gravity = az - gravity_z
            
            # Update velocity based on the normalized acceleration.
            self.current_velocity[0] += ax_minus_gravity
            self.current_velocity[1] += ay_minus_gravity
            self.current_velocity[2] += az_minus_gravity
            #print("current_velocity: ", self.current_velocity)
            
            # Dampen the velocity slightly with a fudge factor to stop it exploding.
            self.current_velocity[0] *= friction_fudge
            self.current_velocity[1] *= friction_fudge
            self.current_velocity[2] *= friction_fudge
            
            # Update the position estimate based on the velocity.
            self.current_position[0] += self.current_velocity[0]
            self.current_position[1] += self.current_velocity[1]
            self.current_position[2] += self.current_velocity[2]
            
        # self.debug=True
        if self.debug:
            print("current_velocity: {:4.3f}, {:4.3f}, {:4.3f}".format(self.current_velocity[0],
                                                                       self.current_velocity[1],
                                                                       self.current_velocity[2]))
            print("{:4.3f}, {:4.3f}, {:4.3f}".format(self.current_position[0],
                                                     self.current_position[1],
                                                     self.current_position[2]))
        self.debug = False

    def printStrokeState(self,state):
        if state == eWaiting:
            print("Waiting")
        elif state == eDrawing:
            print("Drawing")
        elif state == eDone:
            print("Done")
        else:
            print("Unknown")
        
    def loop(self):
        while True:
            while not self.IMU.accelerationAndGyroscopeAvailable():
                # print("Waiting for data")
                continue
            self.samples_read = self.ReadAccelerometerAndGyroscope()

            if self.debug:
                print("Samples read: ", self.samples_read)
                current_index = (self.data_index - self.samples_read) % self.data_length
                for i in range(self.samples_read):
                    local_index = (current_index + i) % self.data_length
                    print("{:d}: {:4.2f}, {:4.2f}, {:4.2f},     {:4.2f}, {:4.2f}, {:4.2f}".format(
                        local_index,
                        self.acceleration_data[local_index][0],
                        self.acceleration_data[local_index][1],
                        self.acceleration_data[local_index][2],
                        self.gyroscope_data[local_index][0],
                        self.gyroscope_data[local_index][1],
                        self.gyroscope_data[local_index][2]))

            # the gyroscope updates
            self.EstimateGyroscopeDrift(self.current_gyroscope_drift)
            self.debug = False
            if self.debug:
                print("current drift: {:4.2f},{:4.2f},{:4.2f}".format(
                    self.current_gyroscope_drift[0],
                    self.current_gyroscope_drift[1],
                    self.current_gyroscope_drift[2]))
            self.debug = False
            
            self.UpdateOrientation(self.samples_read,self.current_gyroscope_drift)

            # self.debugging = True
            done_just_triggered = self.UpdateStroke(self.samples_read)
            if (done_just_triggered):
                print("Done just triggered")

            self.debugging=False            
            self.EstimateGravityDirection()
            self.UpdateVelocity(self.samples_read,self.current_gravity)
            # self.debug = True
            if self.debug:
                print("current velocity: {:4.2f}, {:4.2f}, {:4.2f}".format(
                    self.current_velocity[0],self.current_velocity[1],self.current_velocity[2]))
                print("current gravity: {:4.2f}, {:4.2f}, {:4.2f}".format(
                    self.current_gravity[0],self.current_gravity[1],self.current_gravity[2]))
            self.debug = False

            # accelerator updates
            self.UpdateVelocity(self.samples_read,self.current_gravity)
            # print("current velocity: ",self.current_velocity)
            # print("current_position :",self.current_position)
            
magic_wand = MagicWand()
magic_wand.setup()
magic_wand.printRegisterSettings()
print("")
magic_wand.printConstants()

print("Starting loop")
magic_wand.loop()
