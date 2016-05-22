#!/usr/bin/env python
# coding=utf-8
#The code is drawing the play number each singer

import glob
import pylab as pl
import os
os.system('rm -r ../figure')
os.system('mkdir ../figure')

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
    xtext = pl.xlabel(u'Time')
    ytext = pl.ylabel(u'Play number')
    ttext = pl.title(u'Play number each singer')
    pl.plot_date(pl.datestr2num(X), Y, linestyle='-')  
    pl.grid(True)
    pl.savefig('../figure/'+singer_number+'.png')
    pl.show()
