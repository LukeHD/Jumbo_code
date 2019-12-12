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
lastHadConnection = False
file1.write('\n---------------------- ' + now.strftime('%d.%m.%Y' "  " '%H:%M:%S') + ' ----------------------\n')
file1.write('--------------------- No satellite connected ---------------------\n\n')
file1.close()

while True:
    data = ser.readline()

    if data[0:6] == b'$GPRMC':
        dataStr = data.decode('utf-8')[0:-2]
        dataArr = dataStr.split(",")
        file1 = open("dataTest.txt","a")
        if dataArr[2] == 'V':
            print ('No Connection')
            if lastHadConnection:
                lastHadConnection = False
                now = datetime.now()
                file1.write('\n------------- Connection lost: ' + now.strftime('%d.%m.%Y' "   " '%H:%M:%S') + ' -------------\n\n')
            GPIO.output(23, GPIO.LOW)
            GPIO.output(24, GPIO.HIGH)
        else:   
            print (dataStr)
            if not lastHadConnection:
                lastHadConnection = True
                file1.write('\n---------------- Connected: ' + now.strftime('%d.%m.%Y' "   " '%H:%M:%S') + ' ----------------\n\n')
            GPIO.output(24, GPIO.LOW)
            GPIO.output(23, GPIO.HIGH)
            file1.write(dataStr + '\n')  
        file1.close()
        time.sleep(3)          
