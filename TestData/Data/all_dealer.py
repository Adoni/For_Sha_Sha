import single_dealer
import os

f=open('TestData.txt').readlines()
files=[]
for root,dirs,ff in os.walk('./alldata'):
    files=ff
for i in range(0,int(len(f)/5)):
    if(i<(len(files)/4-1)):
        continue
    x=f[i*5].replace('\n','')
    A=f[i*5+1].split('\t')
    B=f[i*5+2].split('\t')
    tempC=f[i*5+3].split('\t')
    l=len(B)
    if(l>len(tempC)):
        l=len(tempC)
    C=[]
    for j in range(0,l):
        C.append(tempC[j])
    print(x)
    if(single_dealer.get_group_info(x,A,B,C)):
        print("Get Successed!")
    else:
        print("Error At Get Single Group Info!")
