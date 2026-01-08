from esp_ble_uart import *
import time

name = 'ESP32-ble-uart'
UUID_UART = '6E400001-B5A3-F393-E0A9-E50E24DCCA9E'
UUID_TX = '6E400003-B5A3-F393-E0A9-E50E24DCCA9E'
UUID_RX = '6E400002-B5A3-F393-E0A9-E50E24DCCA9E'

uart = Bleuart(name, UUID_UART, UUID_TX, UUID_RX)

uart.close()
val_rx = ""

def rec_rx():
    global val_rx
    val_rx = uart.read().decode().strip()
    print('on rx: ', val_rx)               # Interruption : display data received

uart.irq(handler=rec_rx)

def send_tx(val_tx):
    uart.write(str(val_tx) + '\n')
    print("tx", val_tx)

while True:
    if len(val_rx):
        print("msg: ",val_rx)
        val_rx =""
    if uart.isConnected():
        send_tx("xxx")                     # xxx data to be sent in string format
        # val_rx_int = int(val_rx[:-1])      # to be used if data received is an integer

    time.sleep_ms(1000)
      
