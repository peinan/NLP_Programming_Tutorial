#!/usr/bin/env python
#coding: utf-8
#
# Author: Peinan ZHANG
#

from collections import defaultdict

def predict_one(weight_of, phi_of):
  """only predict one thing"""
  score = 0                                  # score = weight_of * phi_of(x)
  for name, value in phi_of.items():
    if name in weight_of:
      score += value * weight_of[name]
  if score >= 0:
    return 1
  else:
    return -1


def create_features(x):
  phi_of = defaultdict(lambda: 0)
  words = x.split(' ')
  for word in words:
    phi_of['UNI:%s' % (word)] += 1
  return phi_of


def update_weights(weight_of, phi_of, y):
  for name, value in phi_of.items():
    weight_of[name] += value * y


def train_perceptron(train_file):
  weight_of = defaultdict(lambda: 0)
  phi_of    = defaultdict(lambda: 0)

  for line in open(train_file, 'r'):
    y, x   = line.strip().split('\t')
    y      = int(y)
    phi_of = create_features(x)
    y_     = predict_one(weight_of, phi_of)
    # print y_, y
    if y_ != y:
      update_weights(weight_of, phi_of, y)

  with open('perceptron.model', 'w') as model_file:
    for k, v in sorted(weight_of.items(), key = lambda x: x[0]):
      model_file.write('%s\t%f\n' % (k, v))


if __name__ == '__main__':
  import sys
  train_perceptron(sys.argv[1])