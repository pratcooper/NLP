#!/bin/python

import os
import io
import string
import re
import nltk
import pickle
from nltk.stem import PorterStemmer
from nltk.tokenize import word_tokenize


ps = PorterStemmer()

dict_processed = {}
dict_file_word_map = {}

favorite_color = pickle.load( open( "save.p", "rb" ) )


def preprocess_corpus(train_sents):
    """Use the sentences to do whatever preprocessing you think is suitable,
    such as counts, keeping track of rare features/words to remove, matches to lexicons,
    loading files, and so on. Avoid doing any of this in token2features, since
    that will be called on every token of every sentence.

    Of course, this is an optional function.

    Note that you can also call token2features here to aggregate feature counts, etc.
    """
    set_words = set()

    for sent in train_sents:
        for i in xrange(len(sent)):
            if sent[i] not in dict_processed:
                dict_processed[sent[i]] = 1
            else:
                dict_processed[sent[i]] += 1
            set_words.add(sent[i])


    cwd = os.getcwd()
    for filename in os.listdir(cwd + "/data/lexicon/"):
        for word in set_words:
            if word in io.open(cwd + "/data/lexicon/"+filename).read():
                if word not in dict_file_word_map:
                    li = []
                    li.append(filename)
                    dict_file_word_map[word] = li
                else:
                    dict_file_word_map[word].append(filename)
        break


    return dict_processed

def token2features(sent, i,add_neighs = True):
    """Compute the features of a token.

    All the features are boolean, i.e. they appear or they do not. For the token,
    you have to return a set of strings that represent the features that *fire*
    for the token. See the code below.

    The token is at position i, and the rest of the sentence is provided as well.
    Try to make this efficient, since it is called on every token.

    One thing to note is that it is only called once per token, i.e. we do not call
    this function in the inner loops of training. So if your training is slow, it's
    not because of how long it's taking to run this code. That said, if your number
    of features is quite large, that will cause slowdowns for sure.

    add_neighs is a parameter that allows us to use this function itself in order to
    recursively add the same features, as computed for the neighbors. Of course, we do
    not want to recurse on the neighbors again, and then it is set to False (see code).
    """
    ftrs = []
    # bias
    ftrs.append("BIAS")
    # position features
    if i == 0:
        ftrs.append("SENT_BEGIN")
    if i == len(sent)-1:
        ftrs.append("SENT_END")

    # the word itself
    word = unicode(sent[i])
    #word = ps.stem(word)

    ftrs.append("WORD=" + word)
    ftrs.append("LCASE=" + word.lower())
    # some features of the word
    if word.isalnum():
        ftrs.append("IS_ALNUM")
    if word.isnumeric():
        ftrs.append("IS_NUMERIC")
    if word.isdigit():
        ftrs.append("IS_DIGIT")
    if word.isupper():
        ftrs.append("IS_UPPER")
    if word.islower():
        ftrs.append("IS_LOWER")

    #############################
    #word = nltk.word_tokenize(word)

    # #1st feature
    for k, v in favorite_color.iteritems():
        if word in v:
            ftrs.append("LEXICON_" + str(k) + "=TRUE")

    #if word in (favorite_color['firstname.5k'] or favorite_color['firstname.10'] or favorite_color['firstname.100'] or favorite_color['firstname.500'] or favorite_color['firstname.1000'] or favorite_color['lastname.10'] or favorite_color['lastname.100'] or favorite_color['lastname.500'] or favorite_color['lastname.1000'] or favorite_color['lastname.5000'] or favorite_color['people.family_name'] or favorite_color['people.person'] or favorite_color['people.person.lastnames'] or favorite_color['people.person']):
    #    ftrs.append("LEXICON=PERSON")
    if word in (favorite_color['cap.10'] or favorite_color['cap.100'] or favorite_color['cap.500'] or favorite_color['location']or favorite_color['location.country']or favorite_color['venues']):
        ftrs.append("LEXICON_LOCATION=TRUE")
    if word in (favorite_color['english.stop'] or favorite_color['lower.100'] or favorite_color['lower.500'] or favorite_color['lower.1000']):
        ftrs.append("LEXICON_OTHER=TRUE")
    if word in (favorite_color['tv.tv_network'] or favorite_color['tv.tv_program'] or favorite_color['broadcast.tv_channel']):
        ftrs.append("LEXICON_TVSHOW=TRUE")
    if word in (favorite_color['sports.sports_team'] or favorite_color['sports.sports_league']):
        ftrs.append("LEXICON_SPORTS=TRUE")
    #if word in (favorite_color['product'] or favorite_color['business.consumer_company'] or favorite_color['business.consumer_product']):
    #    ftrs.append("LEXICON=PRODUCT")


    # 2nd feature
    tag = nltk.pos_tag([word])[0][1]
    ftrs.append("TAG=" + tag)

    # 3rd feature
    st = ""
    for char in word:
        if char.isupper():
            st = st + 'X'
        elif char.islower():
            st = st + 'x'
        elif char.isdigit():
            st = st + 'd'

    ftrs.append("WORD_SHAPE=" + st)
    #
    # 4th feature
    if re.search(r'\d', word):
        ftrs.append("HAS_DIGIT")

    if "@" in word:
        ftrs.append("CONTAINS_AT")

    # 5th feature
    if "#" in word:
        ftrs.append("CONTAINS_HASH")

    # 6th feature
    if "-" in word:
        ftrs.append("CONTAINS_HIPHEN")


    if "http" in word:
        ftrs.append("IS_LINK")

    # #if word in dict_processed:
    # #    ftrs.append("COUNT_WORD=" + str(dict_processed[word]))
    # #if word in dict_file_word_map:
    # #    ftrs.append("LEX_LIST=" + str(dict_file_word_map[word]))
    #
    # #if word[0].isupper():
    # #    ftrs.append("FIRST_UPPER=" + word[0])
    #
    cnt = 0
    punc =False
    for c in word:
        if (c in "aeiou") or (c in "AEIOU"):
            cnt += 1
        if (c in string.punctuation):
            punc=True

    # 7th feature
    ftrs.append("CONTAINS_PUNC=" + str(punc))

    #ftrs.append("VOWEL_CNT=" + str(cnt))

    # 8th feature
    if len(word) >= 4:
        prf = word[0] + word[1] + word[2]
        ftrs.append("PREFIX=" +prf)
    if len(word) >= 4:
        sf = word[len(word)-3] + word[len(word)-2] + word[len(word)-1]
        ftrs.append("SUFFIX=" +sf)

    # 9th feature
    ftrs.append("LENGTH="+ str(len(word)))

    ftrs.append("LEMMA=" + ps.stem(word))

    #######################################

    # previous/next word feats
    if add_neighs:
        if i > 0:
            for pf in token2features(sent, i-1,add_neighs = False):
                ftrs.append("PREV_" + pf)
        if i < len(sent)-1:
            for pf in token2features(sent, i+1,add_neighs = False):
                ftrs.append("NEXT_" + pf)

    # return it!
    return ftrs

if __name__ == "__main__":
    sents = [
    [ "I","love", "food" ]
    ]
    preprocess_corpus(sents)
    for sent in sents:
        for i in xrange(len(sent)):
            print sent[i], ":", token2features(sent, i)
