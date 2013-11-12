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

def get_user_tag(uid, fname):
    fp = open(fname, 'a')
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
                fp.write('\n')
                fp.close()
                return false
    json_data = json.loads(raw_json)
    for a in json_data:
        weight=0
        tag=''
        for key in a:
            if(key=='weight'):
                weight=a[key]
            else:
                tag=a[key]
        fp.write(' %s'%(tag))
    fp.write("\n")
    fp.close()
def get_user_info_from_file(fin, fout):
    fp = open(fin)
    i=0
    for uid in fp:
        uid = uid.replace('\n', '')
        get_user_info(uid, fout)
        get_user_tag(uid, fout)
        i+=1
        print(i)
def get_user_info(id, fname):
    fp = open(fname, 'a')
    base_url = 'https://api.weibo.com/2/users/show.json?'
    complete_url = base_url + 'uid=' + id + '&' + 'access_token=' + access_token
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
                return
    json_data = json.loads(raw_json)
    #在这里添加需要的数据域
    if(str(json_data['gender'])!="m" and str(json_data['gender'])!="f"):
        print("Not a human!\n")
        return
    fp.write(str(json_data['id']) )
    fp.write('\t')
    fp.write(json_data['screen_name'].replace('\n', '').replace('"', '').encode('GBK', 'ignore').decode('GBK', 'ignore'))
    fp.write('\t')
    fp.write(json_data['name'].replace('\n', '').replace('"', '').encode('GBK', 'ignore').decode('GBK', 'ignore'))
    fp.write('\t')
    fp.write(str(json_data['gender']))
    fp.write('\t')
    fp.write(str(json_data['province']))
    fp.write('\t')
    fp.write(str(json_data['city']))
    fp.write('\t')
    fp.write(str(json_data['location']))
    fp.write('\t')
if (__name__ == '__main__'):
    get_user_info_from_file('train_uid.txt', 'ori_user_info.txt')
    print ('2 done')
