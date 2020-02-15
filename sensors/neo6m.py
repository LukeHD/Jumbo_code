import serial
import time
import datetime
import RPi.GPIO as GPIO
from bufferCode import pushGPS
from postCode import url, postIndices

# --- declaring a loop for the GPS serial stream

def bufferAndPostGPS():
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

            else:   
                print (dataStr)
                pushGPS(dataStr)
                if not lastHadConnection:
                    lastHadConnection = True
                    file1.write('\n---------------- Connected: ' + now.strftime('%d.%m.%Y' "   " '%H:%M:%S') + ' ----------------\n\n')

                GPIO.output(23, GPIO.HIGH)
                file1.write(dataStr + '\n')  
            file1.close()
            postGPS()
            time.sleep(3)
            
            
# --- declaring a function for posting the location to the webserver

def postGPS():
    print(postIndices[2])
    dataSet = session.query(Neo6m).get(postIndices[2])
    if dataSet is not None:
        data = {
            'time': datetime.strftime(dataSet.time, '%Y-%m-%d %H:%M:%S'),
            'data': dataSet
        }
        try:
            r = requests.put(url+'neo', params=data, auth=('Lukas Brennauer', 'a'))
            print('NEO PUT STATUS:', r.status_code)
            if r.status_code == 200:
                postIndices[2] += 1
                postNeo()
        except:
            pass
