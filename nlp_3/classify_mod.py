#!/usr/bin/env python
from collections import defaultdict
from csv import DictReader, DictWriter
import re
import nltk
import codecs
import sys
from nltk.corpus import wordnet as wn
from nltk.tokenize import TreebankWordTokenizer
from nltk.corpus import stopwords
from nltk.tokenize import RegexpTokenizer
from nltk.stem.lancaster import LancasterStemmer
from nltk.stem import *
import itertools

from nltk.collocations import BigramCollocationFinder
from nltk.metrics import BigramAssocMeasures

import string

st = LancasterStemmer()
stemmer = PorterStemmer()
tokenizer = RegexpTokenizer(r'\w+')
kTOKENIZER = TreebankWordTokenizer()
stop = set(stopwords.words('english'))

def morphy_stem(word):
    """
    Simple stemmer
    """
    stem = wn.morphy(word)
    if stem:
        return stem.lower()
    else:
        return word.lower()

class FeatureExtractor:
    def __init__(self):
        """
        You may want to add code here
        """

        None

    def features(self, text):
        d = defaultdict(int)
        for ii in kTOKENIZER.tokenize(text):
            if ii not in stop and ii not in string.punctuation:
                #d[morphy_stem(stemmer.stem(ii))] += 1
                d[stemmer.stem(ii)] += 1
        return d

    def features2(self, text):
        d = defaultdict(int)
        d['first_letter'] = text[0]
        d['last_letter'] = text[len(text) - 1]
        return d

    def features3(self, text):
        d = defaultdict(int)
        text_list = kTOKENIZER.tokenize(text)
        for a in text_list:
            if a not in string.punctuation:
                d['first_word'] = a
                break

        i = len(text_list) - 1

        while(i >=0):
            if text_list[i] not in string.punctuation:
                d['last_word'] = text_list[i]
                break
            i-=1

        return d

    def features4(self, text):
        d = defaultdict(int)
        i = bool(re.search(r'\d', text))
        if i:
            d['is_num'] = 1

        return d

    def features5(self,text):
        d = defaultdict(int)
        count = 0
        for i in text:
            if i in "aeiou":
                count =  count + 1

        d['vowels'] = count

        return d

reader = codecs.getreader('utf8')
writer = codecs.getwriter('utf8')


def prepfile(fh, code):
  if type(fh) is str:
    fh = open(fh, code)
  ret = gzip.open(fh.name, code if code.endswith("t") else code+"t") if fh.name.endswith(".gz") else fh
  if sys.version_info[0] == 2:
    if code.startswith('r'):
      ret = reader(fh)
    elif code.startswith('w'):
      ret = writer(fh)
    else:
      sys.stderr.write("I didn't understand code "+code+"\n")
      sys.exit(1)
  return ret

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument("--trainfile", "-i", nargs='?', type=argparse.FileType('r'), default=sys.stdin, help="input train file")
    parser.add_argument("--testfile", "-t", nargs='?', type=argparse.FileType('r'), default=None, help="input test file")
    parser.add_argument("--outfile", "-o", nargs='?', type=argparse.FileType('w'), default=sys.stdout, help="output file")
    parser.add_argument('--subsample', type=float, default=1.0,
                        help='subsample this fraction of total')
    args = parser.parse_args()
    trainfile = prepfile(args.trainfile, 'r')
    if args.testfile is not None:
        testfile = prepfile(args.testfile, 'r')
    else:
        testfile = None
    outfile = prepfile(args.outfile, 'w')

    # Create feature extractor (you may want to modify this)
    fe = FeatureExtractor()
    
    # Read in training data
    train = DictReader(trainfile, delimiter='\t')

    
    # Split off dev section
    dev_train = []
    dev_test = []
    full_train = []


    for ii in train:
        if args.subsample < 1.0 and int(ii['id']) % 100 > 100 * args.subsample:
            continue
        feat = fe.features(ii['text'])
        #feat= dict(feat.items()[len(feat) / 10:])
        feat2 = fe.features2(ii['text'])
        #feat2 = dict(feat2.items()[len(feat2) / 10:])
        feat3 = fe.features3(ii['text'])
        feat4 = fe.features4(ii['text'])
        feat5 = fe.features5(ii['text'])
        #feat4 = dict(feat4.items()[len(feat4) / 10:])
        #print feat4

        if int(ii['id']) % 5 == 0:
            dev_test.append((feat, ii['cat']))
            dev_test.append((feat2, ii['cat']))
            #dev_test.append((feat3, ii['cat']))
            dev_test.append((feat5, ii['cat']))
            #if feat4.has_key('is_num'):
            #    dev_test.append((feat4, ii['cat']))
        else:
            dev_train.append((feat, ii['cat']))
            dev_train.append((feat2, ii['cat']))
            #dev_train.append((feat3, ii['cat']))
            dev_train.append((feat5, ii['cat']))
            #if feat4.has_key('is_num'):
            #    dev_test.append((feat4, ii['cat']))
        full_train.append((feat, ii['cat']))
        full_train.append((feat2, ii['cat']))
        #full_train.append((feat3, ii['cat']))
        full_train.append((feat5, ii['cat']))
        #if feat4.has_key('is_num'):
        #    dev_test.append((feat4, ii['cat']))

    # Train a classifier
    sys.stderr.write("Training classifier ...\n")
    classifier = nltk.classify.NaiveBayesClassifier.train(dev_train)

    right = 0
    total = len(dev_test)
    for ii in dev_test:
        prediction = classifier.classify(ii[0])
        if prediction == ii[1]:
            right += 1
    sys.stderr.write("Accuracy on dev: %f\n" % (float(right) / float(total)))

    if testfile is None:
        sys.stderr.write("No test file passed; stopping.\n")
    else:
        # Retrain on all data
        classifier = nltk.classify.NaiveBayesClassifier.train(dev_train + dev_test)

        # Read in test section
        test = {}
        for ii in DictReader(testfile, delimiter='\t'):
            test[ii['id']] = classifier.classify(fe.features(ii['text']))

        # Write predictions
        o = DictWriter(outfile, ['id', 'pred'])
        o.writeheader()
        for ii in sorted(test):
            o.writerow({'id': ii, 'pred': test[ii]})
