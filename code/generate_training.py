#!/usr/bin/env python
# coding=utf-8
# The code is generate the raw feature of training data

import glob
from collections import Counter
import os

#load data to csv
def load_data(filename):
    fw = open('song_info.csv','w')
    fw.write('song_Id,publish_time,song_init_plays,language,gender\n')
    for song in glob.glob(filename+'/*/song_info'):
        with open(song,'r') as f:
            for data in f:
                content = data.strip().split()
                #print content
                #quit()
                for el in content[1:-1]:
                    fw.write(el+',')
                fw.write(content[-1]+'\n')
    fw.close()
    fw = open('action_info.csv','w')
    fw.write('song_Id,user_Id,gmt_create,action_type,Ds\n')
    for j,user in enumerate(glob.glob(filename+'/*/action_info')):
        song_id = user.split('/')[-2]
        with open(user,'r') as f:
            for data in f:
                content = data.strip().split()
                fw.write(song_id)
                for el in content:
                    fw.write(','+el)
                fw.write('\n')

# sort action info by date
def sorted_data():
    action_dic = {}
    with open('action_info.csv','r') as f:
        head_line = f.readline()
        for data in f:
            content = data.strip().split(',')
            if content[-1] not in action_dic:
                action_dic.setdefault(content[-1],[])
            s = ''
            for i in content[:-2]:
                s += i + ','
            s += content[-2]
            action_dic[content[-1]].append(s)
    with open('action_info_sorted.csv','w') as f:
        f.write(head_line)
        for ele in sorted(action_dic):
            for action_ele in action_dic[ele]:
                f.write(action_ele+','+ele)
                f.write('\n')
#combine song_info and user_info
def ensemble_data():
    action_playtime_dic = {} #play number one song in same day 
    action_type_dic = {} #type one song in same day
    with open('action_info_sorted.csv','r') as f:
        f.readline()
        for data in f:
            content = data.strip().split(',')
            key = content[0]+','+content[-1]
            if key not in action_playtime_dic:
                action_playtime_dic.setdefault(key,[])
                action_type_dic.setdefault(key,[])
            action_playtime_dic[key].append(content[-3])
            action_type_dic[key].append(content[-2])
    #ensemble data start
    visited = []
    fw_en = open('action_info_ensemble.csv','w')
    with open('action_info_sorted.csv','r') as f:
        #fw_en.write('song_Id,user_Id,gmt_create_total,action_type1,action_type2,action_type3,Ds\n')
        fw_en.write('song_Id,gmt_create_total,action_type1,action_type2,action_type3,Ds\n')
        f.readline()
        for i,data in enumerate(f):
            content = data.strip().split(',')
            key = content[0]+','+content[-1]
            if key in visited:
                continue
            #fw_en.write(content[0]+','+content[1]+',')
            fw_en.write(content[0]+',')
            visited.append(key)
            count1 = Counter(action_playtime_dic[content[0]+','+content[-1]])
            count2 = Counter(action_type_dic[content[0]+','+content[-1]])
            sum_time = 0
            for q in count1:
                sum_time += int(q) * int(count1[q])
            fw_en.write(str(sum_time)+',')
            for num in xrange(1,4):
                if str(num) not in count2:
                    fw_en.write(str(0)+',')
                else:
                    fw_en.write(str(count2[str(num)])+',')
            fw_en.write(content[-1])
            fw_en.write('\n')
    fw_en.close()
    os.system('rm ./action_info.csv')
    os.system('rm ./action_info_sorted.csv')

def combine_data(filename):
    fw = open('../feature/song_action_info_'+filename+'.csv','w')
    #fw.write('song_Id,user_Id,gmt_create_total,action_type1,action_type2,action_type3,Ds,publish_time,song_init_plays,language,gender\n')
    fw.write('song_Id,gmt_create_total,action_type2,action_type3,Ds,publish_time,song_init_plays,language,gender,action_type1\n')
    song_dic = {}
    with open('./song_info.csv','r') as f:
        f.readline()
        for data in f:
            content = data.strip().split(',')
            st = ''
            for el in content[1:-1]:
                st += el+','
            st += content[-1]
            song_dic.setdefault(content[0],st)
    #print song_dic
    with open('./action_info_ensemble.csv','r') as f:
        f.readline()
        for data in f:
            #print data
            content = data.strip().split(',')
            #print content
            for el in content[:2]:
                fw.write(el+',')
            for el in content[3:]:
                fw.write(el+',')
            fw.write(song_dic[content[0]])
            fw.write(','+content[2])
            fw.write('\n')
    fw.close()
def main():
    for filename in glob.glob('../data/old_data/*'):
        print filename
        load_data(filename)
        sorted_data()
        ensemble_data()
        combine_data(filename.split('/')[-1])

if __name__ == "__main__":
    main()
