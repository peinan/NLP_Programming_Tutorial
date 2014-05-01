#!/usr/bin/env python
#coding:utf-8
#
# Author: Peinan ZHANG
#

import sys
from collections import defaultdict

def train_bigram(train_file, model_file):
  count_of         = defaultdict(lambda: 0)
  context_count_of = defaultdict(lambda: 0)

  for line in open(train_file, 'r'):
    words = line.strip().split(' ')
    words.insert(0, '<s>')
    words.append('</s>')
    for i in range(1, len(words) - 1):
      bigram = "%s %s" % (words[i - 1], words[i])
      count_of[bigram]               += 1
      context_count_of[words[i - 1]] += 1
      count_of[words[i]]             += 1
      context_count_of[""]           += 1

  with open(model_file, 'w') as model:
    for ngram, count in sorted(count_of.items()):
      words = ngram.split(' ')
      words.pop()
      if len(words) > 0:
        context = words[0]
      else:
        context = ''
      prob = float(count_of[ngram]) / context_count_of[context]
      # print ngram, prob
      model.write('%s\t%.6f\n' % (ngram, prob))


def import_model(model_file):
  prob_of = defaultdict(lambda: 0)
  for line in open(model_file, 'r'):
    words, prob = line.split('\t')
    prob_of[words] = float(prob)
  return prob_of


def test_bigram(model_file, test_file):
  import math

  # lam_1 = .9
  # lam_2 = .9
  lam100_start = 0
  lam100_end   = 100
  lam100_step  = 1
  N = 10 ** 6
  W = 0
  H = 0

  prob_of = import_model(model_file)


  entropy_of = {}
  for lam100_1 in range(lam100_start, lam100_end, lam100_step):
    for lam100_2 in range(lam100_start, lam100_end, lam100_step):
      lam_1 = float(lam100_1) / 100
      lam_2 = float(lam100_2) / 100
      for line in open(test_file, 'r'):
        line = line.strip()
        words = line.split()
        words.insert(0, '<s>')
        words.append('</s>')
        for i in range(1, len(words) - 1):
          P1 = lam_1 * prob_of[words[i]] + (1 - lam_1) / N
          P2 = lam_2 * prob_of['%s %s' % (words[i - 1], words[i])] \
               + (1 - lam_2) * P1
          H += -math.log(P2, 2)
          W += 1
          entropy = (float(H) / W)
          entropy_of["%.2f %.2f" % (lam_1, lam_2)] = entropy

  # print 'entropy = %f' % (entropy)
  for lams, ent in sorted(entropy_of.items(), key = lambda x: x[1]):
    print lams, ent


if __name__ == '__main__':
  model_file = 'bigram.model'
  train_bigram(sys.argv[1], model_file)
  test_bigram(model_file, sys.argv[2])