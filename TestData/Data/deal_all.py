import os
allfiles=set([])
for root,dirs,files in os.walk('./alldata'):
    allfiles=set(files)
f=open('TestData.txt').readlines()
for i in range(0,int(len(f)/5)):
    x=f[i*5].replace('\n','')
    print(x)
    p='./alldata/'
    fx=p+x+'_info_x.txt'
    fA=p+x+'_info_A.txt'
    fB=p+x+'_info_B.txt'
    fC=p+x+'_info_C.txt'
    os.system('./data_processing.cpp.out '+fx+' '+fA+' '+fB+' '+fC)
