#!usr/bin/env python
#coding:utf-8

import string

sentence = "this is a pen"
words = sentence.split(" ")

for word in words:
	print word

print string.join(words, " ||| ")

