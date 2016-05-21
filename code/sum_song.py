#!/usr/bin/env python
# coding=utf-8
# The code is for sum the song for a singer every day

import glob
for s in glob.glob('../feature/song_action_info_*'):
    value_dic = {}
    print s.split('_')[-1]
    with open(s,'r') as f:
        f.readline()
        for data in f:
            content = data.strip().split(',')
            #print content
            key = content[4]
            value = content[-1]
            if key not in value_dic:
                value_dic.setdefault(key,0)
            value_dic[key] += int(value)
            #print key
    #print value_dic
    #print sorted(value_dic)
    with open('../play_number/'+s.split('_')[-1],'w') as fw:
        fw.write('Date,play\n')
        for ele in sorted(value_dic):
            fw.write(ele+','+str(value_dic[ele])+'\n')
    #raw_input()
