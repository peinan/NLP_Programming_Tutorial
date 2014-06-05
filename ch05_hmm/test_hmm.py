#!/usr/bin/env python
#coding:utf-8
#
# Author: Peinan ZHANG
#

import math
from collections import defaultdict


def import_model(model_file):
  prob_of = {}
  for line in open(model_file):
    term, prob = line.strip().split('\t')
    prob_of[term] = float(prob)
  return prob_of


def extract_tags_words(prob_of, possible_tags, vocab):
  for keys in prob_of.keys():
    possible_tags[keys.split()[0]] += 1
    vocab[keys.split()[1]]         += 1
  return possible_tags, vocab


def test_hmm(trans_model_file, emit_model_file, test_file):
  trans_prob_of = import_model(trans_model_file)
  emit_prob_of  = import_model(emit_model_file)

  possible_tags = defaultdict(lambda: 0)
  vocab         = defaultdict(lambda: 0)
  possible_tags, vocab = extract_tags_words(trans_prob_of, possible_tags, vocab)
  possible_tags, vocab = extract_tags_words(emit_prob_of, possible_tags, vocab)

  # smoothing
  lambda_ = .95

  for line in open(test_file):
    words = line.strip().split()
    best_score = { "0 <s>": 0 }
    best_edge  = { "0 <s>": "NULL" }
    
    # forward step
    for i in range(len(words)):
      for prev_tag in possible_tags.keys():
        for next_tag in possible_tags.keys():
          i_prev    = '%s %s' % (i, prev_tag)
          prev_next = '%s %s' % (prev_tag, next_tag)
          next_word = '%s %s' % (next_tag, words[i])
          if i_prev in best_score and prev_next in trans_prob_of:
            # smoothing for emission prob
            if next_word not in emit_prob_of:
              vocab[words[i]] = 1
              prob_E = (1 - lambda_) / len(vocab)
            else:
              prob_E = lambda_ * emit_prob_of[next_word] \
                       + (1 - lambda_) / len(vocab)
            tmp_score = best_score[i_prev] \
                        + -math.log(trans_prob_of[prev_next]) \
                        + -math.log(prob_E)
            i_next = '%s %s' % (i + 1, next_tag)
            if i_next not in best_score or best_score[i_next] > tmp_score:
              best_score[i_next] = tmp_score
              best_edge[i_next]  = i_prev
    print best_edge

    # treating the end of sentence
    for prev_tag in possible_tags.keys():
      len_prev = '%s %s' % (len(words), prev_tag)
      prev_eos = '%s </s>' % (prev_tag)
      if len_prev in best_score and prev_eos in trans_prob_of:
        tmp_score = best_score[len_prev] + -math.log(trans_prob_of[prev_eos])
        len_eos   = '%s </s>' % (len(words) + 1)
        if len_eos not in best_score or best_score[len_eos] > tmp_score:
          best_score[len_eos] = tmp_score
          best_edge[len_eos]  = len_prev

    # backward step
    tags = []
    next_edge = best_edge['%s </s>' % (len(words) + 1)]
    while next_edge != '0 <s>':
      position, tag = next_edge.split()
      tags.append(tag)
      next_edge = best_edge[next_edge]
    tags.reverse()
    print ' '.join(tags)


if __name__ == '__main__':
  import sys
  # trans_model_file, emit_model_file, test_file
  test_hmm(sys.argv[1], sys.argv[2], sys.argv[3])