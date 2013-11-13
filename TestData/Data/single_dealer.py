##from datetime import *
#coding=utf8
import os
import sys
import time
import json
import re
import http.cookiejar
from urllib.request import urlopen
from urllib.request import quote
from datetime import date

#access token用于调用新浪微博API
access_token = '2.00TvZUzBlxpd6C604d7c8acb06pVnE'
#当抓取json失败时，下次尝试的时间间隔
sleeptime = 5
#API返回的结果数上限，适用于爬取用户微博及关注
INF = 2000

name_to_uid = {}

#get a info of one group, using input as x, A, B, C
def get_group_info(x,A,B,C):
    fx=open('info_x.txt','w')
    info=get_user_info_from_uid(x)
    if(info==''):
        return False
    fx.write(info+'\n')
    fx.close()
    ###
    fA=open('info_A.txt','w')
    for a in A:
        info=get_user_info_from_uid(a)
        if(info==''):
            continue
        fA.write(info+'\n')
    fA.close()
    ###
    fB=open('info_B.txt','w')
    for b in B:
        info=get_user_info_from_uid(b)
        if(info==''):
            continue
        fB.write(info+'\n')
    fB.close()
    ###
    fC=open('info_C.txt','w')
    for c in C:
        info=get_user_info_from_uid(c)
        if(info==''):
            continue
        fC.write(info+'\n')
    fC.close()


def get_user_tag(uid):
    ans=''
    base_url = 'https://api.weibo.com/2/tags.json?'
    complete_url = base_url + 'uid=' + uid + '&' + 'access_token=' + access_token
    raw_json = ''
    try:
        raw_json = urlopen(complete_url).read().decode('utf8')
    except Exception as e:
        ##print (e)
        print ('exception!\n' + complete_url)
        time.sleep(sleeptime)
        try:
            raw_json = urlopen(complete_url).read().decode('utf8')
        except:
            time.sleep(sleeptime)
            try:
                raw_json = urlopen(complete_url).read().decode('utf8')
            except:
                print ('shit!!!!')
                ans=''
                return ans
    json_data = json.loads(raw_json)
    for a in json_data:
        weight=0
        tag=''
        for key in a:
            if(key=='weight'):
                weight=a[key]
            else:
                tag=a[key]
        ans=ans+' '+tag
    return ans
def get_user_info_from_uid(uid):
    print(uid)
    ans=''
    base_url = 'https://api.weibo.com/2/users/show.json?'
    complete_url = base_url + 'uid=' + uid + '&' + 'access_token=' + access_token
    raw_json = ''
    try:
        raw_json = urlopen(complete_url).read().decode('utf8')
    except Exception as e:
        ##print (e)
        print ('exception!\n' + complete_url)
        time.sleep(sleeptime)
        try:
            raw_json = urlopen(complete_url).read().decode('utf8')
        except:
            time.sleep(sleeptime)
            try:
                raw_json = urlopen(complete_url).read().decode('utf8')
            except:
                print ('shit!!!!')
                return ''
    json_data = json.loads(raw_json)
    #在这里添加需要的数据域
    if(str(json_data['gender'])!="m" and str(json_data['gender'])!="f"):
        print("Not a human!\n")
        return ''
    ans+=(str(json_data['id']) )
    ans+=('\t')
    ans+=(json_data['screen_name'].replace('\n', '').replace('"', '').encode('GBK', 'ignore').decode('GBK', 'ignore'))
    ans+=('\t')
    ans+=(json_data['name'].replace('\n', '').replace('"', '').encode('GBK', 'ignore').decode('GBK', 'ignore'))
    ans+=('\t')
    ans+=(str(json_data['gender']))
    ans+=('\t')
    ans+=(str(json_data['province']))
    ans+=('\t')
    ans+=(str(json_data['city']))
    ans+=('\t')
    ans+=(str(json_data['location']))
    ans+=('\t')
    ans+=get_user_tag(uid)
    return ans
