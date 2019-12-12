import serial
import time
import datetime
import RPi.GPIO as GPIO

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(23, GPIO.OUT)
GPIO.setup(24, GPIO.OUT)

ser = serial.Serial("/dev/serial0", baudrate = 9600, timeout = 0.5)

file1 = open("dataTest.txt","a")
now = datetime.datetime.now()
file1.write('\n' + '---------- ' + now.strftime('%d.%m.%Y') + '  ' + now.strftime('%H:%M:%S') + ' ----------' + '\n' + '\n')
file1.close()

while True:
    data = ser.readline()

    if data[0:6] == b'$GPRMC':
        dataStr = data.decode('utf-8')[0:-2]
        dataArr = dataStr.split(",")
        file1 = open("dataTest.txt","a")
        if dataArr[2] == 'V':
            file1.write("no satellite data available" + '\n')
            print ("no satellite data available")
            GPIO.output(23, GPIO.LOW)
            GPIO.output(24, GPIO.HIGH)
        else:    
            file1.write(dataStr + '\n')
            print (dataStr)
            GPIO.output(24, GPIO.LOW)
            GPIO.output(23, GPIO.HIGH)
        file1.close()
        #time.sleep(2)
    else:
        time.sleep(1)          
 
