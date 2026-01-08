from esp_ble_uart import *
from time import *

name = 'ESP32-esp-ble-uart'
UUID_UART = '6E400001-B5A3-F393-E0A9-E50E24DCCA9E'
UUID_TX = '6E400003-B5A3-F393-E0A9-E50E24DCCA9E'
UUID_RX = '6E400002-B5A3-F393-E0A9-E50E24DCCA9E'

uart = Bleuart(name, UUID_UART, UUID_TX, UUID_RX)
uart.close()

# Function to send some data
def send(val_tx):
    uart.write(str(val_tx))  
    print("send tx = ", val_tx)


while True:
    send("abc")       
    sleep_ms(500)
    send(12)
    sleep_ms(500) 
