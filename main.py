from bufferCode import pushData
from postCode import postBme, postMpu
import time
from sensors import neo6m
from multiprocessing import Process

def loopMain():
    while True:
        pushData()
        postBme()
        postMpu()
        time.sleep(10)

if __name__=="__main__":
    Process(target=loopMain).start()
    Process(target=neo6m.loopGPS).start()