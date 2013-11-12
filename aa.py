#coding=utf8
import MySQLdb
f=open('ori_user_info.txt')
ff=open('aim.txt','w')
userid=1
ids=set([3,11,67,132,297,24,38,47,74,7,9])
for l in f:
    l=l.replace('\n','')
    l=l.split('\t')
    l[0]=str(userid)
    if(l[7]==""):
        continue
    if(not userid in ids):
        print(userid)
        userid+=1
        continue
    for s in l:
        ff.write(s+'\t')
    userid+=1
    ff.write('\n')
f.close()
ff.close()
