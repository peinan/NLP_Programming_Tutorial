#!/usr/bin/env python
#coding:utf-8
#
# Author:  Peinan ZHANG
#

import random

def sample_one(probs):
  """Sample one probability"""
  z = sum(probs)
  assert 0 <= z <= 1, "Probability must be [0, 1]"
  remaining = random.uniform(0, z)
  for i in range(len(probs)):
    remaining -= probs[i]
    if remaining <= 0:
      return i
  assert "Sample_one should return a value."

def learn_lda(train_file):
  """Learn Latent Dirichlet Allocation"""
  import sys
  import math
  from collections import defaultdict

  NUM_TOPICS = 2
  MAX_ITER   = 30
  ALPHA      = 0.0001
  BETA       = 0.0001

  # initialization
  xcorpus = []
  ycorpus = []
  xcounts = defaultdict(int)
  ycounts = defaultdict(int)

  def add_counts(word, topic, docid, amount):
    """Add counts to probability"""
    xcounts[topic]          += amount
    xcounts[(word, topic)]  += amount
    ycounts[docid]          += amount
    ycounts[(topic, docid)] += amount

    # error check
    assert xcounts[topic] >= 0, "xcounts[%s] must be >= 0" % (topic)
    assert xcounts[(word, topic)] >= 0, "xcounts[(%s,%s)] must be >= 0" % (word,topic)
    assert ycounts[docid] >= 0, "ycounts[%s] must be >= 0" % (docid)
    assert ycounts[(topic, docid)] >= 0, "ycounts[(%s,%s)] must be >= 0" % (topic, docid)

  # reading training corpus
  existing_words = {}
  for line in open(train_file, "r"):
    docid = len(xcorpus)
    line = line.rstrip()
    words = line.split()
    topics = []
    for word in words:
      topic = random.randint(0, NUM_TOPICS - 1)
      topics.append(topic)
      add_counts(word, topic, docid, 1)
      existing_words[word] = 1
    xcorpus.append(words)
    ycorpus.append(topics)

  NUM_WORDS = len(existing_words)  
  # Memoize P(x|y) to avoid computing the same value again and again
  Pxy_cache = {}
  def get_Pxy(word, topic):
    if (word, topic) in Pxy_cache:
      return Pxy_cache[(word, topic)]
    else:
      Pxy = float(xcounts[(word, topic)] + ALPHA) \
          / (xcounts[topic] + ALPHA * NUM_WORDS)
      assert Pxy >= 0, "P(x|y) must be larger than 0"
      Pxy_cache[(word, topic)] = Pxy
      return Pxy

  # Ditto
  PyY_cache = {}
  def get_PyY(topic, docid):
    if (topic, docid) in PyY_cache:
      return PyY_cache[(topic, docid)]
    else:
      PyY = float(ycounts[(topic, docid)] + BETA) \
          / (ycounts[docid] + BETA * NUM_TOPICS)
      assert PyY >= 0, "P(y|Y) must be larger than 0"
      PyY_cache[(topic, docid)] = PyY
      return PyY

  # training LDA
  for m in range(MAX_ITER):
    ll = 0
    for i in range(len(xcorpus)):      # doc
      for j in range(len(xcorpus[i])): # word
        x = xcorpus[i][j]
        y = ycorpus[i][j]
        add_counts(x, y, i, -1)
        probs = []
        for k in range(NUM_TOPICS):
          probs.append(get_Pxy(x, k) * get_PyY(k, i)) # The last one is Y_i
        new_y = sample_one(probs)
        add_counts(x, new_y, i, 1)
        ycorpus[i][j] = new_y
        if probs[new_y] == 0:
          ll = -float("inf")
        else:
          ll += math.log(probs[new_y], 2)
    print ll

  #print xcounts
  #print ycounts

  words_in = defaultdict(list)
  for (key, value) in xcounts.iteritems():
    if type(key) == tuple and value > 0:
      word  = key[0]
      topic = key[1]
      words_in[topic].append(word)
  for k, v in words_in.items():
    print '%s: %s' % (k, v)


if __name__ == "__main__":
  import sys
  train_file = sys.argv[1]
  learn_lda(train_file)
