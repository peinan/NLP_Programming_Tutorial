#!/usr/bin/env python
#coding:utf-8
#
# Author:  Peinan ZHANG
#

from train_svm import create_features
from train_svm import predict_one

def predict_all(model_file, input_file):
  """Reads model file and predict instance one by one"""
  # Reading a model file
  w = {}
  for line in open(model_file):
    line = line.strip()
    (name, value) = line.split("\t")
    value = float(value)
    w[name] = value

  # Evaluation and print results
  for line in open(input_file):
    line = line.strip()
    phi = create_features(line)
    y_ = predict_one(w, phi)

    print y_

if __name__ == "__main__":
  import sys
  import argparse

  parser = argparse.ArgumentParser()
  parser.add_argument('-t', '--test-file', dest='test')
  parser.add_argument('-m', '--model-file', dest='model')
  args = parser.parse_args()

  if not args.test or not args.model:
    parser.print_help()
    sys.exit(-1)

  predict_all(args.model, args.test)
