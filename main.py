from bufferCode import pushData
from postCode import postBme, postMpu
import time 

def main():
    while True:
        pushData()
        postBme()
        postMpu()
        time.sleep(10)

if __name__=="__main__":
    main()