from datetime import datetime
import requests

from bufferCode import Bme, Mpu, Neo6m, session

# --- creating global variables used for posting

postIndices = [1, 1, 1]

# url = 'http://192.168.137.245:5000/api/raspi/'
url = 'http://192.168.178.71:5000/api/raspi/'

# --- functions to save and load the postIndices from a file

def writeIndices():
    with open('indexFile.txt', 'w') as file:
        for listitem in postIndices:
            file.write('%s\n' % listitem)
    
def readIndices():
    with open('indexFile.txt', 'r') as file:
        if not file.read(1):
            return [1, 1, 1]
        tmp = []
        for line in file:
            tmp.append(1)
        print(tmp)
        return tmp

postIndices = readIndices()
if postIndices == [1, 1, 1]:
    writeIndices()

# --- declaring functions for posting the measurements to the webserver

def postBme():
    print("BME", postIndices[0])
    dataSet = session.query(Bme).get(postIndices[0])
    if dataSet is not None:
        data = {
            'time': datetime.strftime(dataSet.time, '%Y-%m-%d %H:%M:%S'),
            'temperature': dataSet.temperature,
            'humidity': dataSet.humidity,
            'pressure': dataSet.pressure
        }
        try:
            r = requests.put(url+'bme', params=data, auth=('Lukas Brennauer', 'a'))
            print('BME PUT STATUS:', r.status_code)
            if r.status_code == 200:
                postIndices[0] += 1
                writeIndices()
                postBme()
        except:
            pass

def postMpu():
    print("MPU", postIndices[1])
    dataSet = session.query(Mpu).get(postIndices[1])
    if dataSet is not None:
        data = {
            'time': datetime.strftime(dataSet.time, '%Y-%m-%d %H:%M:%S'),
            'gyroscope_x': dataSet.gyroscope_x,
            'gyroscope_y': dataSet.gyroscope_y,
            'gyroscope_z': dataSet.gyroscope_z,
            'acceleration_x': dataSet.acceleration_x,
            'acceleration_y': dataSet.acceleration_y,
            'acceleration_z': dataSet.acceleration_z,
            'rot_x': dataSet.rot_x,
            'rot_y': dataSet.rot_y
        }
        try:
            r = requests.put(url+'mpu', params=data, auth=('Lukas Brennauer', 'a'))
            print('MPU PUT STATUS:', r.status_code)
            if r.status_code == 200:
                postIndices[1] += 1
                writeIndices()
                postMpu()
        except:
            pass

# --- declaring a function for posting the location to the webserver

def postGPS():
    print("NEO6M", postIndices[2])
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
                writeIndices()
                postGPS()
        except:
            pass
    
