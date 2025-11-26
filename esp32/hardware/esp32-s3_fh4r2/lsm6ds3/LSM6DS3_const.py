# constants used by the LSM6DS3 driver
# Copyright (c) U. Raich, October 2023
# This program is part of the course on tinyML at
# the University of Cape Coast, Ghana
# It is released under the MIT license

LSM6DS3_I2C_ADDR               = const(0x6b)
LSM6DS3_WHO_AM_I_CODE          = const(0x69)
# Register addresses

LSM6DS3_FUNC_CFG_ACCESS        = const(0x01)
FUNC_CFG_EN                    = 7
LSM6DS3_SENSOR_SYNC_TIME_FRAME = const(0x04)
LSM6DS3_FIFO_CTRL1             = const(0x06)
FIFO_THRESHOLD_UPPER_POS  = 3
FIFO_THRESHOLD_UPPER_SIZE = 4
TIMER_PEDO_FIFO_EN        = 6
TIMER_PEDO_FIFO_DRDY      = 7

LSM6DS3_FIFO_CTRL2             = const(0x07)
TIMER_PEDO_FIFO_EN        = 7
TIMER_PEDO_FIFO_DRDY      = 6
FIFO_THRESHOLD_LEVEL_POS  = 3
FIFO_THRESHOLD_LEVEL_SIZE = 2
LSM6DS3_FIFO_CTRL3             = const(0x08)
GYRO_FIFO_DECIM_POS       = 5
GYRO_FIFO_DECIM_SIZE      = 3
ACC_FIFO_DECIM_POS        = 2
ACC_FIFO_DECIM_SIZE       = 3
lsm6ds3_dec_factor = { 0 : int('000',2),  # not used in fifo
                       1 : int('001',2),  # no decimation
                       2 : int('010',2),
                       3 : int('011',2),
                       4 : int('100',2),
                       8 : int('101',2),
                      16 : int('110',2),
                      32 : int('111',2)}                                 
                         
LSM6DS3_FIFO_CTRL4             = const(0x09)
LSM6DS3_FIFO_CTRL5             = const(0x0a)
FIFO_ODR_POS              = 6
FIFO_ODR_SIZE             = 4
FIFO_MODE_POS             = 2
FIFO_MODE_SIZE            = 3
lsm6ds3_fifo_mode = {'bypass'                   : int('000',2),
                     'fifo mode'                : int('001',2),
                     'continuous until trigger' : int('011',2),
                     'bypass until trigger'     : int('100',2),
                     'continuous'               : int('110',2)}
                     
LSM6DS3_ORIENT_CFG             = const(0x0b)
LSM6DS3_INT1_CTRL              = const(0x0d)
LSM6DS3_INT2_CTRL              = const(0x0e)
LSM6DS3_WHO_AM_I               = const(0x0f)
LSM6DS3_CTRL1_XL               = const(0x10)
OUTPUT_RATE_POS  = 7
OUTPUT_RATE_SIZE = 4
ACC_FULL_SCALE_POS   = 3
ACC_FULL_SCALE_SIZE  = 2
ACC_BANDWIDTH_POS    = 1
ACC_BANDWIDTH_SIZE   = 2
lsm6dr3_acc_full_scale = {"2g"  : int('00',2),
                          "4g"  : int('10',2),
                          "8g"  : int('11',2),
                          "16g" : int('01',2)}

lsm6ds3_acc_full_scale_convert = { int('00',2) : 2,
                                   int('10',2) : 4,
                                   int('11',2) : 8,
                                   int('01',2) : 16}

lsm6ds3_odr  = {"power down": int('0000',2),
                    "12.5 Hz"   : int('0001',2),
                    "26 Hz"     : int('0010',2),
                    "52 Hz"     : int('0011',2),
                    "104 Hz"    : int('0100',2),
                    "208 Hz"    : int('0101',2),
                    "416 Hz"    : int('0110',2),
                    "833 Hz"    : int('0111',2),
                    "1.66 kHz"  : int('1000',2),
                    "3.33 kHz"  : int('1001',2),
                    "6.66 kHz"  : int('1010',2)}

lsm6ds3_acc_bw = {"400 Hz" : int('00',2),
                  "200 Hz" : int('01',2),
                  "100 Hz" : int('10',2),
                   "50 Hz" : int('11',2)}
            
LSM6DS3_CTRL2_G                = const(0x11)
GYRO_FULL_SCALE_POS   = 3
GYRO_FULL_SCALE_SIZE  = 2
GYRO_BANDWIDTH_POS    = 1
GYRO_BANDWIDTH_SIZE   = 2

lsm6ds3_gyro_full_scale = { "250 dps": int('00',2),
                            "500 dps": int('01',2),
                           "1000 dps": int('10',2),
                           "2000 dps": int('11',2)}

