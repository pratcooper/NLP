#!/usr/bin/env python
import argparse  # optparse is deprecated
from itertools import islice  # slicing for iterators
from nltk.stem import porter
import pyter

import nltk

def ngram(sent, gramcount=1):
    if gramcount < 1:
        raise Exception("Must be at least unigrams")
    return [tuple(sent[i:i + gramcount]) for i in range(0, len(sent) - gramcount + 1)]


def stem(sent):
    porterstemmer = porter.PorterStemmer()
    return [porterstemmer.stem(w.decode("utf8").lower()) for w in sent]


def intersection(h, ref):
    refmap = {}
    for word in ref:
        if word in refmap:
            refmap[word] += 1
        else:
            refmap[word] = 1
    i = 0
    for run in h:
        if run in refmap and refmap[run] > 0:
            i += 1
            refmap[run] -= 1
    return i


def score(h, ref):
    alpha = 0.9
    m = intersection(h, ref)
    if len(h) == 0 or len(ref) == 0:
        return 0
    P, R = float(m) / len(h), float(m) / len(ref)
    score = P * R / (1 - alpha) * R + alpha * P
    return score


def main():
    parser = argparse.ArgumentParser(description='Evaluate translation hypotheses.')
    parser.add_argument('-i', '--input', default='data/hyp1-hyp2-ref',
                        help='input file (default data/hyp1-hyp2-ref)')
    parser.add_argument('-n', '--num_sentences', default=None, type=int,
                        help='Number of hypothesis pairs to evaluate')
    # note that if x == [1, 2, 3], then x[:None] == x[:] == x (copy); no need for sys.maxint
    opts = parser.parse_args()

    # we create a generator and avoid loading all sentences into a list
    def sentences():
        with open(opts.input) as f:
            for pair in f:
                yield [sentence.strip().split() for sentence in pair.split(' ||| ')]

    # note: the -n option does not work in the original code
    for h1, h2, ref in islice(sentences(), opts.num_sentences):

        h1_match = nltk.translate.ribes_score(ref,h1)
        h2_match = nltk.translate.ribes_score(ref,h2)

        print(1 if h1_match > h2_match else  # \begin{cases}
              (0 if h1_match == h2_match
               else -1))  # \end{cases}


# convention to allow import of this file as a module
if __name__ == '__main__':
    main()