import os
import serial
import time



ser = serial.Serial(
    port = '/dev/ttyS0',
    baudrate=115200,
    parity=serial.PARITY_NONE,
    bytesize=serial.EIGHTBITS,
    stopbits=serial.STOPBITS_ONE,
    timeout=1
)


def send_pico_message(message):
    print("Sedning pi -> pico....")
    ser.write(message.encode('utf-8'))


while True:
    send_pico_message("hello")
    time.sleep(2)