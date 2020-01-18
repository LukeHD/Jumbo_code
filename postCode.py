from datetime import datetime
import requests

from bufferCode import Bme, Mpu, session

postIndices = [1, 1]
url = 'http://192.168.2.105:5000/api/raspi/'

def postBme():
    print(postIndices[0])
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
                postBme()
        except:
            pass

def postMpu():
    print(postIndices[1])
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
                postMpu()
        except:
            pass
    
