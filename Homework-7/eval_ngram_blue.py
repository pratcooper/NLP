#!/usr/bin/env python
import argparse  # optparse is deprecated
from itertools import islice  # slicing for iterators
from nltk.stem import porter
import math
from collections import Counter # multiset represented by dictionary
from nltk.util import ngrams
import re
from textstat.textstat import textstat
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import string
import nltk
# Prathameshs-MacBook-Pro:Homework-7 prathameshnaik$ python2.7 eval_ngram_blue.py > eval_rogue_blue.out
# Prathameshs-MacBook-Pro:Homework-7 prathameshnaik$ python2.7 compare-with-human-evaluation < eval_rogue_blue.out
# 	  Pred. y=-1	y=0	y=1
# True y=-1	12215	1371	6865
# True y= 0	4319	2953	4872
# True y= 1	7320	1529	15208
#
# Accuracy = 0.536186
N = 4
def weight(n) : return 1.0 / N

stemmer = nltk.stem.porter.PorterStemmer()
remove_punctuation_map = dict((ord(char), None) for char in string.punctuation)

def stem_tokens(tokens):
    return [stemmer.stem(item) for item in tokens]

'''remove punctuation, lowercase, stem'''
def normalize(text):
    return stem_tokens(nltk.word_tokenize(text.lower().translate(remove_punctuation_map)))

vectorizer = TfidfVectorizer(tokenizer=normalize)

def cosine_sim(text1, text2):
    tfidf = vectorizer.fit_transform([text1, text2])
    return ((tfidf * tfidf.T).A)[0,1]

def ngram(sent, gramcount=1):
    if gramcount < 1:
        raise Exception("Must be at least unigrams")
    return [tuple(sent[i:i + gramcount]) for i in range(0, len(sent) - gramcount + 1)]


def stem(sent):
    porterstemmer = porter.PorterStemmer()
    return [porterstemmer.stem(w.decode("utf8").lower()) for w in sent]


def cal_precision(h, ref):
    matches = intersection(h, ref)
    size_of_h = len(h)
    if matches == 0:
        matches = 0.1
    prec = matches / float(size_of_h)
    return prec


def cal_recall(h, ref):
    matches = intersection(h, ref)
    size_of_ref = len(ref)
    if matches == 0:
        matches = 0.1
    recall = matches / float(size_of_ref)
    return recall


def cal_meteor_formula(h, ref):
    alpha = 0.9
    m = intersection(h, ref)
    if len(h) == 0 or len(ref) == 0:
        return 0
    precision = cal_precision(h, ref)
    recall = cal_recall(h, ref)

    num = precision * recall
    deno = (1 - alpha) * recall + alpha * precision
    res = num / float(deno)
    return res


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


def word_matches(h, ref):
    return sum(1 for w in h if w in ref)

def score(hyp, ref):
    system_bleu = 0.0

    bleu = 0.0
    r = len(ref); c = len(hyp)
    if r < c : bp = 1
    else : bp = math.exp((1 - r) / c)
    for n in range(1,N) :
      system_ngrams = set([s for s in ngrams(hyp, n)])
      ref_ngrams = set([s for s in ngrams(ref, n)])
      try : pn = float(len(system_ngrams.intersection(ref_ngrams))) / len(system_ngrams)
      except ZeroDivisionError : pn = 0.0
      try : bleu += bp * (math.exp(weight(n) * math.log(pn)))
      except ValueError : bleu += 0
    system_bleu += bleu
    return system_bleu

def my_lcs(string, sub):

    if(len(string)< len(sub)):
        sub, string = string, sub

    lengths = [[0 for i in range(0,len(sub)+1)] for j in range(0,len(string)+1)]

    for j in range(1,len(sub)+1):
        for i in range(1,len(string)+1):
            if(string[i-1] == sub[j-1]):
                lengths[i][j] = lengths[i-1][j-1] + 1
            else:
                lengths[i][j] = max(lengths[i-1][j] , lengths[i][j-1])

    return lengths[len(string)][len(sub)]

def calc_rogue_score(hyp, ref):

        prec_max = 0.0
        rec_max = 0.0
        beta = 1.2

        lcs = my_lcs(hyp, ref)

        prec_max = lcs/float(len(hyp))
        rec_max = lcs/float(len(ref))

        if (prec_max != 0 and rec_max != 0):
            score = ((1 + beta ** 2) * prec_max * rec_max) / float(rec_max + beta ** 2 * prec_max)
        else:
            score = 0.0

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
                yield [[re.sub(r"[^a-zA-Z0-9]", "", word) for word in sentence.strip().lower().split()] for sentence in pair.split(' ||| ')]

    # note: the -n option does not work in the original code
    for h1, h2, ref in islice(sentences(), opts.num_sentences):
        rset = set(ref)

        h1_ng1_meteor = cal_meteor_formula(stem(h1), stem(ref))
        h2_ng1_meteor = cal_meteor_formula(stem(h2), stem(ref))

        h1_ng2_meteor = cal_meteor_formula(ngram(stem(h1), 2), ngram(stem(ref), 2))
        h2_ng2_meteor = cal_meteor_formula(ngram(stem(h2), 2), ngram(stem(ref), 2))

        h1_ng3_meteor = cal_meteor_formula(ngram(stem(h1), 3), ngram(stem(ref), 3))
        h2_ng3_meteor = cal_meteor_formula(ngram(stem(h2), 3), ngram(stem(ref), 3))

        h1_rogue_score = calc_rogue_score(h1,ref)
        h2_rogue_score = calc_rogue_score(h2,ref)

        h1_word_ratio = float(len(h1)) / len(ref)
        h2_word_ratio = float(len(h2)) / len(ref)

        hyp1 = ' '.join(word for word in h1)
        hyp2 = ' '.join(word for word in h2)
        refer = ' '.join(word for word in ref)
        h1_cosine = cosine_sim(hyp1,refer)
        h2_cosine = cosine_sim(hyp2, refer)


        h1_match = 1.5*h1_ng1_meteor + 1.2*h1_ng2_meteor + 1.2*h1_ng3_meteor + 1.3*h1_rogue_score + 1.2*h1_word_ratio + 1.1*h1_cosine

        h2_match = 1.5*h2_ng1_meteor + 1.2*h2_ng2_meteor + 1.2*h2_ng3_meteor + 1.3*h2_rogue_score + 1.2*h2_word_ratio + 1.1*h2_cosine

        ###### Comment #########
        # Basically use ngram and rogue score and DONT use bleu score
        print(1 if h1_match > h2_match else # \begin{cases}
                (0 if h1_match == h2_match
                    else -1)) # \end{cases}


# convention to allow import of this file as a module
if __name__ == '__main__':
    main()
