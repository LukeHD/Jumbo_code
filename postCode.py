from datetime import datetime
import requests

from bufferCode import Bme, Mpu, Neo, session
from helper import sensors, getClassByName, getClassAttrsByClassName

# --- creating global variables used for posting

postIndices = [1, 1, 1]

url = 'https://project-jumbo.de/backend/api/'


# --- functions to save and load the postIndices from a file

def writeIndices():
    with open('indexFile.txt', 'w') as file:
        for listitem in postIndices:
            file.write('%s\n' % listitem)


def readIndices():
    with open('indexFile.txt', 'r') as file:
        if not file.read(1):
            return [1, 1, 1]
        else:
            file.seek(0, 0)
            lines = file.readlines()
            return [int(lines[i]) if i < len(lines) else 1 for i in range(3)]


print(readIndices())

postIndices = readIndices()
if postIndices == [1, 1, 1]:
    writeIndices()


# --- declaring functions for posting the measurements to the webserver

def post(name):
    sensorIndex = sensors.index(name)
    capName = name.capitalize()
    upperName = name.upper()

    print(upperName, postIndices[sensorIndex])
    dataSet = session.query(getClassByName(capName)).get(postIndices[sensorIndex])
    if dataSet is not None:
        dataVar = {attr: getattr(dataSet, attr) for attr in getClassAttrsByClassName(capName) if attr != 'id' and attr != 'metadata'}
        dataVar['time'] = dataVar['time'].timestamp()
        print(dataVar)
        try:
            req = requests.request('POST', url+name, data=dataVar, timeout=1)
            print(upperName, 'POST Status:', req.status_code)
            if req.status_code == 200:
                print(req.text)
                postIndices[sensorIndex] += 1
                writeIndices()
                post(name)
        except ConnectionError:
            pass
