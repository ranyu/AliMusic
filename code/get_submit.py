#!/usr/bin/env python
# coding=utf-8
import glob

with open('../submit/mars_tianchi_artist_plays_predict.csv','w') as fw:
    for s in glob.glob('../test/*'):
        song_name = s.split('/')[-1].split('_')[0]
        with open(s,'r') as f:
            for data in f:
                content = data.strip().split(',')
                date = content[0]
                play_number = content[1]
                fw.write(song_name+','+str(int(round(float(play_number))))+','+date+'\n')
