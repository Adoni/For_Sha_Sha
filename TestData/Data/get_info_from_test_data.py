##from datetime import *
#coding=utf8
#it is used to get user information from the TestData which is produced by get_A_B_C_from_X
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

#根据用户id获取用户信息，输出到fname中
def get_user_info(id, fname):
    fp = open(fname, 'a')
    base_url = 'https://api.weibo.com/2/users/show.json?'
    complete_url = base_url + 'uid=' + id + '&' + 'access_token=' + access_token
    raw_json = ''
    try:
        raw_json = urlopen(complete_url).read().decode('utf8')
    except Exception as e:
##        print (e)
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
    fp.write(str(json_data['id']) )
    fp.write('\t')
    fp.write(str(json_data['idstr']) )
    fp.write('\t')
    fp.write(json_data['screen_name'].replace('\n', '').replace('"', '').encode('GBK', 'ignore').decode('GBK', 'ignore'))
    fp.write('\t')
    fp.write(json_data['name'].replace('\n', '').replace('"', '').encode('GBK', 'ignore').decode('GBK', 'ignore'))
    fp.write('\t')
    fp.write(str(json_data['province']) )
    fp.write('\t')
    fp.write(str(json_data['city']) )
    fp.write('\t')
    fp.write(str(json_data['location']))
    fp.write('\t')
    x = json_data['description'].replace('\n', '').replace('"', '').encode('GBK', 'ignore').decode('GBK', 'ignore')
    if (x == ''):
        x = 'null'
    fp.write(x)
    fp.write('\t')
    x = str(json_data['domain'])
    if (x == ''):
        x = 'null'
    fp.write(x)
    fp.write('\t')
    x = str(json_data['weihao'])
    if (x == ''):
        x = 'null'
    fp.write(x)
    fp.write('\t')
    fp.write(str(json_data['gender']))
    fp.write('\t')
    fp.write(str(json_data['followers_count']))
    fp.write('\t')
    fp.write(str(json_data['friends_count']))
    fp.write('\t')
    fp.write(str(json_data['statuses_count']))
    fp.write('\t')
    fp.write(str(json_data['favourites_count']))
    fp.write('\t')
    fp.write(str(json_data['created_at']))
    fp.write('\t')
    fp.write(str(json_data['following']))
    fp.write('\t')
    fp.write(str(json_data['verified']))
    fp.write('\t')
    fp.write(str(json_data['verified_type']))
    fp.write('\t')
    x = json_data['verified_reason'].replace('\n', '').replace('"', '').encode('GBK', 'ignore').decode('GBK', 'ignore')
    if (x == ''):
        x = 'null'
    fp.write(x)
    fp.write('\t')
    fp.write(str(json_data['bi_followers_count']) )
    fp.write('\n')
###################