lsm6ds3_gyro_full_scale_convert = { int('00',2) : 250,
                                    int('01',2) : 500,
                                    int('10',2) : 1000,
                                    int('11',2) : 2000}
LSM6DS3_ENABLE        = 1
LSM6DS3_DISABLE       = 0
LSM6DS3_GYRO_125_DPS  = 0

LSM6DS3_CTRL3_C       = const(0x12)
LSM6DS3_SW_RESET      = 0
LSM6DS3_BLE           = 1
LSM6DS3_IF_ADD_INC    = 2
LSM6DS3_SIM           = 3
LSM6DS3_PP_OD         = 4
LSM6DS3_H_LACTIVE     = 5
LSM6DS3_BDU           = 6
LSM6DS3_BOOT          = 7

LSM6DS3_CTRL4_C                = const(0x13)
LSM6DS3_XL_BW_SCAL_ODR = 7
LSM6DS3_SLEEP_G        = 6
LSM6DS3_INT2_ON_INT1   = 5
LSM6DS3_FIFO_TEMP_EN   = 4
LSM6DS3_DRDY_MASK      = 3
LSM6DS3_I2C_DISABLE    = 2
LSM6DS3_STOP_ON_FTH    = 0

LSM6DS3_CTRL5_C                = const(0x14)
LSM6DS3_CTRL6_C                = const(0x15)
LSM6DS3_CTRL7_G                = const(0x16)
LSM6DS3_CTRL8_XL               = const(0x17)
LSM6DS3_LPF2_XL_EN     = 7
LSM6DS3_HPCF_POS       = 6
LSM6DS3_HPCF_SIZE      = 2
LSM6DS3_HP_SLOPE_XL_EN = 2
LSM6DS3_LOW_PASS_ON_6D = 0
lsm6ds3_high_pass = { "ODR_XL/4"   : int('00',2),
                      "ODR_XL/100" : int('01',2),
                      "ODR_XL/9"   : int('10',2),
                      "ODR_XL/400" : int('11',2)}

lsm6ds3_cutoff = { "ODR_XL/50"  : int('00',2),
                   "ODR_XL/100" : int('01',2),
                   "ODR_XL/9"   : int('10',2),
                   "ODR_XL/400" : int('11',2)}

LSM6DS3_CTRL9_XL               = const(0x18)
LSM6DS3_CTRL10_C               = const(0x19)
LSM6DS3_MASTER_CONFIG          = const(0x1a)
LSM6DS3_WAKE_UP_SRC            = const(0x1b)
LSM6DS3_TAP_SRC                = const(0x1c)
LSM6DS3_D6D_SRC                = const(0x1d)
LSM6DS3_STATUS_REG             = const(0x1e)
# data available bits
LSM6DS3_TDA                    = 2
LSM6DS3_GDA                    = 1
LSM6DS3_XLDA                   = 0
LSM6DS3_OUT_TEMP_L             = const(0x20)
LSM6DS3_OUT_TEMP_H             = const(0x21)
LSM6DS3_OUTX_L_G               = const(0x22)
LSM6DS3_OUTX_H_G               = const(0x23)
LSM6DS3_OUTY_L_G               = const(0x24)
LSM6DS3_OUTY_H_G               = const(0x25)
LSM6DS3_OUTZ_L_G               = const(0x26)
LSM6DS3_OUTZ_L_H               = const(0x27)
LSM6DS3_OUTX_L_XL              = const(0x28)
LSM6DS3_OUTX_H_XL              = const(0x29)
LSM6DS3_OUTY_L_XL              = const(0x2a)
LSM6DS3_OUTY_H_XL              = const(0x2b)
LSM6DS3_OUTZ_L_XL              = const(0x2c)
LSM6DS3_OUTZ_H_XL              = const(0x2d)
LSM6DS3_SENSORHUB1_REG         = const(0x2e)
LSM6DS3_SENSORHUB2_REG         = const(0x2f)
LSM6DS3_SENSORHUB3_REG         = const(0x30)
LSM6DS3_SENSORHUB4_REG         = const(0x31)
LSM6DS3_SENSORHUB5_REG         = const(0x32)
LSM6DS3_SENSORHUB6_REG         = const(0x33)
LSM6DS3_SENSORHUB7_REG         = const(0x34)
LSM6DS3_SENSORHUB8_REG         = const(0x35)
LSM6DS3_SENSORHUB9_REG         = const(0x36)
LSM6DS3_SENSORHUB10_REG        = const(0x37)
LSM6DS3_SENSORHUB11_REG        = const(0x38)
LSM6DS3_SENSORHUB12_REG        = const(0x39)
LSM6DS3_FIFO_STATUS1           = const(0x3a)
LSM6DS3_FIFO_STATUS2           = const(0x3b)
FIFO_WATERMARK_REACHED = 7
FIFO_OVERRUN           = 6
FIFO_FULL              = 5
FIFO_EMPTY             = 4
LSM6DS3_FIFO_STATUS3           = const(0x3c)
LSM6DS3_FIFO_STATUS4           = const(0x3d)
LSM6DS3_FIFO_DATA_OUT_L        = const(0x3e)
LSM6DS3_FIFO_DATA_OUT_H        = const(0x3f)
LSM6DS3_TIMESTAMP0_REG         = const(0x40)
LSM6DS3_TIMESTAMP1_REG         = const(0x41)
LSM6DS3_TIMESTAMP2_REG         = const(0x42)
LSM6DS3_STEP_TIMESTAMP_L       = const(0x49)
LSM6DS3_STEP_TIMESTAMP_H       = const(0x4a)
LSM6DS3_STEP_COUNTER_L         = const(0x4b)
LSM6DS3_STEP_COUNTER_H         = const(0x4c)
LSM6DS3_SENSORHUB13_REG        = const(0x4d)
LSM6DS3_SENSORHUB14_REG        = const(0x4e)
LSM6DS3_SENSORHUB15_REG        = const(0x4f)
LSM6DS3_SENSORHUB16_REG        = const(0x50)
LSM6DS3_SENSORHUB17_REG        = const(0x51)
LSM6DS3_SENSORHUB18_REG        = const(0x52)
LSM6DS3_FUNC_SRC               = const(0x53)
LSM6DS3_TAP_CFG                = const(0x58)
LSM6DS3_TAP_THS_6D             = const(0x59)
LSM6DS3_INT_DUR2               = const(0x5a)
LSM6DS3_WAKE_UP_THS            = const(0x5b)
LSM6DS3_WAKE_UP_DUR            = const(0x5c)
LSM6DS3_FREE_FALL              = const(0x5d)
LSM6DS3_M1_CFG                 = const(0x5e)
LSM6DS3_M2_CFG                 = const(0x5f)
LSM6DS3_OUT_MAG_RAW_X_L        = const(0x66)
LSM6DS3_OUT_MAG_RAW_X_H        = const(0x67)
LSM6DS3_OUT_MAG_RAW_Y_L        = const(0x68)
LSM6DS3_OUT_MAG_RAW_Y_H        = const(0x69)
LSM6DS3_OUT_MAG_RAW_Z_L        = const(0x6a)
LSM6DS3_OUT_MAG_RAW_Z_H        = const(0x6b)

