import xlrd
import pymysql
import sys

def get_database():
    conn = pymysql.connect(host='112.125.122.106',
                           user='root',
                           password='257586',
                           db='gsdb',
                           charset='utf8')
    # 创建游标
    cursor = conn.cursor()
    return conn,cursor


def close_database(conn, cursor):
    cursor.close()
    conn.close()


path=sys.argv[1]
sum=int(sys.argv[2])
conn,cursor=get_database()
sql0="SELECT MAX(id) FROM lajiinfo;"
sql = 'insert into lajiinfo(id,name,type) VALUE (%s,%s,%s)'
workbook=xlrd.open_workbook(path)
table=workbook.sheet_by_name("lajiinfo")
cursor.execute(sql0)
id=cursor.fetchone()[0]
if id==None:
    id=0
for i in range(1,sum+1):
    id=id+1
    for j in range(0,2):
        if j==0:
            name = table.cell_value(i, j)
        elif j==1:
            type = table.cell_value(i, j)
    data=[id,name,type]
    cursor.execute(sql,data)
    conn.commit()
close_database(conn,cursor)
