#!/usr/bin/env python
#coding:utf-8
#
# Author: Peinan ZHANG
#

from collections import defaultdict

def train_hmm(train_file):
  """use hmm to train tags"""

  trans_count_of = defaultdict(lambda: 0)
  emit_count_of  = defaultdict(lambda: 0)
  tag_count_of   = defaultdict(lambda: 0)

  for line in open(train_file):
    terms = line.strip().split(' ')
    words = ['<s>']
    tags  = ['<s>']
    for term in terms:
      word, tag = term.split('_')
      words.append(word)
      tags.append(tag)
    words.append('</s>')
    tags.append('</s>')

    tag_count_of['<s>'] += 1
    for i in range(1, len(tags) - 1):
      trans = '%s %s' % (tags[i - 1], tags[i])
      emit  = '%s %s' % (tags[i], words[i])

      trans_count_of[trans] += 1
      emit_count_of[emit]   += 1
      tag_count_of[tags[i]] += 1
    trans_count_of['%s </s>' % (tags[len(tags) - 2])] += 1

  with open('hmm_trans.model', 'w') as model_trans:
    for trans, count in sorted(trans_count_of.items()):
      # print trans, count, tag_count_of[trans.split(' ')[0]]
      prob_trans = float(count) / tag_count_of[trans.split(' ')[0]]
      model_trans.write('%s\t%f\n' % (trans, prob_trans))

  with open('hmm_emit.model', 'w') as model_emit:
    for emit, count in sorted(emit_count_of.items()):
      # print emit, count, tag_count_of[emit.split(' ')[0]]
      prob_emit = float(count) / tag_count_of[emit.split(' ')[0]]
      model_emit.write('%s\t%f\n' % (emit, prob_emit))


if __name__ == '__main__':
  import sys
  train_hmm(sys.argv[1])