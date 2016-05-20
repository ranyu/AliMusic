#!/usr/bin/env python
# coding=utf-8
# The code simply analysis data

song_set = set()
artist_set = set()
with open('./231531/mars_tianchi_songs.csv','r') as f:
    for data in f:
        print data
        content = data.strip().split(',')
        print content
        song_set.add(content[0])
        artist_set.add(content[1])
print song_set
print len(song_set)
print artist_set
print len(artist_set)
with open('./231531/mars_tianchi_user_actions.csv','r') as f:
    for data in f:
        #print data
        content = data.strip().split(',')
        #print content
        song_set.add(content[1])
print len(song_set)
