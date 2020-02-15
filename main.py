from bufferCode import pushData
from postCode import postBme, postMpu
import time
from sensors import neo6m
from multiprocessing import Process

# --- declaring a function for the main loop (-> buffering and posting BME and MPU data)

def loopMain():
    while True:
        pushData()
        postBme()
        postMpu()
        time.sleep(10)

if __name__=="__main__":

    # --- running the main loop and gps loop simultaneously

    Process(target=loopMain).start()
    Process(target=neo6m.loopGPS).start()
