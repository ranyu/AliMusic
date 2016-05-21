#!/usr/bin/env python
# coding=utf-8
#The code is drawing the play number each singer

import glob
import pylab as pl
for s in glob.glob('../play_number/*.csv'):
    print s
    singer_number = s.split('/')[-1].split('.')[0]
    X = []
    Y = []
    with open(s,'r') as f:
        f.readline()
        for data in f:
            content = data.strip().split(',')
            X.append(content[0])
            Y.append(content[1])
    xtext = pl.xlabel(u'时间')
    ytext = pl.ylabel(u'播放量')
    ttext = pl.title(u'歌手播放量')
    pl.plot_date(pl.datestr2num(X), Y, linestyle='-')  
    pl.grid(True)
    pl.savefig('../figure/'+singer_number+'.jpg')
    #pl.show()
