#!/usr/bin/env python
import argparse  # optparse is deprecated
import sys
import re
from itertools import islice  # slicing for iterators
from nltk.stem import porter
from nltk.corpus import wordnet


def ngram(sent, gramcount=1):
    if gramcount < 1:
        raise Exception("Must be at least unigrams")
    if len(sent) < gramcount:
        return [tuple(sent)]
    return [tuple(sent[i:i + gramcount]) for i in range(0, len(sent) - gramcount + 1)]


def stem(sent):
    porterstemmer = porter.PorterStemmer()
    return [porterstemmer.stem(w.decode("utf-8").lower()) for w in sent]


def intersection_raw(h, ref):
    refset = set(ref)
    i = 0
    for run in h:
        if run in refset:
            i += 1
    return i


def intersection(h, ref, wordnetTest=True):
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
        elif wordnetTest and not run in refmap and not isinstance(run, tuple):
            # Use wordnet to match
            synsets = wordnet.synsets(run.decode("utf-8"))
            if len(synsets) == 0:
                continue;
            for word in refmap:
                s = wordnet.synsets(word.decode("utf-8"))
                if len(s) < 1:
                    continue
                if wordnet.path_similarity(synsets[0], s[0]) > 0.9:
                    i += 1
                    refmap[word] -= 1
    return i


def chunkcalc(h, ref):
    # recursively calculates chunkings
    if len(h) == 0:
        return 0
    allMatches = []
    for i in range(1, len(h) + 1):
        foundMatch = False
        currsrc = tuple(h[0:i])
        for j in range(0, len(ref)):
            if tuple(ref[j:j + i]) == currsrc:
                allMatches.append((i, j))
                foundMatch = True
        if not foundMatch:
            break;
    if len(allMatches) == 0:
        return 0 + chunkcalc(h[1:], ref)
    # find best matches
    sm = sorted(allMatches)
    iref, jref = sm[-1]
    smatches = [(i, j) for i, j in allMatches if i == iref]
    if iref == 1:
        smatches = smatches[0:1]
    scores = [(chunkcalc(h[i:], ref[0:j] + [None] + ref[j + i:])) for i, j in smatches]
    return 1 + sorted(scores)[0]


def score(h, ref, ngrams=False):
    alpha = 0.9  # 0.81 #0.9
    beta = 0.83  # 0.83
    gamma = 0.5  # 0.28
    if len(h) == 0 or len(ref) == 0:
        print h, ref
    m = max(intersection(h, ref, True), intersection(stem(h), stem(ref), False) if not ngrams else 0)
    mu = m
    c = chunkcalc(h[:], ref[:])
    P, R = (float(mu)) / (len(h)), (float(mu)) / (len(ref))
    score = P * R / (1 - alpha) * R + alpha * P
    penalty = gamma * ((float(c) / (m + 0.00001)) ** beta)
    return (1 - penalty) * score


def main():
    a, b = 0.8, 0.2
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
                yield [[re.sub(r"[^a-zA-Z0-9]", "", word) for word in sentence.strip().lower().split()] for sentence in
                       pair.split(' ||| ')]

    # note: the -n option does not work in the original code
    for h1, h2, ref in islice(sentences(), opts.num_sentences):
        h1_match = score(h1, ref)
        h2_match = score(h2, ref)

        h1_match2 = score(ngram(stem(h1), 2), ngram(stem(ref), 2), True)
        h2_match2 = score(ngram(stem(h2), 2), ngram(stem(ref), 2), True)

        diff1 = h1_match - h2_match
        diff2 = h1_match2 - h2_match2

        diff = a * diff1 + b * diff2
        print(1 if diff > 0.0001 else
              (-1 if diff < -0.0001
               else 0))

        # convention to allow import of this file as a module


if __name__ == '__main__':
    main()