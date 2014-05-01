#!/usr/bin/env python
#coding:utf-8
#
# Author: Peinan ZHANG
#

import sys
from collections import defaultdict

count_of = defaultdict(lambda: 0)
for line in open(sys.argv[1], "r"):
	words = line.strip().split(" ")
	for word in words:
		count_of[word] += 1

for k, v in sorted(count_of.items(), key = lambda x: x[1], reverse = True):
	print "%s: %d" % (k, v)