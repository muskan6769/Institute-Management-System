from sqlalchemy import create_engine
import cx_Oracle
password='Sweet130118'
host='localhost'
port=1522
sid='orcl1'
user='system'

sid = cx_Oracle.makedsn(host,port,sid=sid)

cstr = 'oracle://{user}:{password}@{sid}'.format(
    user=user,
    password=password,
    sid=sid
)

engine =  create_engine(
    cstr,
    convert_unicode=False,
    pool_recycle=10,
    pool_size=50,
    echo=True
)

r = engine.execute('select * from Tab_Student')

for row in r:
    print(row)




