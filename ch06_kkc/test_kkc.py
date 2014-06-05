#!/usr/bin/env python
#coding:utf-8

def load_language_model(model_file):
  """Load a bigram model from a file"""
  from collections import defaultdict
  prob_of = defaultdict(float)
  for line in open(model_file, 'r'):
    line = line.strip()
    (word, P) = line.split("\t")
    word = word.decode("utf-8")
    prob_of[word] = float(P)

  def get_bigram_prob(prev_word,curr_word):
    """Compute smoothed bigram"""
    l1 = 0.9
    l2 = 0.9
    V  = 10000
    P1 = l1 * prob_of[curr_word] + (1 - l1) / V
    P2 = l2 * prob_of[prev_word + " " + curr_word] + (1 - l2) * P1
    return P2
  return get_bigram_prob


def load_translation_model(model_file):
  """Load kana-kanji model from a file"""
  prob_of = {}
  for line in open(model_file, 'r'):
    line = line.strip()
    (word, pron, prob) = line.split()
    word = word.decode("utf-8")
    pron = pron.decode("utf-8")
    prob = float(prob)
    if pron not in prob_of:
      prob_of[pron] = {}
    prob_of[pron][word] = prob
  return prob_of

def kana_kanji_convert(lm_file, tm_file, test_file):
  """Convert kana into kanji sequence"""
  import math

  get_bigram_prob = load_language_model(lm_file)
  tm = load_translation_model(tm_file)

  for line in open(test_file, 'r'):
    line = line.strip()
    line = line.decode("utf-8")
    edge  = { 0:{} }
    score = { 0:{} }
    edge[0]["<s>"]  = "NULL"
    score[0]["<s>"] = 0
    for end in range(1, len(line) + 1): # +1
      my_edges = {}
      for begin in range(end): # +1
        pron = line[begin:end]
        my_tm = {}
        if pron in tm:
          my_tm = tm[pron]
        elif len(pron) == 1:
          my_tm[pron] = 1 # is it really 0?
        for (curr_word, tm_prob) in my_tm.items():
          for (prev_word, prev_score) in score[begin].items(): 
            #print "%s %s %f" % (prev_word.encode("utf-8"),
            #                    curr_word.encode("utf-8"),
            #                    get_bigram_prob(prev_word, curr_word))
            curr_score = prev_score - math.log(tm_prob \
              * get_bigram_prob(prev_word, curr_word))
            if end not in score \
              or curr_word not in score[end] \
              or curr_score < score[end][curr_word]:
              if end not in score:
                score[end] = {}
              if end not in edge:
                edge[end] = {}
              score[end][curr_word] = curr_score
              edge[end][curr_word]  = (begin, prev_word)

    # Treat the last step
    score[len(line) + 1] = { "</s>":float("inf")}
    edge[len(line) + 1]  = { "</s>":"" }
    for (last_word, last_score) in score[len(line)].items():
      if last_score < score[len(line) + 1]["</s>"]:
        score[len(line) + 1]["</s>"] = last_score
        edge[len(line) + 1]["</s>"] = (len(line), last_word)

    # backward step
    words = []
    next_edge = edge[len(line) + 1]["</s>"] # note the "+1"
    while next_edge != "NULL":
      (position, word) = next_edge
      words.append(word)
      next_edge = edge[position][word]
    words.pop() # last one is <s>
    words.reverse()
    print " ".join(words).encode("utf-8")

if __name__ == "__main__":
  import sys
  lm_file   = sys.argv[1]
  tm_file   = sys.argv[2]
  test_file = sys.argv[3]
  kana_kanji_convert(lm_file, tm_file, test_file)
