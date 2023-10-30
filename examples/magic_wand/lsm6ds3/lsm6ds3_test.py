from LSM6DS3_i2c import LSM6DS3_I2C
from LSM6DS3_const import *
from utime import sleep_ms

lsm6ds3 = LSM6DS3_I2C()
print("Device ID: 0x{:02x}".format(lsm6ds3.getDeviceID))
print("Reset the device")
lsm6ds3.sw_reset()
sleep_ms(10)

# lsm6ds3.debugging=True
print("---------------------------------------------------------")
print("Setting up the accelerometer") 
print("output data rate: 26 Hz, full scale 4g, bw: 50Hz") 
print("---------------------------------------------------------")

lsm6ds3.acc_odr="26 Hz"
print("acc output datarate: 0x{:02x}".format(lsm6ds3.acc_odr))
print("This corresponds to " + lsm6ds3.acc_odr_txt(lsm6ds3.acc_odr))
print("The numerical value is {:6.1f}".format(lsm6ds3.acc_odr_value(
     lsm6ds3.acc_odr_txt(lsm6ds3.acc_odr))))    

print("Setting full scale to 4g")
lsm6ds3.acc_full_scale="4g"
full_scale = lsm6ds3.acc_full_scale
print("Acc full scale value: {:d}".format(full_scale))
print("Acc full scale: " + lsm6ds3.acc_full_scale_txt(full_scale))

lsm6ds3.acc_bandwidth = "50 Hz"
print("acc bandwidth: 0x{:02x}".format(lsm6ds3.acc_bandwidth))
print("This corresponds to " + lsm6ds3.acc_bandwidth_txt(lsm6ds3.acc_bandwidth))
print("ctrl1_xl: 0x{:02x}".format(lsm6ds3.ctrl1_xl))
      
print("---------------------------------------------------------")
print("Setting up the gyroscope")
print("output data rate: 26 Hz, full scale: 2000 dps") 
print("---------------------------------------------------------")

lsm6ds3.gyro_odr="26 Hz"
print("gyro output datarate: 0x{:02x}".format(lsm6ds3.gyro_odr))
print("This corresponds to " + lsm6ds3.gyro_odr_txt(lsm6ds3.gyro_odr))
print("The numerical value is {:6.1f}".format(lsm6ds3.gyro_odr_value(
     lsm6ds3.gyro_odr_txt(lsm6ds3.gyro_odr))))

print("Setting gyro full scale to 2000 dps")
lsm6ds3.gyro_full_scale="2000 dps"
full_scale = lsm6ds3.gyro_full_scale
print("Gyro full scale value: {:d}".format(full_scale))
print("Gyro full scale: " + lsm6ds3.gyro_full_scale_txt(full_scale))

# lsm6ds3.gyro_125_dps=LSM6DS3_ENABLE
# print("gyro 125 dsp enabled " if lsm6ds3.gyro_125_dps else "gyro 125 dps disabled")
print("ctrl2_g: 0x{:02x}".format(lsm6ds3.ctrl2_g))

sleep_ms(40)  # wait for the data to become ready 40ms <=> 25Hz
print("accelerometer data ready" if lsm6ds3.acc_data_available else"no accelerometer data yet")
while not lsm6ds3.acc_data_available:
    sleep_ms(1)
    print("no accelerometer data yet")

print("Accel X raw: 0x{:04x} = {:d}".format(lsm6ds3.acc_x_raw,lsm6ds3.acc_x_raw))
print("Accel Y raw: 0x{:04x} = {:d}".format(lsm6ds3.acc_y_raw,lsm6ds3.acc_y_raw))
print("Accel Z raw: 0x{:04x} = {:d}".format(lsm6ds3.acc_z_raw,lsm6ds3.acc_z_raw))

print("accel_x: {:6.4f}, accel_y: {:6.4f}, accel_z: {:6.4f}".format(lsm6ds3.acc_x,
                                                                    lsm6ds3.acc_y,
                                                                    lsm6ds3.acc_z))
lsm6ds3.gyro_full_scale = "2000 dps"
print("gyroscope data ready" if lsm6ds3.gyro_data_available else "no gyroscope data yet")
while not lsm6ds3.gyro_data_available:
    sleep_ms(100)
print("gyro_x: {:6.4f}, gyro_y: {:6.4f}, gyro_z: {:6.4f}".format(lsm6ds3.gyro_x,
                                                                 lsm6ds3.gyro_y,
                                                                 lsm6ds3.gyro_z))
print("ctrl3_c: 0x{:02x}".format(lsm6ds3.ctrl3_c))

while not lsm6ds3.temperature_data_available:
    print("no temperature data yet")
    sleep_ms(500)
print("Temperature: {:4.2f}".format(lsm6ds3.temperature))


