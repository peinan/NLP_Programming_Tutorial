#!/usr/bin/env python
#coding:utf-8
#
# Author:  Peinan ZHANG
#

def save_model(model_file, w):
  """Save structured perceptron model to a file"""
  with open(model_file, "w") as model:
    for (feature, weight) in w.items():
      model.write("%s\t%s\n" % (feature, weight))


def create_trans(first_tag, second_tag):
  """Create a bigram feature"""
  phi_bigram = {}
  phi_bigram["T %s %s" % (first_tag, second_tag)] = 1
  return phi_bigram


def create_emit(tag, word):
  """Create a unigram feature"""
  phi_unigram = {}
  phi_unigram["E %s %s" % (tag, word)] = 1
  if word.istitle():
    phi_unigram["CAPS %s" % (word)] = 1
  phi_unigram["PREFIX-1 %s" % (word[:1])] = 1
  phi_unigram["PREFIX-2 %s" % (word[:2])] = 1
  phi_unigram["PREFIX-3 %s" % (word[:3])] = 1
  phi_unigram["SUFFIX-1 %s" % (word[-1:])] = 1
  phi_unigram["SUFFIX-2 %s" % (word[-2:])] = 1
  phi_unigram["SUFFIX-3 %s" % (word[-3:])] = 1
  return phi_unigram


def create_features(words, tags):
  """Create features given a pair of input and output"""
  phi = {}

  # bigram features
  for i in range(len(tags) + 1):
    if i == 0:
      first_tag = "<s>"
    else:
      first_tag = tags[i-1]
    if i == len(tags):
      next_tag = "</s>"
    else:
      next_tag = tags[i]
    phi.update(create_trans(first_tag, next_tag)) # Note that += doesn't work

  # unigram features
  for i in range(len(tags)):
    phi.update(create_emit(tags[i], words[i])) # ditto

  return phi


def calc_score(w, prev_tag, next_tag, word):
  """Return a score given a weight vector and features"""
  score = 0
  for feature in create_trans(prev_tag, next_tag):
    score += w[feature]
  if next_tag != "</s>":
    for feature in create_emit(next_tag, word):
      score += w[feature]

  return score


def hmm_viterbi(w, words, possible_tags, transition):
  """Returns the best path given the current weights and input"""
  l = len(words)
  best_score = { "0 <s>":0 }
  best_edge  = { "0 <s>":"NULL" }

  # forward step
  for i in range(l):
    for prev_tag in possible_tags.keys():
      for next_tag in possible_tags.keys():
        i_prev    = "%s %s" % (i, prev_tag)
        prev_next = "%s %s" % (prev_tag, next_tag)
        next_word = "%s %s" % (next_tag, words[i])
        if i_prev in best_score and prev_next in transition:
          score = best_score[i_prev] + calc_score(w, prev_tag, next_tag, words[i])
          i_next = "%s %s" % (i+1, next_tag)
          # Note the ineauality
          if i_next not in best_score or best_score[i_next] < score:
            best_score[i_next] = score
            best_edge[i_next]  = i_prev

  # Treating the end of sentence
  for prev_tag in possible_tags.keys():
    l_prev   = "%s %s" % (l, prev_tag)
    prev_eos = "%s </s>" % (prev_tag)
    # Consider only the transition probability. See p.18 of slides #5.
    if l_prev in best_score and prev_eos in transition:
      score = best_score[l_prev] + calc_score(w, prev_tag, "</s>", "</s>")
      l_eos = "%s </s>" % (l + 1) # note the "+1"
      # Note the inequality
      if l_eos not in best_score or best_score[l_eos] < score:
        best_score[l_eos] = score
        best_edge[l_eos]  = l_prev

  # backward step
  tags = []
  next_edge = best_edge["%s </s>" % (l + 1)] # note the "+1"
  while next_edge != "0 <s>":
    (position, tag) = next_edge.split()
    tags.append(tag)
    next_edge = best_edge[next_edge]
  tags.reverse()
  
  return tags


def train_hmm(model_file, train_file, max_iter):
  """Train a POS tagger using structured perceptron"""
  import sys
  from collections import defaultdict
  w = defaultdict(float)
  transition = {}
  possible_tags = { "<s>":1, "</s>":1 }
  possible_transition = {}
  MAX_ITER = max_iter

  for i in range(MAX_ITER):
    print >>sys.stderr, "Iteration #%i ..." % (i)
    j = 0
    for line in open(train_file, 'r'):
      if j % 100 == 0:
        print >>sys.stderr, "Processing %i lines..." % (j)
      j += 1
      line = line.rstrip()
      wordtags = line.split()
      words = []
      tags  = []
      for wordtag in wordtags:
        (word, tag) = wordtag.split("_")
        words.append(word)
        tags.append(tag)
      for i in range(len(tags)):
        possible_tags[tags[i]] = 1
        if i == 0:
          transition["<s> %s" % (tags[i])] = 1
        # we need to process the last element only once
        if i == len(tags) - 1:
          transition["%s </s>" % (tags[i])] = 1
        else:
          transition["%s %s" % (tags[i], tags[i+1])] = 1
          
      best_tags = hmm_viterbi(w, words, possible_tags, transition)
      phi_prime = create_features(words, tags)
      phi_hat   = create_features(words, best_tags)
      for feature in phi_prime:
        w[feature] += 1
      for feature in phi_hat:
        w[feature] -= 1

  save_model(model_file, w)
  

if __name__ == "__main__":
  import sys
  import argparse
  parser = argparse.ArgumentParser()
  parser.add_argument("-t", "--train-file", dest="train")
  parser.add_argument("-m", "--model-file", dest="model")
  parser.add_argument("-i", "--iteration", default=10)
  opts = parser.parse_args()

  if not opts.model or not opts.train:
    parser.print_help()
    sys.exit(-1)

  model_file = opts.model
  train_file = opts.train
  max_iter   = int(opts.iteration)
  train_hmm(model_file, train_file, max_iter)
