#!/usr/bin/env python
#coding:utf-8
#
# Author:  Peinan ZHANG
#

import sys
from collections import defaultdict

def train_bigram(train_file):
  count_of         = defaultdict(lambda: 0)
  context_count_of = defaultdict(lambda: 0)

  for line in open(train_file, 'r'):
    words = line.strip().split(' ')
    words.insert(0, '<s>')
    words.append('</s>')
    for i in range(1, len(words)):
      bigram = "%s %s" % (words[i - 1], words[i])
      count_of[bigram]               += 1
      context_count_of[words[i - 1]] += 1
      count_of[words[i]]             += 1
      context_count_of[""]           += 1

  for ngram, count in sorted(count_of.items()):
    words = ngram.split(' ')
    words.pop()
    if len(words) > 0:
      context = words[0]
    else:
      context = ''
    prob = float(count_of[ngram]) / context_count_of[context]
    # print ngram, prob
    print '%s\t%.6f' % (ngram, prob)


if __name__ == '__main__':
  train_bigram(sys.argv[1])