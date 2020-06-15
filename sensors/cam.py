from picamera import PiCamera
from time import sleep

camera = PiCamera()
camera.resolution = (2592, 1944)
n=0

def takeImage():
    global n
    n = n + 1 
    camera.capture('/home/pi/Documents/Jumbo_code/cam/image' + str(n) +'.jpg')

while True:
    takeImage()
    sleep(3)