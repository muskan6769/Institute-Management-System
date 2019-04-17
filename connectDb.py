from sqlalchemy import create_engine
import cx_Oracle
password=''
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
print(r)
for row in r:
    print(row)

#reg_password = engine.execute("select * from Student_Tab where Roll_No = :a",{'a':'IIT2017046'})
reg_password = engine.execute("select Password from Student_Tab where Roll_No = :a",{'a':'IIT2017046'})
for row in reg_password:
    print(row)



