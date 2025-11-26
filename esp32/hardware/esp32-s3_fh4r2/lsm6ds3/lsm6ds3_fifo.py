from LSM6DS3_i2c import LSM6DS3_I2C
from LSM6DS3_const import *
from utime import sleep_ms

FREQ = 104
ON   = 1

lsm6ds3 = LSM6DS3_I2C()
print("Device ID: 0x{:02x}".format(lsm6ds3.getDeviceID))
print("Reset the device")
lsm6ds3.sw_reset()
sleep_ms(2)

print("---------------------------------------------------------")
print("Setting up the accelerometer")
print("output data rate: 104 Hz, full scale: 4g") 
print("---------------------------------------------------------")

lsm6ds3.acc_odr="{:d} Hz".format(FREQ)
print("acc output datarate: 0x{:02x}".format(lsm6ds3.acc_odr))
print("This corresponds to " + lsm6ds3.acc_odr_txt(lsm6ds3.acc_odr))
print("Setting full scale to 4g")
lsm6ds3.acc_full_scale="4g"
full_scale = lsm6ds3.acc_full_scale
print("Acc full scale value: {:d}".format(full_scale))
print("Acc full scale: " + lsm6ds3.acc_full_scale_txt(full_scale))

lsm6ds3.acc_bandwidth = "50 Hz"
print("acc bandwidth: 0x{:02x}".format(lsm6ds3.acc_bandwidth))
print("This corresponds to " + lsm6ds3.acc_bandwidth_txt(lsm6ds3.acc_bandwidth))
print("ctrl1_xl: 0x{:02x}\n".format(lsm6ds3.ctrl1_xl))
      
print("---------------------------------------------------------")
print("Setting up the gyroscope")
print("output data rate: 104 Hz, full scale: 2000 dps") 
print("---------------------------------------------------------")

lsm6ds3.gyro_odr="{:d} Hz".format(FREQ)
print("gyro output datarate: 0x{:02x}".format(lsm6ds3.gyro_odr))
print("This corresponds to " + lsm6ds3.gyro_odr_txt(lsm6ds3.gyro_odr))

print("Setting gyro full scale to 2000 dps")
lsm6ds3.gyro_full_scale="2000 dps"
full_scale = lsm6ds3.gyro_full_scale
print("Gyro full scale value: {:d}".format(full_scale))
print("Gyro full scale: " + lsm6ds3.gyro_full_scale_txt(full_scale))
print("ctrl2_g: 0x{:02x}\n".format(lsm6ds3.ctrl2_g))

print("---------------------------------------------------------")
print("Setting up FIFO")
print("---------------------------------------------------------")
print("Set watermark threshold")
lsm6ds3.fifo_threshold = 0x200
print("Fifo threshold set to 0x{:04x}".format(lsm6ds3.fifo_threshold))
print("fifo_ctrl1: 0x{:02x}, fifo_ctrl2: 0x{:02x}\n".format(lsm6ds3.fifo_ctrl1,lsm6ds3.fifo_ctrl2))

print("Set fifo odr")
lsm6ds3.fifo_odr = "{:d} Hz".format(FREQ)
print("Fifo odr is set to {}".format(lsm6ds3.fifo_odr_txt(lsm6ds3.fifo_odr)))

print("Set the acc and gyro decimation factor to no decimation (factor = 1)")
lsm6ds3.fifo_acc_dec_factor  = 1
lsm6ds3.fifo_gyro_dec_factor = 1
print("acc decimation factor: {:d}".format(lsm6ds3.fifo_acc_dec_factor_txt(
    lsm6ds3.fifo_acc_dec_factor)))
print("gyro decimation factor: {:d}".format(lsm6ds3.fifo_gyro_dec_factor_txt(
    lsm6ds3.fifo_gyro_dec_factor)))
print("fifo_ctrl3: 0x{:02x}\n".format(lsm6ds3.fifo_ctrl3))

print("Set fifo mode to continuous")
lsm6ds3.fifo_mode = "continuous"
print("Fifo mode is set to 0x{:02x}".format(lsm6ds3.fifo_mode))
print("which corresponds to {}".format(lsm6ds3.fifo_mode_txt(lsm6ds3.fifo_mode)))
print("fifo_ctrl5: 0x{:02x}\n".format(lsm6ds3.fifo_ctrl5))

# lsm6ds3.bdu = ON
# print("ctrl3_c: 0x{:02x}\n".format(lsm6ds3.ctrl3_c))
print("---------------------------------------------------------")
print("Read FIFO")
print("---------------------------------------------------------\n")

while True:
    while lsm6ds3.fifo_empty:
        sleep_ms(10)
    # Read no of values in fifo
    data_count = lsm6ds3.words_in_fifo
    print("{:d} values in fifo".format(data_count))
    if data_count % 6:
        print("wrong data in FIFO")
    gyro_x_raw = lsm6ds3.fifo_data
    gyro_y_raw = lsm6ds3.fifo_data
    gyro_z_raw = lsm6ds3.fifo_data 
    acc_x_raw  = lsm6ds3.fifo_data
    acc_y_raw  = lsm6ds3.fifo_data
    acc_z_raw  = lsm6ds3.fifo_data
    print("gyro: ({:6.2f},{:6.2f},{:6.2f}), accel: ({:4.2f},{:4.2f},{:4.2f})".format(
        lsm6ds3.gyro_to_physical(gyro_x_raw),
        lsm6ds3.gyro_to_physical(gyro_y_raw),
        lsm6ds3.gyro_to_physical(gyro_z_raw),
        lsm6ds3.acc_to_physical(acc_x_raw),
        lsm6ds3.acc_to_physical(acc_y_raw),
        lsm6ds3.acc_to_physical(acc_z_raw)))
        
