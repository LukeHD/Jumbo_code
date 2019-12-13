import datetime
import time


while True:
    now = datetime.datetime.now()
    print (now.strftime('%d.%m.%Y') + '  ' + now.strftime('%H:%M:%S'))
    time.sleep(2)