# lsm6ds3imu.py: replacement of the LSM9DS1 arduino class using the LSM6DS3
# since there is no magnetometer and it is not used by the magic wand
# these functions are removed.
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

class MagicWand(object):
    def __init__(self,debug=False):
        self.debug = debug
        if self.debug:
            print("Magic Wand debugging enabled")
        else:
            print("Magic Wand debugging disabled")
        self.stroke_transmit_stride = const(2)
        self.stroke_transmit_max_length = const(160)
        self.stroke_max_length = const(self.stroke_transmit_max_length * self.stroke_transmit_stride)
        self.stroke_points_byte_count = 2 *self.stroke_transmit_max_length
        self.stroke_struct_byte_count = const(2 * self.stroke_points_byte_count)
        self.moving_sample_count = const(5)
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
        self.orientation_data = [[0.0, 0.0, 0.0]] * self.data_length
        # The next free entry in the data array.
        
        self.stroke_length = 0
        self.stroke_struct_buffer = [None] * self.stroke_struct_byte_count
        self.stroke_state = self.stroke_struct_buffer
        # int32_t* stroke_transmit_length = reinterpret_cast<int32_t*>(stroke_struct_buffer + sizeof(int32_t));
        # int8_t* stroke_points = reinterpret_cast<int8_t*>(stroke_struct_buffer + (sizeof(int32_t) * 2));

        self.current_velocity = [0.0, 0.0, 0.0]
        self.current_position = [0.0, 0.0, 0.0]
        self.current_gravity  = [0.0, 0.0, 0.0]
        self.current_gyroscope_drift = [0.0, 0.0, 0.0]
        
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

    @property
    def debugging(self):
        return self.debug

    @debugging.setter
    def debugging(self,onOff):
        self.debug = onOff
        
    def ReadAccelerometerAndGyroscope(self):
        self.samples_read, gyro_samples, acc_samples = self.IMU.readAccelerationAndGyroscope()
        if self.debug:
            print("no of samples read: {:d}".format(self.samples_read))
        for i in range(self.samples_read):
            self.gyroscope_data[self.data_index+i] = gyro_samples[i]

            self.acceleration_data[self.data_index+i] = acc_samples[i]
            self.current_acceleration_data = acc_samples[i]

            # update the data index
            self.data_index += 1
            self.data_index = self.data_index % self.data_length
            if self.data_index == 0:
                self.buffer_full = True
        if self.debug: 
            print("data index: {:d}".format(self.data_index))
            print("New gyro values: x: {:4.2f}, y: {:4.2f}, z: {:4.2f}".format(
                self.gyroscope_data[self.data_index-1][0],
                self.gyroscope_data[self.data_index-1][1],
                self.gyroscope_data[self.data_index-1][2]))
        
            print("New acc values: x: {:4.2f}, y: {:4.2f}, z: {:4.2f}".format(
                self.acceleration_data[self.data_index-1][0],
                self.acceleration_data[self.data_index-1][1],
                self.acceleration_data[self.data_index-1][2]))

        if self.IMU.lsm6ds3.fifo_overrun:
            print("LSM6DS3 FiFo overrun error")
            
    def VectorMagnitude(self,vec) :
        return math.sqrt(vec[0] * vec[0] + vec[1] * vec[1] + vec[2] * vec[2])

    def NormalizeVector(self,vec) :
        magnitude = VectorMagnitude(in_vec)
        return [vec[0]/magnitude,vec[1]/magnitude,vec[2]/magnitude]

    def DotProduct(self,a, b) :
        return (a[0] * b[0], a[1] * b[1], a[2] * b[2])
    
    def EstimateGyroscopeDrift(self) :
        if self.debug:
            print("Estimate Gyroscope Drift")
        isMoving = self.VectorMagnitude(self.current_velocity) > 0.1
        if isMoving: 
            return
        samples_to_average = 20
        if samples_to_average >= self.data_index and not self.buffer_full:
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
        return ((x_total / samples_to_average,y_total / samples_to_average,z_total / samples_to_average))

    def  UpdateOrientation(self,new_samples, drift) :
    
        drift_x = drift[0]
        drift_y = drift[1]
        drift_z = drift[2]

        start_index = (self.data_index + (self.data_length - new_samples)) % \
                       self.data_length

        # The gyroscope values are in degrees-per-second, so to approximate
        # degrees in the integrated orientation, we need to divide each value
        # by the number of samples each second.
        
        recip_sample_rate = 1.0 / self.sample_rate

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
        self.current_orientation = self.orientation_data[index]
        previous_index = (index + self.data_length - 1) % self.data_length
        previous_orientation = self.orientation_data[previous_index]
        self.current_orientation[0] = previous_orientation[0] + dx_normalized
        self.current_orientation[1] = previous_orientation[1] + dy_normalized
        self.current_orientation[2] = previous_orientation[2] + dz_normalized
        if self.debug:
            print("current orientation: {:4.2f},{:4.2f},{:4.2f}".format(
                self.current_orientation[0],self.current_orientation[1],self.current_orientation[2]))

    def IsMoving(self,samples_before):
        moving_threshold = 10.0
        
        if self.data_index - samples_before < self.moving_sample_count:
            return False

        start_index = (data_index + \
                       (gyroscope_data_length - (moving_sample_count + samples_before))) % \
                       gyroscope_data_length

        total = 0.0
        for i in range(moving_sample_count):
            index = ((start_index + i) % data_length)
            current_orientation = self.orientation_data[index]
            previous_index = (index + (data_length - 1)) % data_length
            previous_orientation = self.orientation_data[previous_index]
            dx = self.current_orientation[0] - self.previous_orientation[0]
            dy = self.current_orientation[1] - self.previous_orientation[1]
            dz = self.current_orientation[2] - self.previous_orientation[2]
            mag_squared = (dx * dx) + (dy * dy) + (dz * dz);
            total += mag_squared;
        is_moving = total > moving_threshold
        return is_moving

    def UpdateStroke(self,new_samples):
        minimum_stroke_length = self.moving_sample_count + 10
        minimum_stroke_size = 0.2

        done_just_triggered = False
        
        for i in range(new_samples):
            current_head = new_samples - (i + 1)
            is_moving = self.IsMoving(current_head)
            old_state = stroke_state
            if old_state == eWaiting or old_state == eDone:
                if is_moving:
                    stroke_length = moving_sample_count
                    stroke_state = eDrawing
                elif old_state == eDrawing:
                    if (not is_moving):
                        if stroke_length > minimum_stroke_length:
                            stroke_state = eDone
                        else:
                            stroke_length = 0;
                    stroke_state = eWaiting
  
            is_waiting = stroke_state == eWaiting
            if is_waiting:
                continue
    
            stroke_length += 1
            if stroke_length > stroke_max_length:
                stroke_length = stroke_max_length
  
            # Only recalculate the full stroke if it's needed.
            draw_last_point = (i == (new_samples -1)) and (stroke_state == eDrawing)
            done_just_triggered = (old_state != eDone) and (stroke_state == eDone)
            if not (done_just_triggered or draw_last_point):
                continue

            start_index = ((self.data_index + 
                            (self.gyroscope_data_length - (stroke_length + current_head))) % 
                           self.gyroscope_data_length);

            x_total = 0.0
            y_total = 0.0
            z_total = 0.0
            
            for j in range(stroke_length):
                index = (start_index + j) % self.gyroscope_data_length
                entry = orientation_data[index]  
                x_total += entry[0]
                y_total += entry[1]
                z_total += entry[2]

            x_mean = x_total / stroke_length
            y_mean = y_total / stroke_length
            z_mean = z_total / stroke_length
            range = 90.0

            gy = current_gravity[1]
            gz = current_gravity[2];
            gmag = math.sqrt((gy * gy) + (gz * gz))
            if gmag < 0.0001:
                gmag = 0.0001
        
                ngy = gy / gmag
                ngz = gz / gmag
                
                xaxisz = -ngz
                xaxisy = -ngy
                
                yaxisz = -ngy
                yaxisy = ngz
    
            stroke_transmit_length = stroke_length / stroke_transmit_stride


            for j in range(stroke_transmit_length):
                orientation_index = (start_index + j * stroke_transmit_stride) % self.gyroscope_data_length
                orientation_entry = orientation_data[orientation_index] 

                orientation_x = orientation_entry[0]
                orientation_y = orientation_entry[1]
                orientation_z = orientation_entry[2]
                
                nx = (orientation_x - x_mean) / range
                ny = (orientation_y - y_mean) / range
                nz = (orientation_z - z_mean) / range
                
                x_axis = xaxisz * nz + xaxisy * ny
                y_axis = yaxisz * nz + yaxisy * ny    
                
                stroke_index = j * 2
                stroke_entry = stroke_points[stroke_index]
                
                unchecked_x = math.round(x_axis * 128.0)
                
                if unchecked_x > 127:
                    stored_x = 127
                elif unchecked_x < -128:
                    stored_x = -128
                else:
                    stored_x = unchecked_x
                stroke_entry[0] = stored_x;
      
                unchecked_y = math.round(y_axis * 128.0)

                if unchecked_y > 127:
                    stored_y = 127
                elif unchecked_y < -128:
                    stored_y = -128
                else:
                    stored_y = unchecked_y
                stroke_entry[1] = stored_y;

                is_first = (j == 0)
                if is_first or x_axis < x_min :
                    x_min = x_axi
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
                    stroke_state = eWaiting
                    stroke_transmit_length = 0
                    stroke_length = 0
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
        
        return ((x_total / samples_to_average,
                 y_total / samples_to_average,
                 z_total / samples_to_average))

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
            print("index: ",index, "acc entry: ",entry)
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
            print("current_velocity: ", self.current_velocity)
            
            # Dampen the velocity slightly with a fudge factor to stop it exploding.
            self.current_velocity[0] *= friction_fudge
            self.current_velocity[1] *= friction_fudge
            self.current_velocity[2] *= friction_fudge
            
            # Update the position estimate based on the velocity.
            self.current_position[0] += self.current_velocity[0]
            self.current_position[1] += self.current_velocity[1]
            self.current_position[2] += self.current_velocity[2]

    def loop(self):
        for i in range(1000):
            print("loop count: ",i)
            while not self.IMU.accelerationAndGyroscopeAvailable():
                print("Waiting for data")
                sleep_ms(10)              
            self.ReadAccelerometerAndGyroscope()
            # the gyroscope updates
            self.current_gyroscope_drift = self.EstimateGyroscopeDrift()
            print("current drift: {:4.2f},{:4.2f},{:4.2f}".format(
                self.current_gyroscope_drift[0],
                self.current_gyroscope_drift[1],
                self.current_gyroscope_drift[2]))            
            self.UpdateOrientation(self.samples_read,self.current_gyroscope_drift)
            
            self.debugging = True
            done_just_triggered = self.UpdateStroke(self.samples_read)
            self.debugging=False
        '''            
            self.current_gravity = self.EstimateGravityDirection()
            self.UpdateVelocity(self.samples_read,self.current_gravity)
            print("current velocity: {:4.2f}, {:4.2f}, {:4.2f}".format(
                self.current_velocity[0],self.current_velocity[1],self.current_velocity[2]))
        print("current gravity: {:4.2f}, {:4.2f}, {:4.2f}".format( \
            self.current_gravity[0],self.current_gravity[1],self.current_gravity[2]))
        
        print("single gravity values: {:4.2f}, {:4.2f}, {:4.2f}".format( \
            self.acceleration_data[0][0],self.acceleration_data[0][1],self.acceleration_data[0][2]))
                                                    

            # the gyroscope updates
            self.current_gravity = self.EstimateGravityDirection()
            print("Current gravity: ",self.current_gravity)
            self.debug = True

            self.debug=False
            # self.UpdateStroke(
            # accelerator updates
            self.current_gravity = self.EstimateGravityDirection()
            self.UpdateVelocity(self.samples_read,self.current_gravity)
            print("current velocity: ",self.current_velocity)
            print("current_position :",self.current_position)
        '''
magic_wand = MagicWand()
magic_wand.setup()
print("Starting loop")
magic_wand.loop()
