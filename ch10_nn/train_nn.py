#!/usr/bin/env python
#coding:utf-8
#
# Author:  Peinan ZHANG
#


#from train_svm import predict_one
from train_svm import create_features

def predict_one(w, phi):
  """Predict the label of an instance using tanh"""
  from math import tanh
  score = 0

  for name, value in phi.iteritems():
    if name in w:
      score += value * w[name]
    else:
      w[name] = 0

  return tanh(score)

def predict_nn(network, phi):
  """Predict using a neural network"""
  import random

  # See page 17
  y = [ phi ]

  for i in range(len(network)):
    (layer, weight) = network[i]

    # need to randomize, see page 23
    for feature in y[layer - 1].keys(): # note that - 1
      if feature not in weight:
        weight[feature] = random.uniform(-1, 1)

    answer = predict_one(weight, y[layer - 1]) # note that - 1
    if len(y) < layer + 1:
      y.append({})
    y[layer][i] = answer

  return y

def update_nn(network, phi, y_, learning_rate):
  """Update a neural network"""
  delta = {}
  y = predict_nn(network, phi)

  # Backpropagation
  for j in sorted(range(len(network)), reverse=True):
    (layer, w) = network[j]
    if j == len(network) - 1:
      delta[j] = y_ - y[-1][j]
    else:
      sum = 0
      (layer, weight) = network[j]
      for i in y[layer + 1].keys():
        (prev_layer, prev_weight) = network[i]
        sum += delta[i] * prev_weight[j]
      delta[j] = (1 - y[layer][j] ** 2) * sum

  for j in range(len(network)):
    (layer, w) = network[j]
    for (name, val) in y[layer - 1].items():
      w[name] += learning_rate * delta[j] * val

def train_nn(train_file, model_file, num_nodes, num_layers, num_iter):
  """Train a neural network"""
  import random
  import pickle
  import sys

  NUM_NODES  = num_nodes
  NUM_LAYERS = num_layers
  NUM_ITER   = num_iter
  # Too large learning rate gives bizarre results
  #LEARNING_RATE = 0.5
  LEARNING_RATE = 0.1

  # See page 10
  network = []
  for i in range(NUM_LAYERS):
    for j in range(NUM_NODES):
      weight = {}
      node = (i + 1, weight) # note that + 1
      network.append(node)
  # the last node
  network.append((NUM_LAYERS + 1, {}))
  
  for i in range(NUM_ITER):
    print >>sys.stderr, "Iteration #%s..." % (i)
    for line in open(train_file, 'r'):
      line = line.rstrip()
      (y, x) = line.split("\t")
      y = int(y)
      phi = create_features(x)
      update_nn(network, phi, y, LEARNING_RATE)

  # debugging
  for line in open(train_file, 'r'):
    line = line.rstrip()
    (y, x) = line.split("\t")
    y = int(y)
    phi = create_features(x)
    y_ = predict_nn(network, phi)
    print y, y_[-1].values()[0]

  with open(model_file, 'w') as f:
    pickle.dump(network, f)

if __name__ == "__main__":
  import sys
  import argparse

  parser = argparse.ArgumentParser()
  parser.add_argument('-t', '--train-file', dest='train')
  parser.add_argument('-m', '--model-file', dest='model')
  parser.add_argument('-n', '--num-nodes',  dest='num_nodes', default=2)
  parser.add_argument('-l', '--num-layers', dest='num_layers', default=1)
  parser.add_argument('-i', '--num-iter',   dest='num_iter', default=1)
  args = parser.parse_args()

  if not args.train or not args.model:
    parser.print_help()
    sys.exit(-1)

  train_file = args.train
  model_file = args.model
  num_nodes  = int(args.num_nodes)
  num_layers = int(args.num_layers)
  num_iter   = int(args.num_iter)

  train_nn(train_file, model_file, num_nodes, num_layers, num_iter)