#Embedded functions registers

LSM6DS3_SLV0_ADD               = const(0x02)
LSM6DS3_SLV0_SUBADD            = const(0x03)
LSM6DS3_SLV0_CONFIG            = const(0x04)
LSM6DS3_SLV1_ADD               = const(0x05)
LSM6DS3_SLV1_SUBADD            = const(0x06)
LSM6DS3_SLV1_CONFIG            = const(0x07)
LSM6DS3_SLV2_ADD               = const(0x08)
LSM6DS3_SLV2_SUBADD            = const(0x09)
LSM6DS3_SLV2_CONFIG            = const(0x0a)
LSM6DS3_SLV3_ADD               = const(0x0b)
LSM6DS3_SLV3_SUBADD            = const(0x0c)
LSM6DS3_SLV3_CONFIG            = const(0x0d)
LSM6DS3_DATAWRITE_SRC_MODE_SUB_SLV0 = const(0x0e)
LSM6DS3_PEDO_THS_REG           = const(0x0f)
LSM6DS3_SM_THS                 = const(0x13)
LSM6DS3_PEDO_DEB_REG           = const(0x14)
LSM6DS3_STEP_COUNT_DELTA       = const(0x15)
LSM6DS3_MAG_SI_XX              = const(0x24)
LSM6DS3_MAG_SI_XY              = const(0x25)
LSM6DS3_MAG_SI_XZ              = const(0x26)
LSM6DS3_MAG_SI_YX              = const(0x27)
LSM6DS3_MAG_SI_YY              = const(0x28)
LSM6DS3_MAG_SI_YZ              = const(0x29)
LSM6DS3_MAG_SI_ZX              = const(0x2a)
LSM6DS3_MAG_SI_ZY              = const(0x2b)
LSM6DS3_MAG_SI_ZZ              = const(0x2c)
LSM6DS3_MAG_OFFX_L             = const(0x2d)
LSM6DS3_MAG_OFFX_H             = const(0x2e)
LSM6DS3_MAG_OFFY_L             = const(0x2f)
LSM6DS3_MAG_OFFY_H             = const(0x30)
LSM6DS3_MAG_OFFZ_L             = const(0x31)
LSM6DS3_MAG_OFFZ_H             = const(0x31)

LSM6DS3_TEMPERATURE_SENSITIVITY = const(16)
LSM6DS3_TEMPERATURE_OFFSET      = 25.0
