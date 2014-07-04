#!/usr/bin/env python
#coding:utf-8
#
# Author:  Peinan ZHANG
#


from train_nn import predict_nn
from train_svm import create_features

def test_nn(test_file, model_file):
  """Test using a neural network"""
  import pickle

  with open(model_file, 'r') as f:
    network = pickle.load(f)

  for line in open(test_file, 'r'):
    line = line.rstrip()
    phi = create_features(line)
    y = predict_nn(network, phi)
    #print y[-1].values()[0]
    if y[-1].values()[0] >= 0:
      print 1
    else:
      print -1

if __name__ == "__main__":
  import sys
  import argparse

  parser = argparse.ArgumentParser()
  parser.add_argument('-t', '--test-file',  dest='test')
  parser.add_argument('-m', '--model-file', dest='model')
  args = parser.parse_args()

  if not args.test or not args.model:
    parser.print_help()
    sys.exit(-1)

  test_file  = args.test
  model_file = args.model

  test_nn(test_file, model_file)
