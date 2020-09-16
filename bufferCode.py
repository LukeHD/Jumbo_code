from datetime import datetime as dt
from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from sensors.bme280 import readBME280All
from sensors.mpu6050 import getMpuData

engine = create_engine('sqlite:///saves.db', echo=False)

Base = declarative_base()
Session = sessionmaker(bind=engine)
session = Session()


# --- Declaring the database classes/tables

class Bme(Base):
    __tablename__ = 'bme'

    id = Column(Integer, primary_key=True)
    time = Column(DateTime, default=dt.now())
    temp = Column(Integer)
    hum = Column(Integer)
    press = Column(Integer)


class Mpu(Base):
    __tablename__ = 'mpu'

    id = Column(Integer, primary_key=True)
    time = Column(DateTime, default=dt.now())
    gyro_x = Column(Integer)
    gyro_y = Column(Integer)
    gyro_z = Column(Integer)
    acc_x = Column(Integer)
    acc_y = Column(Integer)
    acc_z = Column(Integer)
    rot_x = Column(Integer)
    rot_y = Column(Integer)


class Neo(Base):
    __tablename__ = 'neo'

    id = Column(Integer, primary_key=True)
    time = Column(DateTime, default=dt.now())
    pos = Column(String)


def getClassByName(name):
    return globals()[name]


# --- creating the file if it doesn't exist already

Base.metadata.create_all(engine)


# --- declaring the functions for buffering the measurements

def buffer(name, vals):
    try:
        ins = getClassByName(name.capitalize())(**vals)
        session.add(ins)
        session.commit()
        print('buffered', name)
    except Exception as e:
        print("\nWasn't able to add to the", name, "table!", e)


def bufferData():
    bmeVal = readBME280All()
    buffer("bme", {
        "time": dt.now(),
        "temp": bmeVal[0],
        "press": bmeVal[1],
        "hum": bmeVal[2]
    })

    mpuVal = getMpuData()
    buffer("mpu", {
        "time": dt.now(),
        "gyro_x": mpuVal[0][0],
        "gyro_y": mpuVal[0][1],
        "gyro_z": mpuVal[0][2],
        "acc_x": mpuVal[1][0],
        "acc_y": mpuVal[1][1],
        "acc_z": mpuVal[1][2],
        "rot_x": mpuVal[2][0],
        "rot_y": mpuVal[2][1]
    })
