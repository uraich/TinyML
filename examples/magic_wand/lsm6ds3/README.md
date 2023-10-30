# Installing the LSM6DS3 driver
The LSM6DS3 driver consists of several files:
* LSM6DS3_const.py: contains all the constants needed be the driver. This file should also be imported be an application using the driver
* LSM6DS3_i2c.py is a subclass of LSM6DS3.py implementing register access through I2C. When using the LSM6DS3 with SPI, an LSM6DS3_spi.py module should be written.
* LSM6DS3.py: Implements all the LSm6DS3 functionality not depending on the type of hardware interface used

lsm6ds_test.py accesses some of the methods while the FIFO is not in use
lsm6ds6_fifo is similar to lsm6ds3_test.py but uses the FIFO