#coding=utf8
import MySQLdb
f=open('ori_user_info.txt')
conn=MySQLdb.connect(host='localhost',user='root',passwd='9261adoni',port=3306)
cur=conn.cursor()
try:
    cur.execute('drop database shasha')
except:
    print("Database didn't exist!")
conn.commit()
cur.execute('create database if not exists shasha default charset=utf8')
conn.select_db('shasha')
cur.execute('create table users(uid varchar(100), name varchar(100), screenname varchar(100), gender char, province varchar(100), city varchar(100), location varchar(100), tags varchar(100)) default charset=utf8')
cur.execute("SET NAMES utf8")
cur.execute("SET CHARACTER_SET_CLIENT=utf8")
cur.execute("SET CHARACTER_SET_RESULTS=utf8")
conn.commit()
userid=1
for l in f:
    l=l.replace('\n','')
    l=l.split('\t')
    l[0]=str(userid)
    if(l[7]==""):
        continue
    cur.execute('insert into users values(%s,%s,%s,%s,%s,%s,%s,%s)',l)
    userid+=1
conn.commit()
cur.close()
conn.close()

