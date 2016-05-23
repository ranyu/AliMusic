#!/usr/bin/env python
# coding=utf-8
import sys

result = 0
with open(sys.argv[1],'r') as f:
    for data in f:
        result += float(data.strip().split()[0])
print result
