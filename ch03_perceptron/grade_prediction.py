#!/usr/bin/env python
#coding:utf-8
#
# Author: Peinan ZHANG
#

def grade_prediction(gold_file, test_file):
  ans = [line.split("\t")[0] for line in open(gold_file)]
  for line in open(test_file):
    line = line.strip()
    

if __name__ == '__main__':
  import sys
  grade_prediction(sys.argv[1], sys.argv[2])