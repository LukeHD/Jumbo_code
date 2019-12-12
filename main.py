from sqlalchemy import create_engine
from sqlalchemy import Table, Column, Integer, String, DateTime, MetaData, ForeignKey
from sqlalchemy import select
from sqlalchemy.sql import and_, or_, not_
from datetime import datetime as dt
from sensors.bme280 import readBME280All
from sensors.mpu6050 import getMpuData

import random # not necessary later on!!!

engine = create_engine('sqlite:///saves.db', echo=True)
conn = engine.connect()

metadata = MetaData()
bme = Table('bme-280', metadata,
    Column('id', Integer, primary_key=True),
    Column('time', DateTime, default=dt.now()),

    Column('temperature', Integer),
    Column('humidity', Integer),
    Column('pressure', Integer),
)

mpu = Table('mpu-6050', metadata,
    Column('id', Integer, primary_key=True),
    Column('time', DateTime, default=dt.now()),

    Column('gyroscope_x', Integer),
    Column('gyroscope_y', Integer),
    Column('gyroscope_z', Integer),

    Column('acceleration_x', Integer),
    Column('acceleration_y', Integer),
    Column('acceleration_z', Integer),

    Column('rot_x', Integer),
    Column('rot_y', Integer)
)
metadata.create_all(engine)

def push_data():
    bmeVal = readBME280All()
    ins = bme.insert().values(
        temperature = bmeVal[0],
        humidity = bmeVal[1],
        pressure = bmeVal[2]
    )

    try:
        result = conn.execute(ins)
        print('\nAdded id: ', result.inserted_primary_key[0], ' to the bme table with values: ')
        for val in ins.compile().params:
            print(val, ': ', ins.compile().params[val])
        print()
    except Exception as e:
        print("\nWasn't able to add to the bme table!")
        print(e, "\n")

    mpuVal = getMpuData()
    ins = mpu.insert().values(
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
        result = conn.execute(ins)
        print('\nAdded id: ', result.inserted_primary_key[0], ' to the mpu table with values: ')
        for val in ins.compile().params:
            print(val, ': ', ins.compile().params[val])
        print()
    except Exception as e:
        print("\nWasn't able to add to the mpu table!")
        print(e, "\n")

# def get_data():
#     try:
#         s = select([values])
#         result = conn.execute(s)
#         for row in result:
#             print()
#             for columns in values.c:
#                 print(columns.name, ": ", row[columns])
#         print()

#     except Exception as e:
#         print("\nWasn't able to read data!")
#         print(e, "\n")

# def remove_data(id_arg):
#     to_delete = values.delete().where(values.c.id == id_arg)
#     conn.execute(to_delete)
    
#     #---optional
#     try: 
#         s = select([values])
#         result = conn.execute(s)
#         a = 0
#         for row in result:
#             a+=1
#         if id_arg>a:
#             print("\nNo dataset was deleted, because the index was out of range.\n")
#     except Exception as e:
#         print (e)

def main():
    push_data()

if __name__=="__main__":
    main()