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

def get_All_Friends_from_uid(uid):
    friends=[]
    base_url = 'https://api.weibo.com/2/friendships/friends/bilateral/ids.json?'
    complete_url = base_url + 'uid=' + uid + '&count=400' + '&access_token=' + access_token
    raw_json = ''
    try:
        raw_json = urlopen(complete_url).read().decode('utf8')
    except Exception as e:
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
    for friend_id in json_data['ids']:
        friends.append(str(friend_id))
    return friends

#########################################
def get_joint_friends(uid1,uid2):
    joint_friends=[]
    base_url = 'https://api.weibo.com/2/friendships/friends/in_common.json?'
    complete_url = base_url + 'uid=' + uid1 + '&' + 'suid=' + uid2+'&' + 'access_token=' + access_token
    raw_json = ''
    try:
        raw_json = urlopen(complete_url).read().decode('utf8')
    except Exception as e:
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
    for user in json_data['users']:
        joint_friends.append(str(user["id"]))
    return joint_friends

############################
def choose_the_weightest(dictB, weight):
    B=set()
    l=weight
    if(l>len(dictB)):
        l=len(dictB)
    sorted_Set=sorted(dictB.items(), key=lambda d:d[1], reverse = True)
    for i in range(0,l):
        B.add(sorted_Set[i][0])
    return B

############################
def get_A_B_C_from_friend_to_file(friends,uid):
    print("==================")
    setA=set()
    setB=set()
    setC=set()
    dictB=dict()
    temp_setC=set()
    for friend_id in friends:
        if(friend_id in setA):
            continue
        joint_friends=get_joint_friends(friend_id,uid)
        if(joint_friends==[]):
            continue
        setA.add(friend_id)
        for joint_id in joint_friends:
            if(not joint_id in dictB):
                dictB[joint_id]=1
            else:
                dictB[joint_id]+=1
        temp_setC.update(set(get_All_Friends_from_uid(friend_id)))
    weight=100
    setB=choose_the_weightest(dictB,weight)
    each_C_num=2
    j=0
    for f in temp_setC:
        if(f in dictB):
            continue
        else:
            j+=1
            setC.add(f)
        if(j>3*len(setA)):
            break
    print(setB)
    f=open("TestData.txt","a")
    f.write(uid)
    f.write('\n')
    for i in setA:
        f.write(i+'\t')
    f.write('\n')
    for i in setB:
        f.write(i+'\t')
    f.write('\n')
    for i in setC:
        f.write(i+'\t')
    f.write('\n')
    f.write('==========================================\n')

#########################################
def get_A_B_C_from_X_file(fin):
    fp = open(fin)
    num=0
    MaxNum=100
    for uid in fp:
        if(num>MaxNum):
            continue
        uid = uid.replace('\n', '')
        friends=get_All_Friends_from_uid(uid)
        if(len(friends)<100):
            continue
        num+=1
        #print(num)
        get_A_B_C_from_friend_to_file(friends,uid)

if (__name__ == '__main__'):
    get_A_B_C_from_X_file("train_uid.txt")
