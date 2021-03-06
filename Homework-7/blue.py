#!/usr/bin/env python
import argparse  # optparse is deprecated
from itertools import islice  # slicing for iterators
import sys
from nltk import pos_tag, word_tokenize, download
from collections import defaultdict
from operator import mul
from math import log


def word_matches(h, ref):
    h = [word.lower() for word in h]
    ref = [word.lower() for word in ref]

    # calculate brevity penalty
    bp = min(1.0, float(len(h)) / float(len(ref)))

    # generate all possible n-grams from reference sentence
    n = 2
    if n <= len(ref):
        r_dict = [[] for x in xrange(sum(xrange(len(ref) - n + 1, len(ref) + 1)))]
    else:
        r_dict = [[] for x in xrange(len(ref) * (len(ref) + 1) / 2)]
    idx = 0
    for r_start in xrange(0, len(ref) + 1):
        for r_end in xrange(r_start + 1, min(len(ref) + 1, r_start + 1 + n)):
            r_dict[idx] = ref[r_start:r_end]
            idx += 1

    # gather number of matched n-grams between hypothesis and reference sentences
    # sys.stderr.write(str(h) + ' ' + str(ref)+'\n')
    n_gram_count = [0 for x in xrange(min(n, len(h)))]
    for i in xrange(n, 0, -1):
        h_start = 0
        h_end = i
        while h_start < len(h) - i + 1:
            potential_gram = h[h_start:h_end]
            if potential_gram in r_dict:
                n_gram_count[i - 1] += 1
                h_start = h_end
                # sys.stderr.write('in!\n')
            else:
                h_start += 1
            h_end = h_start + i

    # calculate n-gram precision
    n_gram_total = range(len(h), max(0, len(h) - n), -1)
    precision = [float(c) / n_gram_total[i] if n_gram_total[i] != 0 else 0.0 for i, c in enumerate(n_gram_count)]

    # return BLEU score
    return bp * reduce(mul, precision, 1)
    # return bp*sum([log(y,10) for y in precision])


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
    for i, (h1, h2, ref) in enumerate(islice(sentences(), opts.num_sentences)):
        #sys.stderr.write('\rsentence %d' % i)
        h1_match = word_matches(h1, ref)
        h2_match = word_matches(h2, ref)
        print(1 if h1_match > h2_match else  # \begin{cases}
              (1 if h1_match == h2_match
               else -1))  # \end{cases}
    sys.stderr.write('\n')


# convention to allow import of this file as a module
if __name__ == '__main__':
    main()