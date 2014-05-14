#!/usr/bin/env python
#coding:utf-8
#
# Author: Peinan ZHANG
#

import math
from unigram import *

def word_segment(model_file, input_file):
  unigram_of = import_model(model_file)

  for line in open(input_file, 'r'):
    line = unicode(line, 'utf-8')
    line = line.strip()

    """forward step"""
    best_edge  = {0: 'NULL'}
    best_score = {0:0}

    for word_end in range(1, len(line) + 1):
      best_score[word_end] = float('inf')
      for word_begin in range(word_end):
        word = line[word_begin:word_end]
        if word in unigram_of or len(word) == 1:
          prob = calc_prob(word, unigram_of)
          score_temp = best_score[word_begin] + -math.log(prob)
          if score_temp < best_score[word_end]:
            best_score[word_end] = score_temp
            best_edge[word_end]  = (word_begin, word_end)

    """back step"""
    words = []
    next_edge = best_edge[len(best_edge) - 1]
    while next_edge != 'NULL':
      word = line[next_edge[0]:next_edge[1]]
      words.append(word.encode('utf-8'))
      next_edge = best_edge[next_edge[0]]
    words.reverse()

    print ' '.join(words)


if __name__ == '__main__':
  import sys
  word_segment(sys.argv[1], sys.argv[2])