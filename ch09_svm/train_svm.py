#!/usr/bin/env python
#coding:utf-8
#
# Author: Peinan ZHANG
#

def update_weights(w, phi, y, c):
  """Update weights online with L1 regularization"""
  # L1 regularization
  for name, value in w.items():
    if abs(value) < c:
      w[name] = 0
    else:
      if value > 0:
        w[name] -= c
      else:
        w[name] += c

  for name, value in phi.items():
    w[name] += value * y


def create_features(x):
  """Create unigram features"""
  from collections import defaultdict
  phi = defaultdict(int)

  words = x.split()
  for word in words:
    phi["UNI:%s" % (word)] += 1

  return phi


def predict_one(w, phi):
  """Predict the label of an instance"""
  score = 0

  for name, value in phi.iteritems():
    if name in w:
      score += value * w[name]
    else:
      w[name] = 0

  if score >= 0:
    return 1
  else:
    return -1


def train_svm(training_file, model_file, margin):
  """Train a model with perceptron"""
  from collections import defaultdict
  w   = defaultdict(float)
  phi = defaultdict(float)
  MAX_ITER = 100

  for iter in range(MAX_ITER):
    for line in open(training_file, 'r'):
      line = line.strip()
      (y, x) = line.split("\t")
      y = int(y)  # assume label is int
  
      phi = create_features(x)
      val = predict_one(w, phi) * y
      if val <= margin:
        update_weights(w, phi, y, margin)

  with open(model_file, "w") as model:
    for name, value in sorted(w.items(), key=lambda x:x[0]):
      model.write("%s\t%f\n" % (name, value))


if __name__ == "__main__":
  import sys
  import argparse

  parser = argparse.ArgumentParser()
  parser.add_argument('-c', '--margin',     dest='margin')
  parser.add_argument('-t', '--train-file', dest='train')
  parser.add_argument('-m', '--model-file', dest='model')
  args = parser.parse_args()

  if not args.margin or not args.train or not args.model:
    parser.print_help()
    sys.exit(-1)
  train_svm(args.train, args.model, float(args.margin))
