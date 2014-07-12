#!/usr/bin/env python
#coding:utf-8
#
# Author:  Peinan ZHANG
#

from train_hmm_percep import hmm_viterbi

def load_model(model_file):
  """Load structured perceptron model from a file"""
  from collections import defaultdict
  w             = defaultdict(float)    # Need to care unknown words
  possible_tags = { "<s>":1, "</s>":1 } # Note that these are not in the model
  transition    = {}

  for line in open(model_file, 'r'):
    line = line.rstrip()
    (feature, weight) = line.split("\t")
    w[feature] = float(weight)
    features = feature.split()
    if features[0] == "E":
      possible_tags[features[1]] = 1
    elif features[0] == "T":
      transition["%s %s" % (features[1], features[2])] = 1

  return (w, possible_tags, transition)


def test_hmm(test_file, model_file):
  """Assign POS to a given file using structured perceptron"""
  (w, possible_tags, transition) = load_model(model_file)

  for line in open(test_file, 'r'):
    line  = line.rstrip()
    words = line.split()
    tags  = hmm_viterbi(w, words, possible_tags, transition)
    print " ".join(tags)


if __name__ == "__main__":
  import sys
  import argparse
  parser = argparse.ArgumentParser()
  parser.add_argument("-t", "--test-file",  dest="test")
  parser.add_argument("-m", "--model-file", dest="model")
  opts = parser.parse_args()

  if not opts.model or not opts.test:
    parser.print_help()
    sys.exit(-1)

  test_hmm(opts.test, opts.model)
