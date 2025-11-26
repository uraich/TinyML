from micropython import const
from machine import Pin,I2C
from utime import sleep_ms
from LSM6DS3_const import *


class LSM6DS3(object):
    
    def __init__(self):
        pass

    def readByte(self,register):
        return self.readBytes(register,1)[0]

    def writeByte(self,register,value):
        tmp =bytearray(1)
        tmp[0] = value
        self.writeBytes(register,tmp)

    def readShort(self,register):
        tmp = self.readBytes(register,2)
        return self.bytesToShort(tmp)

    def writeShort(self,register,value):
        tmp = self.shortToBytes(value)
        self.writeBytes(register,tmp)
        
    def readBits(self, register, bit_position, no_of_bits):
        '''!
        Reads a number of bits from the register
        @param bit_position: the left most position of the bit field
        @param no_of_bits: the number of bits in the bit field
        '''
        tmp = self.readByte(register)
        # print("Who am I register unshifted raw: 0x{:02x}".format(tmp))
        mask = 1
        for i in range(1,no_of_bits):
            mask = mask << 1 | 1
        shift = bit_position - no_of_bits + 1
        mask <<= shift        
        # print("mask: 0x{:02x}".format(mask))
        tmp &= mask
        return tmp >> shift

    def readBit(self,register,bit_position) :
        '''!
        Reads a single bit from the register
        @param register: reguster address from which the bit is read
        @param bit_position: the left most position of the bit field
        '''
        tmp=self.readByte(register)
        if tmp & (1 << bit_position) :
            return True
        else:
            return False
        
    def writeBits(self, register, bit_position, no_of_bits, value):
        '''!
        Writes a number of bits to the register
        @param bit_position: the left most position of the bit field
        @param no_of_bits: the number of bits in the bit field
        @param value: the value to be written
        '''        
        tmp = self.readByte(register)
        if self.debug:
            print("Register 0x{:02x} raw: 0x{:02x}".format(register,tmp))
        mask = 1
        for i in range(1,no_of_bits):
            mask = mask << 1 | 1
        shift = bit_position - no_of_bits + 1
        mask <<= shift
        # if self.debug:
        #     print("mask: 0x{:02x}".format(mask))
        mask = ~ mask
        tmp &= mask
        tmp |= value <<shift
        if self.debug:
            print("Writing 0x{:02x} to register 0x{:02x}".format(tmp,register))
        self.writeByte(register,tmp)

    def writeBit(self,register,bit_position,value):
        '''!
        Writes single bit to the register
        @param bit_position: the left most position of the bit field
        @param no_of_bits: the number of bits in the bit field
        @param value: the value to be written
        '''               
        tmp = self.readByte(register)
        if self.debug:
            print("writeBit: Original content of register 0x{:02x} : 0x{:02x}".format(register,tmp))
        if value:
            tmp |= (1 << bit_position)
        else:
            tmp &= ~(1 << bit_position)
        if self.debug:
            print("writeBit: New content of register 0x{:02x} : 0x{:02x}".format(register,tmp))
        self.writeByte(register,tmp)
        
    def bytesToShort(self,bytes):
        '''!
        The lsm6Ds3 returns 16 bit signed values in 2 bytes. The bytes are joined and the resulting value
        converted to a Python integer
        @ param hi: the most significant 8 bits or the value
        @ param lo: the low significant bits
        @ return the signed integer value
        '''
        val = (bytes[1] << 8 ) | bytes[0]
        # if self.debug:
        #     print("value: 0x{:04x}".format(val))
        if not val & 0x8000:           # positive 16 bit value
            # if self.debug:
            #     print ("positive value: {:d}".format(val))
            return val
        else:
            val = -((val ^ 0xffff) + 1)
            # if self.debug:
            #     print("negative value: {:d} ".format(val)) 
            return val

    def shortToBytes(self,value) :
        tmp = pack('>h', value)
        # if self.debug:
            # print("16 bit value: 0x{:02x}{:02x}".format(tmp[0],tmp[1]))
        return tmp

    @property
    def debugging(self) -> bool:
        return self.debug
    
    @debugging.setter
    def debugging(self,onOff):
        '''!
        set the debugging flag
        @param onOff: sets the debug flag
        '''
        if onOff:
            print("Switch debug on")
        self.debug = onOff

    @property
    def temperature(self) -> float:
        """Temperature in Celsius"""
        # Data from Datasheet Table 4.3
        # Temp range -40 to 85 Celsius
        # T_ADC_RES = ADC Res 16 bit
        # Stabilization time 500 μs

        self.raw_temp_data = self.readShort(LSM6DS3_OUT_TEMP_L)
        if self.debug:
            print("Raw temperature data 0x{:04x} {:d}".format(self.raw_temp_data,self.raw_temp_data))
        temp =  self.raw_temp_data / LSM6DS3_TEMPERATURE_SENSITIVITY + LSM6DS3_TEMPERATURE_OFFSET
        if self.debug:
            print("Temperature:  {:4.2f}°C".format(temp))
        return temp
    
    # WHO_AM_I register
    @property
    def getDeviceID(self) -> int:
        '''!
        Get Device ID.
        This register is used to verify the identity of the device (0b01101001, 0x69).
        @return Device ID 
        @see LSM6DS3_WHO_AM register
        '''

        return self.readByte(LSM6DS3_WHO_AM_I)
    
    # CTRL1_XL
    
    @property
    def ctrl1_xl(self) -> int:
        return self.readByte(LSM6DS3_CTRL1_XL)

    @ctrl1_xl.setter
    def ctrl1_xl(self,value) -> int:
        self.writeByte(LSM6DS3_CTRL1_XL,value)
        
    @property
    def acc_odr(self) -> int:
        return self.readBits(LSM6DS3_CTRL1_XL,OUTPUT_RATE_POS,OUTPUT_RATE_SIZE)

    @acc_odr.setter
    def acc_odr(self,odr_str):
        '''!
        Set the accelerometer datarate
        @see LSM6DS3_CTRL1_XL register
        '''
        odr = lsm6ds3_odr[odr_str]
        if self.debug:
            print("acc odr value: 0x{:02x}".format(odr))
        self.writeBits(LSM6DS3_CTRL1_XL,OUTPUT_RATE_POS,OUTPUT_RATE_SIZE,odr)

    def acc_odr_txt(self,odr_number) -> str:
        odr = self.readBits(LSM6DS3_CTRL1_XL,OUTPUT_RATE_POS,OUTPUT_RATE_SIZE)
        lsm6dr3_odr_reverse = {v: k for k, v in lsm6ds3_odr.items()}
        return lsm6dr3_odr_reverse[odr_number]
    
    def acc_odr_value(self,odr_string):
        odr_split = odr_string.split(' ')
        value = float(odr_split[0])
        if odr_split[1] == "kHz":
            value *= 1000
        return value
        
    @property
    def acc_full_scale(self) -> int:
        return self.readBits(LSM6DS3_CTRL1_XL,ACC_FULL_SCALE_POS,ACC_FULL_SCALE_SIZE)

    @acc_full_scale.setter
    def acc_full_scale(self,full_scale_str):
        full_scale = lsm6dr3_acc_full_scale[full_scale_str]
        self.writeBits(LSM6DS3_CTRL1_XL,ACC_FULL_SCALE_POS,ACC_FULL_SCALE_SIZE,full_scale)

    def acc_full_scale_txt(self,full_scale_number):
        # reverse key and value in the dictionary
        lsm6dr3_acc_full_scale_reverse = {v: k for k, v in lsm6dr3_acc_full_scale.items()}
        return lsm6dr3_acc_full_scale_reverse[full_scale_number]

    @property
    def acc_bandwidth(self) -> int:
        return self.readBits(LSM6DS3_CTRL1_XL,ACC_BANDWIDTH_POS,ACC_BANDWIDTH_SIZE)

    @acc_bandwidth.setter
    def acc_bandwidth(self,acc_bandwidth_str):
        bandwidth = lsm6ds3_acc_bw[acc_bandwidth_str]
        if self.debug:
            print("setting accelerometer bandwidth to 0x{:02x}".format(bandwidth))
        self.writeBits(LSM6DS3_CTRL1_XL,ACC_BANDWIDTH_POS,ACC_BANDWIDTH_SIZE,bandwidth)

    def acc_bandwidth_txt(self,acc_bandwidth_number):
        # reverse key and value in the dictionary
        lsm6dr3_acc_bw_reverse = {v: k for k, v in lsm6ds3_acc_bw.items()}
        return lsm6dr3_acc_bw_reverse[acc_bandwidth_number]        

    # CTRL2_G
    
    @property
    def ctrl2_g(self) -> int:
        return self.readByte(LSM6DS3_CTRL2_G)

    @ctrl2_g.setter
    def ctrl2_g(self,value) -> int:
        self.writeByte(LSM6DS3_CTRL2_G,value)
        
    @property
    def gyro_odr(self) -> int:
        return self.readBits(LSM6DS3_CTRL2_G,OUTPUT_RATE_POS,OUTPUT_RATE_SIZE)

    @acc_odr.setter
    def gyro_odr(self,odr_str):
        '''!
        Set the gyroscope datarate
        @see LSM6DS3_CTRL2_G register
        '''
        odr = lsm6ds3_odr[odr_str]
        if self.debug:
            print("gyro odr value: 0x{:02x}".format(odr))
        self.writeBits(LSM6DS3_CTRL2_G,OUTPUT_RATE_POS,OUTPUT_RATE_SIZE,odr)

    
    def gyro_odr_txt(self,odr_number) -> str:
        # odr = self.readBits(LSM6DS3_CTRL2_G,OUTPUT_RATE_POS,OUTPUT_RATE_SIZE)
        # lsm6dr3_gyro_odr_reverse = {v: k for k, v in lsm6ds3_odr.items()}
        # return lsm6dr3_gyro_odr_reverse[odr_number]
        return self.acc_odr_txt(odr_number)
    
    def gyro_odr_value(self,odr_string):
        return self.acc_odr_value(odr_string)
        
    @property
    def gyro_full_scale(self) -> int:
        return self.readBits(LSM6DS3_CTRL2_G,GYRO_FULL_SCALE_POS,GYRO_FULL_SCALE_SIZE)

    @gyro_full_scale.setter
    def gyro_full_scale(self,full_scale_str):
        full_scale = lsm6ds3_gyro_full_scale[full_scale_str]
        self.writeBits(LSM6DS3_CTRL2_G,GYRO_FULL_SCALE_POS,GYRO_FULL_SCALE_SIZE,full_scale)

    def gyro_full_scale_txt(self,full_scale_number):
        # reverse key and value in the dictionary
        lsm6ds3_gyro_full_scale_reverse = {v: k for k, v in lsm6ds3_gyro_full_scale.items()}
        return lsm6ds3_gyro_full_scale_reverse[full_scale_number]

    @property
    def gyro_125_dps(self):
        return self.readBit(LSM6DS3_CTRL2_G,LSM6DS3_GYRO_125_DPS)
    
    @gyro_125_dps.setter
    def gyro_125_dps(self,state):
        self.writeBit(LSM6DS3_CTRL2_G,LSM6DS3_GYRO_125_DPS,state)

    # CTRL7_G
    
    @property
    def ctrl7_g(self) -> int:
        return self.readByte(LSM6DS3_CTRL7_G)

    @ctrl7_g.setter
    def ctrl7_g(self,value) -> int:
        self.writeByte(LSM6DS3_CTRL7_G,value)
        
    @property
    def status_reg(self):
        return(self.readBytes(LSM6DS3_STATUS_REG))

    @property
    def temperature_data_available(self):
        return self.readBit(LSM6DS3_STATUS_REG,LSM6DS3_TDA)

    @property
    def gyro_data_available(self):
        return self.readBit(LSM6DS3_STATUS_REG,LSM6DS3_GDA)

    @property
    def acc_data_available(self):
        return self.readBit(LSM6DS3_STATUS_REG,LSM6DS3_XLDA)
                
    # read raw accelerometer data
    @property
    def acc_x_raw(self):
        return self.readShort(LSM6DS3_OUTX_L_XL)

    @property
    def acc_y_raw(self):
        return self.readShort(LSM6DS3_OUTY_L_XL)

    @property
    def acc_z_raw(self):
        return self.readShort(LSM6DS3_OUTZ_L_XL)

    @property
    def acc_raw(self):
        return ((self.readShort(LSM6DS3_OUTX_L_XL),
                 self.readShort(LSM6DS3_OUTY_L_XL),
                 self.readShort(LSM6DS3_OUTZ_L_XL)))

    def acc_to_physical(self,raw_acc_data):
        full_scale = lsm6ds3_acc_full_scale_convert[self.acc_full_scale]
        physical_data = float(raw_acc_data*full_scale)/float(0x7fff)
        if self.debug:
            print("raw_data: {:d}".format(raw_data))
            print("Full scale: {:d} g".format(full_scale))
            print("physical_data: {:6.4f}".format(physical_data))
        return physical_data
    
    @property
    def acc_x(self):
        return self.acc_to_physical(self.acc_x_raw)
    
    @property
    def acc_y(self):
        return self.acc_to_physical(self.acc_y_raw)
    
    @property
    def acc_z(self):
        return self.acc_to_physical(self.acc_z_raw)
    
    @property
    def acc(self):
        return ((self.acc_x,self.acc_y,self.acc_z))

    # read raw gyroscope data
    @property
    def gyro_x_raw(self):
        return self.readShort(LSM6DS3_OUTX_L_G)
    @property
    def gyro_y_raw(self):
        return self.readShort(LSM6DS3_OUTY_L_G)
    @property
    def gyro_z_raw(self):
        return self.readShort(LSM6DS3_OUTZ_L_G)

    @property
    def gyro_raw(self):
        return ((self.readShort(LSM6DS3_OUTX_L_G),
                 self.readShort(LSM6DS3_OUTY_L_G),
                 self.readShort(LSM6DS3_OUTZ_L_G)))

    def gyro_to_physical(self,raw_data):
        full_scale = lsm6ds3_gyro_full_scale_convert[self.gyro_full_scale]
        physical_data = float(raw_data*full_scale)/float(0x7fff)
        if self.debug:
            print("raw gyro data: {:d}".format(raw_data))
            print("Full scale: {:d} g".format(full_scale))
            print("physical_data: {:6.4f}".format(physical_data))
        return physical_data
        
    @property
    def gyro_x(self):
        return  self.gyro_to_physical(self.gyro_x_raw)

    @property
    def gyro_y(self):
        return  self.gyro_to_physical(self.gyro_y_raw)

    @property
    def gyro_z(self):
        return  self.gyro_to_physical(self.gyro_z_raw)

    @property
    def gyro(self):
        return ((self.gyro_x,self.gyro_y,self.gyro_z))

    @property
    def ctrl3_c(self):
        return self.readByte(LSM6DS3_CTRL3_C)

    @ctrl3_c.setter
    def ctrl3_c(self,value):
        self.writeByte(LSM6DS3_CTRL3_C,value)

    def sw_reset(self):
        self.writeBit(LSM6DS3_CTRL3_C,LSM6DS3_SW_RESET,LSM6DS3_ENABLE)
                      
    def boot(self):
        self.writeBit(LSM6DS3_CTRL3_C,LSM6DS3_BOOT,LSM6DS3_ENABLE)

    @property
    def bdu(self):
        return self.readBit(LSM6DS3_CTRL3_C,LSM6DS3_BDU)

    @bdu.setter
    def bdu(self,onOff):
        self.writeBit(LSM6DS3_CTRL3_C,LSM6DS3_BDU,onOff)
        
    @property
    def if_add_inc(self):
        return self.readBit(LSM6DS3_CTRL3_C,LSM6DS3_IF_ADD_INC)

    @if_add_inc.setter
    def if_add_inc(self,onOff):
        self.writeBit(LSM6DS3_CTRL3_C,LSM6DS3_IF_ADD_INC,onOff)

    @property
    def ble(self):
        return self.readBit(LSM6DS3_CTRL3_C,LSM6DS3_BLE)

    @ble.setter
    def ble(self,onOff):
        self.writeBit(LSM6DS3_CTRL3_C,LSM6DS3_BLE,onOff)    

    # FIFO control
    # FIFO_CTRL1 and 2
    
    @property
    def fifo_ctrl1(self):
        return self.readByte(LSM6DS3_FIFO_CTRL1)
    
    @property
    def fifo_ctrl2(self):
        return self.readByte(LSM6DS3_FIFO_CTRL2)   

    @property
    def fifo_threshold(self):
        thr_lower  = self.readByte(LSM6DS3_FIFO_CTRL1)
        thr_higher = self.readBits(LSM6DS3_FIFO_CTRL2,
                                   FIFO_THRESHOLD_UPPER_POS,
                                   FIFO_THRESHOLD_UPPER_SIZE)
        return (thr_higher << 8) | thr_lower
    
    @fifo_threshold.setter
    def fifo_threshold(self,value):
        thr_lower  = value & 0xff
        thr_higher = (value & 0xf00) >> 8
        self.writeByte(LSM6DS3_FIFO_CTRL1,value)
        self.writeBits(LSM6DS3_FIFO_CTRL2,
                       FIFO_THRESHOLD_UPPER_POS,
                       FIFO_THRESHOLD_UPPER_SIZE,
                       thr_higher)

    # FIFO_CTRL3
    @property
    def fifo_ctrl3(self):
        return self.readByte(LSM6DS3_FIFO_CTRL3)

    @property
    def fifo_acc_dec_factor(self):
        return self.readBits(LSM6DS3_FIFO_CTRL3,
                             ACC_FIFO_DECIM_POS,
                             ACC_FIFO_DECIM_SIZE)
    @fifo_acc_dec_factor.setter
    def fifo_acc_dec_factor(self,decimation_factor):
        self.writeBits(LSM6DS3_FIFO_CTRL3,
                   ACC_FIFO_DECIM_POS,
                   ACC_FIFO_DECIM_SIZE,
                   lsm6ds3_dec_factor[decimation_factor])

    def fifo_acc_dec_factor_txt(self,code):
        # reverse key and value in the dictionary
        lsm6dr3_dec_factor_reverse = {v: k for k, v in lsm6ds3_dec_factor.items()}
        return lsm6dr3_dec_factor_reverse[code]        

    @property
    def fifo_gyro_dec_factor(self):
        return self.readBits(LSM6DS3_FIFO_CTRL3,
                             GYRO_FIFO_DECIM_POS,
                             GYRO_FIFO_DECIM_SIZE)
    @fifo_gyro_dec_factor.setter
    def fifo_gyro_dec_factor(self,decimation_factor):
        self.writeBits(LSM6DS3_FIFO_CTRL3,
                   GYRO_FIFO_DECIM_POS,
                   GYRO_FIFO_DECIM_SIZE,
                   lsm6ds3_dec_factor[decimation_factor])

    def fifo_gyro_dec_factor_txt(self,code):
        return self.fifo_acc_dec_factor_txt(code)        
        
    # FIFO_CTRL4
    @property
    def fifo_ctrl4(self):
        return self.readByte(LSM6DS3_FIFO_CTRL4)
    
    # FIFO_CTRL5
    @property
    def fifo_ctrl5(self):
        return self.readByte(LSM6DS3_FIFO_CTRL5)

    @fifo_ctrl5.setter
    def fifo_ctrl5(self,value):
        self.writeByte(LSM6DS3_FIFO_CTRL5,value)


    @property    
    def fifo_odr(self):
        return self.readBits(LSM6DS3_FIFO_CTRL5,FIFO_ODR_POS,FIFO_ODR_SIZE)

    def fifo_odr_txt(self,odr_number):
        return self.acc_odr_txt(odr_number)
        
    @fifo_odr.setter
    def fifo_odr(self,odr_str):
        self.writeBits(LSM6DS3_FIFO_CTRL5,
                       FIFO_ODR_POS,
                       FIFO_ODR_SIZE,
                       lsm6ds3_odr[odr_str])

    @property
    def fifo_mode(self):
        return self.readBits(LSM6DS3_FIFO_CTRL5,FIFO_MODE_POS,FIFO_MODE_SIZE)
    
    @fifo_mode.setter
    def fifo_mode(self,mode_str):
        self.writeBits(LSM6DS3_FIFO_CTRL5,
                       FIFO_MODE_POS,
                       FIFO_MODE_SIZE,
                       lsm6ds3_fifo_mode[mode_str])
    
    def fifo_mode_txt(self,fifo_mode_number):
        # reverse key and value in the dictionary
        lsm6dr3_fifo_mode_reverse = {v: k for k, v in lsm6ds3_fifo_mode.items()}
        return lsm6dr3_fifo_mode_reverse[fifo_mode_number]
    
    # FIFO status registers
    # FIFO_STATUS1 and 2

    @property
    def fifo_status1(self):
        return self.readByte(LSM6DS3_FIFO_STATUS1)

    @property
    def fifo_status2(self):
        return self.readByte(LSM6DS3_FIFO_STATUS2)

    @property
    def words_in_fifo(self):
        number_high = self.readByte(LSM6DS3_FIFO_STATUS2) & 0xf
        number_low  = self.readByte(LSM6DS3_FIFO_STATUS1)
        return (number_high << 8) | number_low
    
    @property
    def fifo_watermark_reached(self):
        return self.readBit(LSM6DS3_FIFO_STATUS2,FIFO_WATERMARK_REACHED)

    @property
    def fifo_overrun(self):
        return self.readBit(LSM6DS3_FIFO_STATUS2,FIFO_OVERRUN)

    @property
    def fifo_full(self):
        return self.readBit(LSM6DS3_FIFO_STATUS2,FIFO_FULL)

    @property
    def fifo_empty(self):
        return self.readBit(LSM6DS3_FIFO_STATUS2,FIFO_EMPTY)

    @property
    def fifo_data(self):
        return self.readShort(LSM6DS3_FIFO_DATA_OUT_L)

    #FIFO_STATUS3 and 4
    @property
    def fifo_status3(self):
        return self.readByte(LSM6DS3_FIFO_STATUS3)

    @property
    def fifo_status4(self):
        return self.readByte(LSM6DS3_FIFO_STATUS4)

    @property
    def fifo_pattern(self):
        return (self.fifo_status4 & 3) << 8 | self.fifo_status3

    @property
    def fifo_status1(self):
        return self.readByte(LSM6DS3_FIFO_STATUS1)
