from bufferCode import Bme, Mpu, Neo, session
import datetime as dt
import string
import random


for i in range(50):
    # ins = Bme(
    # 	time = dt.datetime.now(),
    # 	temp = i+2,
    # 	hum = i+3,
    # 	press = i+4
    # )

    # ins = Mpu(
    # 	time=dt.datetime.now(),
    # 	gyro_x=i+1,
    # 	gyro_y=i+2,
    # 	gyro_z=i+3,
    # 	acc_x=i+4,
    # 	acc_y=i+5,
    # 	acc_z=i+6,
    # 	rot_x=i+7,
    # 	rot_y=i+8
    # )

    posStr = ""
    for _i in range(25):
        posStr += random.choice(string.ascii_letters + string.digits + string.punctuation)
    ins = Neo(
        time=dt.datetime.now(),
        pos=posStr
    )

    session.add(ins)
    session.commit()
