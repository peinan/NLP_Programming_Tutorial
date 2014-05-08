#!/usr/bin/env python
#coding: utf-8
#
# Author: Peinan ZHANG
#

from collections import defaultdict
from train_perceptron import *

# prediction
# y = sign(sum(w_i * phi_i(x)))

def predict_all(model_file, input_file):
  """the whole flow of prediction"""
  weight_of = import_model(model_file)       # weight_of[name] = w_name
  for line in open(input_file, 'r'):
    phi_of = create_features(line.strip())   # phi_of[name] = phi_name(x)
    y_  = predict_one(weight_of, phi_of)     # sign(weight_of * phi_of(x))
    print y_


def import_model(model_file):
  for line in open(model_file, 'r'):
    line = line.strip()
    ngram, weight = line.split("\t")
    weight_of[ngram] = weight
  return weight_of


def test_perceptron(model_file, test_file):
  predict_all(model_file, test_file)


if __name__ == '__main__':
  import sys
  test_perceptron(sys.argv[1])