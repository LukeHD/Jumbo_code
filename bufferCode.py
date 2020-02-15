from datetime import datetime as dt
from sqlalchemy import create_engine
from sqlalchemy import Table, Column, Integer, String, DateTime, MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from sensors.bme280 import readBME280All
from sensors.mpu6050 import getMpuData

engine = create_engine('sqlite:///saves.db', echo=False)

Base = declarative_base()
Session = sessionmaker(bind=engine)
session = Session()

class Bme(Base):
    __tablename__ = 'bme'
    
    id = Column(Integer, primary_key=True)
    time = Column(DateTime, default=dt.now())

    temperature = Column(Integer)
    humidity = Column(Integer)
    pressure = Column(Integer)

class Mpu(Base):
    __tablename__ = 'mpu'

    id = Column(Integer, primary_key=True)
    time = Column(DateTime, default=dt.now())

    gyroscope_x = Column(Integer)
    gyroscope_y = Column(Integer)
    gyroscope_z = Column(Integer)

    acceleration_x = Column(Integer)
    acceleration_y = Column(Integer)
    acceleration_z = Column(Integer)

    rot_x = Column(Integer)
    rot_y = Column(Integer)

Base.metadata.create_all(engine)

def pushData():
    bmeVal = readBME280All()
    ins = Bme(
        time = dt.now(),
        temperature = bmeVal[0],
        pressure = bmeVal[1],
        humidity = bmeVal[2]
    )
    try:
        session.add(ins)
        session.commit()
        print('buffered bme')
    except:
        print("\nWasn't able to add to the bme table!")

    mpuVal = getMpuData()
    ins = Mpu(
        time = dt.now(),
        gyroscope_x = mpuVal[0][0],
        gyroscope_y = mpuVal[0][1],
        gyroscope_z = mpuVal[0][2],

        acceleration_x = mpuVal[1][0],
        acceleration_y = mpuVal[1][1],
        acceleration_z = mpuVal[1][2],

        rot_x = mpuVal[2][0],
        rot_y = mpuVal[2][1]
    )

    try:
        session.add(ins)
        session.commit()
        print('buffered mpu')
    except:
        ("\nWasn't able to add to the mpu table!")

