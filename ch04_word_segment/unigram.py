#!/usr/bin/env python
#coding:utf-8
#
# Author: Peinan ZHANG
#

import sys
from collections import defaultdict

def train_unigram(train_file):
	count_of    = defaultdict(lambda: 0)
	total_count = 0
	
	for line in open(train_file, "r"):
		words = line.strip().split(" ")
		words.append("</s>")
		for word in words:
			count_of[word] += 1
			total_count    += 1

	model_file = "unigram.model"
	with open(model_file, "w") as model_file:
		for k, v in count_of.items():
			prob = float(count_of[k]) / total_count
			model_file.write("%s\t%f\n" % (k, prob))


def calc_prob(word, unigram_of):
	lambda_1   = .95
	lambda_unk = 1 - lambda_1
	N          = 10 ** 6

	prob = lambda_unk / N
	if word in unigram_of:
		prob += lambda_1 * unigram_of[word]

	return prob


def import_model(model_file):
	prob_of = defaultdict(lambda: 0)
	for line in open(model_file, "r"):
		line = line.strip()
		word, prob = line.split("\t")
		word = word.decode("utf-8")
		prob_of[word] = float(prob)
	return prob_of


def test_unigram(model_file, test_file):
	import math
	
	lam1    = 0.95
	lam_unk = 1 - lam1
	unk     = 0
	N       = 1000000
	W       = 0
	H       = 0

	prob_of = import_model(model_file)
	
	for line in open(test_file, "r"):
		words = line.strip().split(" ")
		words.append("</s>")
		for word in words:
			W += 1
			P = lam_unk / N 
			if word in prob_of:
				P += lam1 * prob_of[word]
			else:
				unk += 1
			H += -math.log(P, 2)
	
	print "entropy  = %f" % (float(H) / W)
	print "coverage = %f" % (float(W - unk) / W)


if __name__ == "__main__":
	train_unigram(sys.argv[1])
	# test_unigram("unigram.model", sys.argv[2])
