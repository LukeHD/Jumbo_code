from sqlalchemy import create_engine
from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey
from sqlalchemy import select
from sqlalchemy.sql import and_, or_, not_

engine = create_engine('sqlite:///test.db', echo=True)

metadata = MetaData()
users = Table('users', metadata,
    Column('id', Integer, primary_key=True),
    Column('name', String),
    Column('fullname', String),
)

addresses = Table('addresses', metadata,
    Column('id', Integer, primary_key=True),
    Column('user_id', None, ForeignKey('users.id')),
    Column('email_address', String, nullable=False)
)

metadata.create_all(engine)

ins = users.insert()
print (str(ins))
ins = users.insert().values(name='jack', fullname='Jack Jones')
print (str(ins))
print (ins.compile().params)

conn = engine.connect()
print (conn)

result = conn.execute(ins)
print (result.inserted_primary_key)

ins = users.insert()
result2 = conn.execute(ins, id=2, name='wendy', fullname='Wendy Williams')
print (result2.inserted_primary_key)

conn.execute(addresses.insert(), [
    {'user_id': 1, 'email_address' : 'jack@yahoo.com'},
    {'user_id': 1, 'email_address' : 'jack@msn.com'},
    {'user_id': 2, 'email_address' : 'www@www.org'},
    {'user_id': 2, 'email_address' : 'wendy@aol.com'},
])

s = select([users])
result = conn.execute(s)
for row in result:
    print (row)

#result = conn.execute(s)
#row = result.fetchone()
#print("name:", row[users.c.name], "; fullname:", row[users.c.fullname])

for row in conn.execute(s):
    print("name:", row[users.c.name], "; fullname:", row[users.c.fullname])
result.close()

s = select([users.c.name, users.c.fullname])
result = conn.execute(s)
for row in result:
    print("name:", row[users.c.name], "; fullname:", row[users.c.fullname])

for row in conn.execute(select([users, addresses])):
    print(row)

s = select([users, addresses]).where(users.c.id == addresses.c.user_id)
result = conn.execute(s)
for row in result:
    print (row)

print(and_(
    users.c.name.like('j%'),
    users.c.id == addresses.c.user_id,
    or_(
        addresses.c.email_address == 'wendy@aol.com',
        addresses.c.email_address == 'jack@yahoo.com'
    ),
    not_(users.c.id > 5)
    )
)
