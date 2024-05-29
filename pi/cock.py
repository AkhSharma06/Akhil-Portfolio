import serial
ser = serial.Serial ("/dev/ttyAMA0")    #Open named port 
ser.baudrate = 115200 #Set baud rate to 9600
data = ser.read(10) 