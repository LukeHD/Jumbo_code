from sqlalchemy import create_engine
from sqlalchemy import Table, Column, Integer, String, DateTime, MetaData, ForeignKey
from sqlalchemy import select
from sqlalchemy.sql import and_, or_, not_
from datetime import datetime as dt
import random # not necessary later on!!!

engine = create_engine('sqlite:///saves.db', echo=True)
conn = engine.connect()

metadata = MetaData()
values = Table('values', metadata,
    Column('id', Integer, primary_key=True),
    Column('time', DateTime, default=dt.now()),

    Column('temperature', Integer),
    Column('humidity', Integer),
    Column('pressure', Integer),
)

metadata.create_all(engine)

def get_T():
    return random.randrange(-15, 30)

def get_P():
    return random.randrange(900, 1100)

def get_H():
    return random.randrange(0, 100)

def push_data():
    ins = values.insert().values(
        temperature = get_T(),
        humidity = get_H(),
        pressure = get_P()
    )

    try:
        result = conn.execute(ins)
        print("\nResult was added as with id: ", result.inserted_primary_key, " and values: ")
        for val in ins.compile().params:
            print(val, ": ", ins.compile().params[val])
        print()
    except Exception as e:
        print("\nWasn't able to add data!")
        print(e, "\n")

def get_data():
    try:
        s = select([values])
        result = conn.execute(s)
        for row in result:
            print()
            for columns in values.c:
                print(columns.name, ": ", row[columns])
        print()

    except Exception as e:
        print("\nWasn't able to read data!")
        print(e, "\n")

def remove_data(id_arg):
    to_delete = values.delete().where(values.c.id == id_arg)
    conn.execute(to_delete)
    
    #---optional
    try: 
        s = select([values])
        result = conn.execute(s)
        a = 0
        for row in result:
            a+=1
        if id_arg>a:
            print("\nNo dataset was deleted, because the index was out of range.\n")
    except Exception as e:
        print (e)

def main():
    remove_data(15)
    get_data()

if __name__=="__main__":
    main()