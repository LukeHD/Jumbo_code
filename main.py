from bufferCode import bufferData
from postCode import post
import time
from sensors import neo6m
from multiprocessing import Process


# --- declaring a function for the main loop (-> buffering and posting BME and MPU data)

def mainLoop():
    while True:
        bufferData()
        post("bme")
        post("mpu")
        time.sleep(10)


if __name__ == "__main__":

    # --- running the main loop and gps loop simultaneously

    Process(target=mainLoop).start()
    Process(target=neo6m.bufferAndPostGPS).start()
