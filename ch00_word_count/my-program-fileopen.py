#!usr/bin/env python
#coding:utf-8

import sys
import string

my_file = open(sys.argv[1], "r")

# for line in my_file:
# 	line = line.strip()
# 	if len(line) != 0:
# 		print line

for line in my_file:
	line = line.strip()
	words = line.split(" ")
# 	print words

print string.join(words, " ||| ")
