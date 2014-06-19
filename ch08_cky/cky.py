#!/usr/bin/env python
#coding:utf-8
#
# Author: Peinan ZHANG
#


def load_grammar(grammar_file):
  """Load grammar file in "lhs \t rhs \t prob \n" format"""
  import math
  from collections import defaultdict
  nonterm = []
  preterm = defaultdict(list)
  for rule in open(grammar_file, 'r'):
    rule = rule.rstrip()
    (lhs, rhs, prob) = rule.split("\t")
    log_prob = math.log(float(prob))
    rhs_symbols = rhs.split()
    if len(rhs_symbols) == 1:
      preterm[rhs].append((lhs, log_prob))
    else:
      nonterm.append((lhs, rhs_symbols[0], rhs_symbols[1], log_prob))

  return nonterm, preterm

def parse_input(input_file, grammar_file):
  """Parse an input file given a grammar file"""
  from collections import defaultdict
  (nonterm, preterm) = load_grammar(grammar_file)

  for line in open(input_file, 'r'):
    line = line.rstrip()
    words = line.split()

    best_score = {}
    best_edge  = {}

    # This function should have access to best_edge and words
    def print_tree(sym_ij):
      """Print (sub)-tree"""
      if sym_ij in best_edge:
        return "(%s %s %s)" % (sym_ij[0],
                               print_tree(best_edge[sym_ij][0]),
                               print_tree(best_edge[sym_ij][1]))
      else:
        return "(%s %s)" % (sym_ij[0], words[sym_ij[1]])

    # process preterminal symbols
    for i in range(len(words)):
      for (lhs, log_prob) in preterm[words[i]]:
        best_score[(lhs, i, i+1)] = log_prob

    # process nonterminal symbols
    for j in range(2, len(words) + 1): # remember + 1
      for i in range(j - 2, -1, -1):   # -1 is a step size
        for k in range(i + 1, j):      # remember + 1 in rhs
          for (sym, lsym, rsym, log_prob) in nonterm:
            lsym_ik = (lsym, i, k)
            rsym_kj = (rsym, k, j)
            sym_ij  = (sym,  i, j)
            if lsym_ik in best_score and best_score[lsym_ik] > -float("inf") and \
               rsym_kj in best_score and best_score[rsym_kj] > -float("inf"):
               my_lp = best_score[lsym_ik] + best_score[rsym_kj] + log_prob
               if sym_ij not in best_score or my_lp > best_score[sym_ij]:
                 best_score[sym_ij] = my_lp
                 best_edge[sym_ij]  = (lsym_ik, rsym_kj)

    #print best_edge

    print print_tree(("S", 0, len(words)))


if __name__ == "__main__":
  import sys
  input_file   = sys.argv[1]
  grammar_file = sys.argv[2]
  parse_input(input_file, grammar_file)
