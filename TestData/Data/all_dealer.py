import single_dealer

f=open('TestData.txt').readlines()
for i in range(0,int(len(f)/5)):
    x=f[i*5].replace('\n','')
    A=f[i*5+1].split('\t')
    B=f[i*5+2].split('\t')
    C=f[i*5+3].split('\t')
    if(single_dealer.get_group_info(x,A,B,C)):
        print("Get Successed!")
        break
    else:
        print("Error At Get Single Group Info!")
